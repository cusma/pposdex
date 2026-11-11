import base64
import logging
import math
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, NotRequired, TypedDict, cast

import msgpack
from algosdk.constants import microalgos_to_algos_ratio
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from pposdex import helpers
from pposdex import inequality_idx as idx
from pposdex.helpers import Account, Json, PPoSDexError

logger = logging.getLogger(__name__)

d_N = 1  # noqa: N816 (math notation)
d_T = 1  # noqa: N816 (math notation)
MICROALGO_TOTAL_SUPPLY = 10**16
# PPoS Dex v3: the fewest online accounts holding more than these shares of the
# online stake, the thresholds that matter to Algorand consensus
V3_SHARES = {
    # Protocol upgrades need 90% of the proposed blocks to approve them: more
    # than 10% of the online stake can block them
    "veto": 0.1,
    # Conservatively, consensus stalls when more than 20% of the online stake
    # does not vote
    "liveness": 0.2,
    # More than 1/3 of the online stake breaks the honest majority assumption
    "nakamoto": 1 / 3,
    # Protocol upgrades need the broad agreement of more than 90% of the online
    # stake: how many accounts that supermajority takes
    "upgrade": 0.9,
}
# Published by 4.0.0, before v3 had more than the liveness coefficient
LEGACY_KEYS = {
    "ppos_dex_v3": "ppos_dex_v3_liveness",
    "ppos_dex_v3_operators": "ppos_dex_v3_liveness_operators",
}


class PPoSDexData(TypedDict):
    """PPoS Dex data point, as published on-chain"""

    algo_threshold: int
    accounts: int
    algo_dynamics: float
    ppos_online_stake: float
    ppos_online_accounts: float
    algo_hhi: NotRequired[float]
    ppos_gini: float
    ppos_theil_l: float
    ppos_theil_t: float
    ppos_hhi: NotRequired[float]
    ppos_dex: float
    ppos_dex_v2: NotRequired[float]
    ppos_dex_v3_veto: NotRequired[int]
    ppos_dex_v3_veto_operators: NotRequired[int]
    ppos_dex_v3_liveness: NotRequired[int]
    ppos_dex_v3_liveness_operators: NotRequired[int]
    ppos_dex_v3_nakamoto: NotRequired[int]
    ppos_dex_v3_nakamoto_operators: NotRequired[int]
    ppos_dex_v3_upgrade: NotRequired[int]
    ppos_dex_v3_upgrade_operators: NotRequired[int]
    round: NotRequired[int]
    timestamp: str


# PPoS Dex data point keys holding a metric
Metric = Literal[
    "algo_dynamics",
    "ppos_online_stake",
    "ppos_online_accounts",
    "algo_hhi",
    "ppos_gini",
    "ppos_theil_l",
    "ppos_theil_t",
    "ppos_hhi",
    "ppos_dex",
    "ppos_dex_v2",
    "ppos_dex_v3_veto",
    "ppos_dex_v3_veto_operators",
    "ppos_dex_v3_liveness",
    "ppos_dex_v3_liveness_operators",
    "ppos_dex_v3_nakamoto",
    "ppos_dex_v3_nakamoto_operators",
    "ppos_dex_v3_upgrade",
    "ppos_dex_v3_upgrade_operators",
]


class InvalidDataError(ValueError):
    """PPoS Dex data point does not comply with the schema"""


@dataclass(frozen=True)
class Field:
    type: type
    min: float | None = None
    max: float | None = None
    required: bool = True


SCHEMA: dict[str, Field] = {
    "algo_threshold": Field(int),
    "accounts": Field(int, min=0),
    "algo_dynamics": Field(float, min=0),
    "ppos_online_stake": Field(float, min=0, max=1),
    "ppos_online_accounts": Field(float, min=0, max=1),
    "algo_hhi": Field(float, min=0, max=1, required=False),
    "ppos_gini": Field(float, min=0, max=1),
    "ppos_theil_l": Field(float, min=0),
    "ppos_theil_t": Field(float, min=0),
    "ppos_hhi": Field(float, min=0, max=1, required=False),
    "ppos_dex": Field(float, min=0, max=1),
    "ppos_dex_v2": Field(float, min=0, max=1, required=False),
    "ppos_dex_v3_veto": Field(int, min=1, required=False),
    "ppos_dex_v3_veto_operators": Field(int, min=1, required=False),
    "ppos_dex_v3_liveness": Field(int, min=1, required=False),
    "ppos_dex_v3_liveness_operators": Field(int, min=1, required=False),
    "ppos_dex_v3_nakamoto": Field(int, min=1, required=False),
    "ppos_dex_v3_nakamoto_operators": Field(int, min=1, required=False),
    "ppos_dex_v3_upgrade": Field(int, min=1, required=False),
    "ppos_dex_v3_upgrade_operators": Field(int, min=1, required=False),
    "round": Field(int, min=0, required=False),
    "timestamp": Field(str),
}


