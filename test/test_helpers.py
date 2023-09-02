import base64

from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algokit_utils import Account

from src.helpers import get_algo_holders, get_address_txns_note, post_note


def test_get_algo_holders(
    indexer_client: IndexerClient,
    faucet: Account,
) -> None:
    holders = get_algo_holders(indexer_client)
    assert faucet.address in [account["address"] for account in holders]


def test_post_note(
    algod_client: AlgodClient,
    faucet: Account,
) -> None:
    note = b"test"
    post_txn = post_note(algod_client, faucet, note)
    assert post_txn["txn"]["txn"]["note"] == base64.b64encode(note).decode()


def test_get_address_txns_note(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    faucet: Account,
) -> None:
    note = b"silvio"
    post_note(algod_client, faucet, note)
    post_note(algod_client, faucet, b"noise")
    post_note(algod_client, faucet, b"more noise")
    post_note(algod_client, faucet, b"even more noise")
    published_notes = get_address_txns_note(indexer_client, faucet.address)
    assert base64.b64encode(note).decode() in published_notes
