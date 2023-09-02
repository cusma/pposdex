from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algokit_utils import Account

from src.helpers import post_note
from src.ppos_dex_data import SCHEMA, get_ppos_dex_data, post_ppos_dex_data


def test_ppos_dex_data(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    faucet: Account,
) -> None:
    post_data = post_ppos_dex_data(algod_client, indexer_client, faucet, 0, SCHEMA)
    post_note(algod_client, faucet, b"noise")
    post_note(algod_client, faucet, b"more noise")
    post_note(algod_client, faucet, b"even more noise")
    get_data = get_ppos_dex_data(indexer_client, faucet.address, 0, SCHEMA, 0)
    assert get_data[0] == post_data
