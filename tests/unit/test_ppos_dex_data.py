import base64
import csv
import logging
import math
from collections.abc import Callable
from pathlib import Path

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
        v3 = {
            name: idx.nakamoto_coefficient(online, share)
            for name, share in pposdex.V3_SHARES.items()
        }
        assert data["ppos_dex_v3_veto"] == data["ppos_dex_v3_veto_operators"]
        assert data["ppos_dex_v3_veto"] == v3["veto"]
        assert data["ppos_dex_v3_liveness"] == v3["liveness"]
        assert data["ppos_dex_v3_nakamoto"] == v3["nakamoto"]
        assert data["ppos_dex_v3_upgrade"] == v3["upgrade"]
        assert data["ppos_dex_v3_upgrade_operators"] == v3["upgrade"]
        # The coefficients grow with their thresholds
        assert v3["veto"] <= v3["liveness"] <= v3["nakamoto"] <= v3["upgrade"]
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


class TestWithRecomputed:
    @staticmethod
    def write(path: Path, rows: list[dict[str, object]]) -> Path:
        columns = ["timestamp", "round", "published", "algo_threshold"]
        with path.open("w", encoding="utf8", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=[*columns, *pposdex.RECOMPUTED_METRICS]
            )
            writer.writeheader()
            writer.writerows({"published": 1} | row for row in rows)
        return path

    def test_fills_only_the_missing_metrics(
        self, tmp_path: Path, make_data_point: Callable[..., PPoSDexData]
    ) -> None:
        old = make_data_point(timestamp="2021-01-01 00:00:00.0")
        v4 = make_data_point(timestamp="2026-11-01 00:00:00.0", ppos_dex_v3_liveness=7)
        new = make_data_point(timestamp="2026-11-02 00:00:00.0")
        values: dict[str, object] = dict.fromkeys(pposdex.V3_METRICS, 5)
        path = self.write(
            tmp_path / "recomputed.csv",
            [{"timestamp": d["timestamp"], **values} for d in (old, v4)],
        )
        filled = pposdex.with_recomputed([new, v4, old], path)
        assert filled[0] is new
        assert filled[1]["ppos_dex_v3_liveness"] == 7
        assert filled[1].get("ppos_dex_v3_veto") == 5
        assert not pposdex.is_recomputed(filled[1], "ppos_dex_v3_liveness")
        assert pposdex.is_recomputed(filled[1], "ppos_dex_v3_veto")
        assert set(filled[2].get("recomputed", [])) == set(pposdex.V3_METRICS)
        # The published points are left as they are
        assert "recomputed" not in v4

    def test_hhi_and_v2(
        self, tmp_path: Path, make_data_point: Callable[..., PPoSDexData]
    ) -> None:
        first = make_data_point(timestamp="2021-01-16 00:00:00.0")
        before_v2 = make_data_point(timestamp="2021-02-15 00:00:00.0")
        for data in (first, before_v2):
            del data["ppos_dex_v2"]
        del first["ppos_hhi"]
        path = self.write(
            tmp_path / "recomputed.csv",
            [
                {"timestamp": d["timestamp"], "ppos_hhi": 0.1}
                for d in (first, before_v2)
            ],
        )
        filled = pposdex.with_recomputed([before_v2, first], path)
        # The HHI of the first points from the ledger, published since
        assert filled[1].get("ppos_hhi") == 0.1
        assert filled[0].get("ppos_hhi") == 0.02
        # v2 from the ALGO supply, the online stake and the HHI of the point
        assert filled[1].get("ppos_dex_v2") == pytest.approx(0.7 * 0.5 * 0.9)
        assert filled[0].get("ppos_dex_v2") == pytest.approx(0.7 * 0.5 * 0.98)
        assert filled[1].get("recomputed") == ["ppos_hhi", "ppos_dex_v2"]
        assert filled[0].get("recomputed") == ["ppos_dex_v2"]

    def test_points_without_published_ones(
        self, tmp_path: Path, make_data_point: Callable[..., PPoSDexData]
    ) -> None:
        old = make_data_point(timestamp="2022-03-29 00:00:00.0")
        new = make_data_point(timestamp="2023-09-03 00:00:00.0")
        ledger = dict.fromkeys(pposdex.RECOMPUTED_METRICS, 1) | {
            "algo_dynamics": 0.7,
            "ppos_online_stake": 0.5,
            "ppos_hhi": 0.1,
            "round": 7,
            "published": 0,
            "algo_threshold": 1000,
        }
        path = self.write(
            tmp_path / "recomputed.csv",
            [
                ledger | {"timestamp": t}
                for t in ("2022-03-30 00:00:00", "2023-09-04 00:00:00")
            ],
        )
        filled = pposdex.with_recomputed([new, old], path)
        # Within the data points given, newest first
        assert [d["timestamp"] for d in filled] == [
            "2023-09-03 00:00:00.0",
            "2022-03-30 00:00:00",
            "2022-03-29 00:00:00.0",
        ]
        point = filled[1]
        assert point.get("round") == 7
        assert point.get("ppos_dex_v2") == pytest.approx(0.7 * 0.5 * 0.9)
        assert set(point.get("recomputed", [])) == {
            *pposdex.RECOMPUTED_METRICS,
            "ppos_dex_v2",
        }
        # Not published, nor recomputed: the accounts of all the ALGO
        assert math.isnan(pposdex.online_accounts(point))
        assert math.isnan(pposdex.total_accounts(point))
        # Values derived from the point are recomputed when all its metrics are
        assert pposdex.is_recomputed(point, pposdex.evenness)
        assert not pposdex.is_recomputed(filled[0], pposdex.evenness)

    def test_nothing_to_fill(self, tmp_path: Path) -> None:
        assert pposdex.with_recomputed([], tmp_path / "x.csv") == []

    def test_without_the_file(
        self, tmp_path: Path, make_data_point: Callable[..., PPoSDexData]
    ) -> None:
        published = make_data_point()
        before_v2 = make_data_point()
        del before_v2["ppos_dex_v2"]
        filled = pposdex.with_recomputed([published, before_v2], tmp_path / "x.csv")
        assert filled[0] is published
        assert pposdex.is_recomputed(filled[1], "ppos_dex_v2")
