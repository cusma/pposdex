from collections.abc import Callable

from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from pposdex.helpers import Account, post_note
from pposdex.ppos_dex_data import get_ppos_dex_data, post_ppos_dex_data


def test_ppos_dex_data(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    faucet: Account,
    wait_for_indexer: Callable[[int], None],
) -> None:
    post_data = post_ppos_dex_data(algod_client, indexer_client, faucet, 0)
    post_note(algod_client, faucet, b"noise")
    post_note(algod_client, faucet, b"more noise")
    last_txn = post_note(algod_client, faucet, b"even more noise")
    wait_for_indexer(last_txn["confirmed-round"])
    get_data = get_ppos_dex_data(indexer_client, faucet.address, 0, 0)
    assert get_data[0] == post_data
