import base64
import msgpack
import schema

from datetime import datetime
from typing import Optional

from algokit_utils import Account
from algosdk.constants import microalgos_to_algos_ratio
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

import src.inequality_idx as idx
import src.helpers as helpers

d_N = 1
d_T = 1
MICROALGO_TOTAL_SUPPLY = 10**16
SCHEMA = schema.Schema(
    {
        "algo_threshold": int,
        "accounts": schema.And(int, lambda n: 0 <= n),
        "algo_dynamics": schema.And(float, lambda n: 0 <= n),
        "ppos_online_stake": schema.And(float, lambda n: 0 <= n <= 1),
        "ppos_online_accounts": schema.And(float, lambda n: 0 <= n <= 1),
        schema.Optional("algo_hhi"): schema.And(float, lambda n: 0 <= n <= 1),
        "ppos_gini": schema.And(float, lambda n: 0 <= n <= 1),
        "ppos_theil_l": schema.And(float, lambda n: 0 <= n),
        "ppos_theil_t": schema.And(float, lambda n: 0 <= n),
        schema.Optional("ppos_hhi"): schema.And(float, lambda n: 0 <= n <= 1),
        "ppos_dex": schema.And(float, lambda n: 0 <= n <= 1),
        schema.Optional("ppos_dex_v2"): schema.And(float, lambda n: 0 <= n <= 1),
        "timestamp": str,
    }
)


def post_ppos_dex_data(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    publisher: Account,
    algo_threshold: int,
    data_schema: schema.Schema,
    wait_rounds: int = 0,
) -> dict:
    """
    Post PPoS Dex data on-chain

    Args:
        algod_client: Algod Client
        indexer_client: Algorand Indexer Client
        publisher: Data publisher account
        algo_threshold: Minimum balance data filter (expressed in ALGOs)
        data_schema: Data validation schema
        wait_rounds: Wait rounds for note publishing confirmation

    Returns:
        PPoS Dex published data
    """
    microalgo_threshold = algo_threshold * microalgos_to_algos_ratio
    holders = helpers.get_algo_holders(indexer_client, microalgo_threshold)

    stakes = [account["amount"] for account in holders]
    online_stakes = [
        account["amount"] for account in holders if account["status"] == "Online"
    ]

    ledger = algod_client.ledger_supply()

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

    ppos_dex_data = {
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
    ppos_dex_data = data_schema.validate(ppos_dex_data)

    # Publish Data
    helpers.post_note(
        algod_client, publisher, msgpack.packb(ppos_dex_data), wait_rounds
    )
    return ppos_dex_data


def get_ppos_dex_data(
    indexer_client: IndexerClient,
    publisher_address: str,
    algo_threshold: int,
    data_schema: schema.Schema,
    start_block: int,
    end_block: Optional[int] = None,
) -> list[dict]:
    """
    Get PPoS Dex data from chain

    Args:
        indexer_client: Algorand Indexer Client
        publisher_address: Publisher addres to read from
        algo_threshold: Minimum balance data filter (expressed in ALGOs)
        data_schema: Data validation schema
        start_block: Data starting block
        end_block: Data ending block

    Returns:
        List of PPoS Dex data points
    """
    ppos_dex_txns_note = helpers.get_address_txns_note(
        indexer_client, publisher_address, start_block, end_block
    )

    ppos_dex_data: list[dict] = []
    for txn_note in ppos_dex_txns_note:
        try:
            data: dict = msgpack.unpackb(base64.b64decode(txn_note))
            data = data_schema.validate(data)
            if data["algo_threshold"] == algo_threshold:
                ppos_dex_data += [data]
        except schema.SchemaError:
            # Ignore non compliant data
            pass
        except msgpack.ExtraData:
            # Ignore wrongly serialized data
            pass

    if not ppos_dex_data:
        quit(
            f"No valid PPos Dex data published by {publisher_address} starting from block {start_block}."
        )

    return ppos_dex_data
