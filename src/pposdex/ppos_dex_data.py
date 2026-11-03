import base64
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, NotRequired, TypedDict, cast

import msgpack
from algosdk.constants import microalgos_to_algos_ratio
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from pposdex import helpers
from pposdex import inequality_idx as idx
from pposdex.helpers import Account

d_N = 1  # noqa: N816 (math notation)
d_T = 1  # noqa: N816 (math notation)
MICROALGO_TOTAL_SUPPLY = 10**16


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
    "timestamp": Field(str),
}


def validate(data: object) -> PPoSDexData:
    """
    Validate a PPoS Dex data point against the SCHEMA

    Args:
        data: PPoS Dex data point

    Returns:
        The validated data point

    Raises:
        InvalidDataError: if the data point does not comply with the SCHEMA
    """
    if not isinstance(data, dict):
        raise InvalidDataError(f"Expected a mapping, got {type(data).__name__}")

    unknown_keys = data.keys() - SCHEMA.keys()
    if unknown_keys:
        raise InvalidDataError(f"Unknown keys: {sorted(map(str, unknown_keys))}")

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
    # Sorted: the indexes below sum the stakes in this order
    online_stakes = sorted(
        account["amount"] for account in holders if account["status"] == "Online"
    )

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
        publisher_address: Publisher addres to read from
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
        except InvalidDataError:
            # Ignore non compliant data
            pass
        except msgpack.ExtraData:
            # Ignore wrongly serialized data
            pass

    if not ppos_dex_data:
        sys.exit(
            f"No valid PPos Dex data published by {publisher_address} "
            f"starting from block {start_block}."
        )

    return ppos_dex_data
