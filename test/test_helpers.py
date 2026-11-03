import base64
from collections.abc import Callable

import pytest
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from pposdex.helpers import (
    Account,
    get_address_txns_note,
    get_algo_holders,
    post_note,
)

pytestmark = pytest.mark.integration


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
    wait_for_indexer: Callable[[int], None],
) -> None:
    note = b"silvio"
    post_note(algod_client, faucet, note)
    post_note(algod_client, faucet, b"noise")
    post_note(algod_client, faucet, b"more noise")
    last_txn = post_note(algod_client, faucet, b"even more noise")
    wait_for_indexer(last_txn["confirmed-round"])
    published_notes = get_address_txns_note(indexer_client, faucet.address)
    assert base64.b64encode(note).decode() in published_notes