def validate(data: object) -> PPoSDexData:
    """
    Validate a PPoS Dex data point against the SCHEMA

    Keys published by older versions are renamed, and unknown keys, like those
    added by newer versions, are ignored.

    Args:
        data: PPoS Dex data point

    Returns:
        The validated data point, without unknown keys

    Raises:
        InvalidDataError: if the data point does not comply with the SCHEMA
    """
    if not isinstance(data, dict):
        raise InvalidDataError(f"Expected a mapping, got {type(data).__name__}")

    data = {LEGACY_KEYS.get(key, key): value for key, value in data.items()}
    unknown_keys = data.keys() - SCHEMA.keys()
    if unknown_keys:
        logger.debug("Ignoring unknown keys: %s", sorted(map(str, unknown_keys)))
        data = {key: value for key, value in data.items() if key in SCHEMA}

    for key, spec in SCHEMA.items():
        if key not in data:
            if spec.required:
                raise InvalidDataError(f"Missing key: {key}")
            continue
        value = data[key]
        if not isinstance(value, spec.type):
            raise InvalidDataError(f"{key}: expected {spec.type.__name__}")
        if not isinstance(value, int | float):
            continue
        if spec.min is not None and value < spec.min:
            raise InvalidDataError(f"{key}: {value} < {spec.min}")
        if spec.max is not None and value > spec.max:
            raise InvalidDataError(f"{key}: {value} > {spec.max}")

    return cast(PPoSDexData, data)


def online_accounts(data: PPoSDexData) -> float:
    """Online accounts holding at least the threshold"""
    return data["accounts"] * data["ppos_online_accounts"]


def effective_validators(data: PPoSDexData) -> float:
    """Equal-stake validators with the same stake entropy as the online ones

    Theil T is the log of the online accounts minus the stake entropy H, so
    the entropy equivalent number of validators exp(H) is N * exp(-T).
    """
    return online_accounts(data) * math.exp(-data["ppos_theil_t"])


def equal_stake_validators(data: PPoSDexData) -> float:
    """Equal-stake validators with the same HHI as the online ones"""
    hhi = data.get("ppos_hhi")
    return 1 / hhi if hhi else math.nan


def operator_stakes(online_accounts: list[Json]) -> list[int]:
    """
    Stakes of the likely operators of online accounts

    Accounts are merged when rekeyed to the same address, or when their
    participation keys share the same validity window: likely registered
    together by the same operator.

    Args:
        online_accounts: Online accounts, as returned by the Indexer

    Returns:
        Stake of each operator
    """
    operator = {account["address"]: account["address"] for account in online_accounts}

    def find(address: str) -> str:
        while operator[address] != address:
            operator[address] = operator[operator[address]]
            address = operator[address]
        return address

    first_by_link: dict[object, str] = {}
    for account in online_accounts:
        keys = account.get("participation") or {}
        window = (keys.get("vote-first-valid"), keys.get("vote-last-valid"))
        links = [("auth", account.get("auth-addr")), ("window", window)]
        for link in links:
            if link[1] is None or link[1] == (None, None):
                continue
            first = first_by_link.setdefault(link, account["address"])
            operator[find(account["address"])] = find(first)

    stakes: dict[str, int] = {}
    for account in online_accounts:
        root = find(account["address"])
        stakes[root] = stakes.get(root, 0) + account["amount"]
    return list(stakes.values())


