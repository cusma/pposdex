import base64
import logging
from collections.abc import Callable

import pytest
from algosdk import account, transaction
from fakes import FakeAlgod, FakeIndexer

from pposdex import helpers
from pposdex.helpers import Account, Json, PPoSDexError


class TestAccount:
    def test_address(self) -> None:
        private_key, address = account.generate_account()
        assert Account(private_key=private_key).address == address

    def test_private_key_not_in_repr(self, publisher: Account) -> None:
        assert publisher.private_key not in repr(publisher)


class TestPublisherAccount:
    def test_from_mnemonic(
        self,
        monkeypatch: pytest.MonkeyPatch,
        publisher: Account,
        publisher_mnemonic: str,
    ) -> None:
        monkeypatch.setenv(helpers.ENV_MNEMONIC, publisher_mnemonic)
        assert helpers.get_publisher_account() == publisher

    def test_missing_mnemonic(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv(helpers.ENV_MNEMONIC, raising=False)
        with pytest.raises(PPoSDexError, match=helpers.ENV_MNEMONIC):
            helpers.get_publisher_account()


class TestIndexerRequest:
    def test_retries_then_succeeds(
        self,
        indexer: FakeIndexer,
        make_holders: Callable[[int], list[Json]],
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        indexer.holders = make_holders(3)
        indexer.failures = 2
        assert len(helpers.get_algo_holders(indexer)) == 3
        assert caplog.messages.count("Retrying the Indexer request...") == 2

    def test_gives_up(
        self, indexer: FakeIndexer, caplog: pytest.LogCaptureFixture
    ) -> None:
        indexer.failures = helpers.MAX_ATTEMPTS
        with pytest.raises(PPoSDexError, match="Indexer request failed"):
            helpers.get_algo_holders(indexer)
        assert len(indexer.requests) == helpers.MAX_ATTEMPTS
        # No retry is announced after the last attempt
        retries = caplog.messages.count("Retrying the Indexer request...")
        assert retries == helpers.MAX_ATTEMPTS - 1


class TestAlgoHolders:
    def test_paginates(
        self, indexer: FakeIndexer, make_holders: Callable[[int], list[Json]]
    ) -> None:
        indexer.holders = make_holders(2500)
        assert helpers.get_algo_holders(indexer) == indexer.holders
        # 3 pages of 1000 accounts, then an empty one
        assert len(indexer.requests) == 4
        assert {r["limit"] for r in indexer.requests} == {helpers.ACCOUNTS_PAGE_SIZE}

    def test_min_balance(
        self, indexer: FakeIndexer, make_holders: Callable[[int], list[Json]]
    ) -> None:
        indexer.holders = make_holders(100)
        threshold = 50_000 * 10**6
        holders = helpers.get_algo_holders(indexer, threshold)
        assert holders
        assert all(h["amount"] > threshold for h in holders)

    def test_no_holders(self, indexer: FakeIndexer) -> None:
        with pytest.raises(PPoSDexError, match="No account"):
            helpers.get_algo_holders(indexer, 1)


class TestAddressTxnsNote:
    def test_paginates_and_skips_txns_without_note(self, indexer: FakeIndexer) -> None:
        notes = [f"note {i}".encode() for i in range(1500)]
        indexer.notes["PUBLISHER"] = notes
        txns_note = helpers.get_address_txns_note(indexer, "PUBLISHER", 1, 2)
        assert txns_note == [base64.b64encode(note).decode() for note in notes]
        assert indexer.requests[0]["min_round"] == 1
        assert indexer.requests[0]["max_round"] == 2

    def test_no_notes(self, indexer: FakeIndexer) -> None:
        with pytest.raises(PPoSDexError, match="No published note"):
            helpers.get_address_txns_note(indexer, "NOBODY")


def test_post_note(
    algod: FakeAlgod, publisher: Account, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.DEBUG, logger="pposdex")
    confirmed = helpers.post_note(algod, publisher, b"hello", wait_rounds=3)

    assert confirmed["confirmed-round"] == 1001
    (signed,) = algod.sent
    # A zero ALGO payment to self, signed by the publisher alone
    assert isinstance(signed, transaction.SignedTransaction)
    assert signed.signature
    txn = signed.transaction
    assert isinstance(txn, transaction.PaymentTxn)
    assert (txn.sender, txn.receiver, txn.amt, txn.note) == (
        publisher.address,
        publisher.address,
        0,
        b"hello",
    )
    assert "Publishing Algorand PPoS Dex data in txID: TXID" in caplog.messages
