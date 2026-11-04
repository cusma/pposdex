import base64
import logging
from collections.abc import Callable

import msgpack
import pytest
from fakes import ONLINE_MONEY, TOTAL_MONEY, FakeAlgod, FakeIndexer

from pposdex import inequality_idx as idx
from pposdex import ppos_dex_data as pposdex
from pposdex.helpers import Account, Json, PPoSDexError
from pposdex.ppos_dex_data import PPoSDexData

PUBLISHER = "PUBLISHER"


def b64(note: bytes) -> str:
    return base64.b64encode(note).decode()


class TestPost:
    def test_computes_and_publishes(
        self,
        algod: FakeAlgod,
        indexer: FakeIndexer,
        publisher: Account,
        make_holders: Callable[[int], list[Json]],
    ) -> None:
        indexer.holders = make_holders(300)
        data = pposdex.post_ppos_dex_data(algod, indexer, publisher, 1000)

        stakes = [h["amount"] for h in indexer.holders if h["amount"] > 10**9]
        online = sorted(
            h["amount"]
            for h in indexer.holders
            if h["amount"] > 10**9 and h["status"] == "Online"
        )
        assert data["accounts"] == len(stakes)
        assert data["algo_dynamics"] == TOTAL_MONEY / pposdex.MICROALGO_TOTAL_SUPPLY
        assert data["ppos_online_stake"] == ONLINE_MONEY / TOTAL_MONEY
        assert data["ppos_online_accounts"] == len(online) / len(stakes)
        assert data["algo_hhi"] == idx.herfindahl_hirschman(stakes)
        assert data["ppos_gini"] == idx.gini(online)
        assert data["ppos_theil_l"] == idx.theil_l(online)
        assert data["ppos_theil_t"] == idx.theil_t(online)
        assert data["ppos_hhi"] == idx.herfindahl_hirschman(online)
        # Fake accounts share no keys: every account is its own operator
        assert data["ppos_dex_v3"] == idx.nakamoto_coefficient(
            online, pposdex.CONSENSUS_SHARE
        )
        assert data["ppos_dex_v3_operators"] == data["ppos_dex_v3"]
        assert data["round"] == 1000
        # The published note is the same data point, msgpack encoded
        (signed,) = algod.sent
        assert msgpack.unpackb(signed.transaction.note) == data

    def test_invalid_data_is_not_published(
        self,
        algod: FakeAlgod,
        indexer: FakeIndexer,
        publisher: Account,
        make_holders: Callable[[int], list[Json]],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        indexer.holders = make_holders(30)
        monkeypatch.setattr(pposdex, "MICROALGO_TOTAL_SUPPLY", -1)
        with pytest.raises(pposdex.InvalidDataError, match="algo_dynamics"):
            pposdex.post_ppos_dex_data(algod, indexer, publisher, 1000)
        assert not algod.sent


def account(
    address: str, amount: int, auth: str | None = None, window: int | None = None
) -> Json:
    keys = (
        {"vote-first-valid": window, "vote-last-valid": window + 100}
        if window
        else None
    )
    return {
        "address": address,
        "amount": amount,
        "auth-addr": auth,
        "participation": keys,
    }


def test_operator_stakes() -> None:
    accounts = [
        account("A", 1, auth="X"),
        account("B", 2, auth="X"),
        account("C", 4, window=10),
        account("D", 8, window=10),
        account("E", 16),
        # Rekeyed elsewhere, but registered with C and D
        account("F", 32, auth="Y", window=10),
        account("G", 64, window=20),
    ]
    assert sorted(pposdex.operator_stakes(accounts)) == [3, 16, 44, 64]


class TestGet:
    def test_reads_valid_data_for_threshold(
        self,
        indexer: FakeIndexer,
        make_data_point: Callable[..., PPoSDexData],
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        caplog.set_level(logging.DEBUG, logger="pposdex")
        latest = make_data_point(timestamp="2026-11-02 00:00:00.000000")
        oldest = make_data_point(timestamp="2026-11-01 00:00:00.000000")
        noise, incomplete = b"noise", msgpack.packb({"ppos_dex": 2.0})
        indexer.notes[PUBLISHER] = [
            msgpack.packb(latest),
            noise,
            incomplete,
            msgpack.packb(make_data_point(algo_threshold=1)),
            msgpack.packb(oldest),
        ]

        data = pposdex.get_ppos_dex_data(indexer, PUBLISHER, 1000, 1, 2)

        assert data == [latest, oldest]
        assert indexer.requests[0]["min_round"] == 1
        skipped = [m for m in caplog.messages if m.startswith("Skipping note")]
        assert skipped == [
            f"Skipping note {b64(noise)}: unpack(b) received extra data.",
            f"Skipping note {b64(incomplete)}: Missing key: algo_threshold",
        ]

    def test_no_valid_data(
        self, indexer: FakeIndexer, make_data_point: Callable[..., PPoSDexData]
    ) -> None:
        indexer.notes[PUBLISHER] = [msgpack.packb(make_data_point(algo_threshold=1))]
        with pytest.raises(PPoSDexError, match="No valid PPoS Dex data"):
            pposdex.get_ppos_dex_data(indexer, PUBLISHER, 1000, 1)