def post_ppos_dex_data(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    publisher: Account,
    algo_threshold: int,
    wait_rounds: int = 0,
) -> PPoSDexData:
    """
    Post PPoS Dex data on-chain

    Args:
        algod_client: Algod Client
        indexer_client: Algorand Indexer Client
        publisher: Data publisher account
        algo_threshold: Minimum balance data filter (expressed in ALGOs)
        wait_rounds: Wait rounds for note publishing confirmation

    Returns:
        PPoS Dex published data
    """
    microalgo_threshold = algo_threshold * microalgos_to_algos_ratio
    holders = helpers.get_algo_holders(indexer_client, microalgo_threshold)

    stakes = [account["amount"] for account in holders]
    online = [account for account in holders if account["status"] == "Online"]
    # Sorted: the indexes below sum the stakes in this order
    online_stakes = sorted(account["amount"] for account in online)

    ledger = algod_client.ledger_supply()
    assert isinstance(ledger, dict)

    # Data Processing
    algo_dyn = ledger["total-money"] / MICROALGO_TOTAL_SUPPLY
    algo_prt = ledger["online-money"] / ledger["total-money"]
    accounts_prt = len(online_stakes) / len(stakes)
    algo_hhi = idx.herfindahl_hirschman(stakes)
    ppos_gini = idx.gini(online_stakes)
    ppos_theil_l = idx.theil_l(online_stakes)
    ppos_theil_t = idx.theil_t(online_stakes)
    ppos_hhi = idx.herfindahl_hirschman(online_stakes)
    ppos_dex_v1 = d_N * d_T * algo_dyn * algo_prt * accounts_prt * (1 - ppos_gini)
    ppos_dex_v2 = d_N * d_T * algo_dyn * algo_prt * (1 - ppos_hhi)
    operators = operator_stakes(online)
    # Each coefficient by account, and by likely operator
    v3 = {
        name: (
            idx.nakamoto_coefficient(online_stakes, share),
            idx.nakamoto_coefficient(operators, share),
        )
        for name, share in V3_SHARES.items()
    }

    ppos_dex_data: PPoSDexData = {
        "algo_threshold": algo_threshold,
        "accounts": len(stakes),
        "algo_dynamics": algo_dyn,
        "ppos_online_stake": algo_prt,
        "ppos_online_accounts": accounts_prt,
        "algo_hhi": algo_hhi,
        "ppos_gini": ppos_gini,
        "ppos_theil_l": ppos_theil_l,
        "ppos_theil_t": ppos_theil_t,
        "ppos_hhi": ppos_hhi,
        "ppos_dex": ppos_dex_v1,
        "ppos_dex_v2": ppos_dex_v2,
        "ppos_dex_v3_veto": v3["veto"][0],
        "ppos_dex_v3_veto_operators": v3["veto"][1],
        "ppos_dex_v3_liveness": v3["liveness"][0],
        "ppos_dex_v3_liveness_operators": v3["liveness"][1],
        "ppos_dex_v3_nakamoto": v3["nakamoto"][0],
        "ppos_dex_v3_nakamoto_operators": v3["nakamoto"][1],
        "ppos_dex_v3_upgrade": v3["upgrade"][0],
        "ppos_dex_v3_upgrade_operators": v3["upgrade"][1],
        "round": ledger["current_round"],
        "timestamp": str(datetime.now()),
    }
    ppos_dex_data = validate(ppos_dex_data)

    # Publish Data
    helpers.post_note(
        algod_client, publisher, msgpack.packb(ppos_dex_data), wait_rounds
    )
    return ppos_dex_data


def get_ppos_dex_data(
    indexer_client: IndexerClient,
    publisher_address: str,
    algo_threshold: int,
    start_block: int,
    end_block: int | None = None,
) -> list[PPoSDexData]:
    """
    Get PPoS Dex data from chain

    Args:
        indexer_client: Algorand Indexer Client
        publisher_address: Publisher address to read from
        algo_threshold: Minimum balance data filter (expressed in ALGOs)
        start_block: Data starting block
        end_block: Data ending block

    Returns:
        List of PPoS Dex data points
    """
    ppos_dex_txns_note = helpers.get_address_txns_note(
        indexer_client, publisher_address, start_block, end_block
    )

    ppos_dex_data: list[PPoSDexData] = []
    for txn_note in ppos_dex_txns_note:
        try:
            data = validate(msgpack.unpackb(base64.b64decode(txn_note)))
            if data["algo_threshold"] == algo_threshold:
                ppos_dex_data += [data]
        except (InvalidDataError, msgpack.ExtraData) as err:
            # Ignore non compliant or wrongly serialized data
            logger.debug("Skipping note %s: %s", txn_note, err)

    if not ppos_dex_data:
        raise PPoSDexError(
            f"No valid PPoS Dex data published by {publisher_address} "
            f"starting from block {start_block}."
        )

    return ppos_dex_data
