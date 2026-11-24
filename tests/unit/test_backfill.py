import base64
import csv
import io
import json
import urllib.error
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import backfill_v3 as backfill
import msgpack
import pytest
from backfill_v3 import Cache, Candidates, Client, State

from pposdex.helpers import Json
from pposdex.ppos_dex_data import PPoSDexData

ALGO = 10**6
URL = "https://nodely.test/v2/status"


def account(amount: int, online: bool = True, extra: Json | None = None) -> Json:
    status = "Online" if online else "Offline"
    return {"amount": amount * ALGO, "status": status} | (extra or {})


@pytest.fixture
def cache(tmp_path: Path) -> Iterator[Cache]:
    cache = Cache(tmp_path / "cache.sqlite")
    yield cache
    cache.close()


class TestKeyregs:
    def test_online_and_offline(self) -> None:
        online = {
            "tx-type": "keyreg",
            "sender": "A",
            "keyreg-transaction": {"vote-participation-key": "K"},
        }
        offline = {"tx-type": "keyreg", "sender": "B", "keyreg-transaction": {}}
        assert list(backfill._keyregs_of(online)) == [("A", True)]
        assert list(backfill._keyregs_of(offline)) == [("B", False)]

    def test_non_participation_is_offline(self) -> None:
        txn = {
            "tx-type": "keyreg",
            "sender": "A",
            "keyreg-transaction": {
                "vote-participation-key": "K",
                "non-participation": True,
            },
        }
        assert list(backfill._keyregs_of(txn)) == [("A", False)]

    def test_inner_ones(self) -> None:
        # Staking pools register their keys from an app call
        txn = {
            "tx-type": "appl",
            "sender": "USER",
            "inner-txns": [
                {
                    "tx-type": "keyreg",
                    "sender": "POOL",
                    "keyreg-transaction": {"vote-participation-key": "K"},
                }
            ],
        }
        assert list(backfill._keyregs_of(txn)) == [("POOL", True)]


class TestCandidates:
    def test_online_from_their_first_registration(self) -> None:
        candidates = Candidates([(10, "A", True), (20, "B", True)], ["G"])
        assert sorted(candidates.at(15)) == ["A", "G"]

    def test_offline_until_the_next_registration(self) -> None:
        candidates = Candidates([(10, "A", True), (30, "A", True)], [])
        candidates.observe(15, {"A": State(False, 0, None, None, None)})
        assert candidates.at(20) == []
        assert candidates.at(30) == ["A"]
        candidates.observe(30, {"A": State(True, 5, None, None, None)})
        assert candidates.at(40) == ["A"]


class TestState:
    def test_round_trip(self) -> None:
        state = State.from_account(
            account(
                5,
                extra={
                    "auth-addr": "AUTH",
                    "participation": {"vote-first-valid": 1, "vote-last-valid": 9},
                },
            )
        )
        assert state == State(True, 5 * ALGO, "AUTH", 1, 9)
        assert state.as_account("A") == {
            "address": "A",
            "amount": 5 * ALGO,
            "auth-addr": "AUTH",
            "participation": {"vote-first-valid": 1, "vote-last-valid": 9},
        }

    def test_without_keys(self) -> None:
        state = State.from_account(account(5, online=False))
        assert state.as_account("A") == {"address": "A", "amount": 5 * ALGO}


class TestCache:
    def test_states(self, cache: Cache) -> None:
        cache.add_states(7, {"A": State(True, 1, None, 2, 3)})
        assert cache.states(7) == {"A": State(True, 1, None, 2, 3)}
        assert cache.states(8) == {}

    def test_supply(self, cache: Cache) -> None:
        assert cache.supply(7) == (False, None)
        cache.add_supply(7, None)
        assert cache.supply(7) == (True, None)

    def test_counts_the_calls(self, cache: Cache) -> None:
        assert [cache.count_call() for _ in range(3)] == [1, 2, 3]


class TestClient:
    @pytest.fixture
    def client(
        self, cache: Cache, monkeypatch: pytest.MonkeyPatch
    ) -> Callable[[list[Any]], Client]:
        monkeypatch.setattr("backfill_v3.time.sleep", lambda _: None)

        def make(answers: list[Any]) -> Client:
            def urlopen(request: Any, timeout: float) -> io.StringIO:
                answer = answers.pop(0)
                if isinstance(answer, Exception):
                    raise answer
                return io.StringIO(json.dumps(answer))

            monkeypatch.setattr("backfill_v3.urllib.request.urlopen", urlopen)
            return Client(cache)

        return make

    @staticmethod
    def http_error(code: int) -> urllib.error.HTTPError:
        return urllib.error.HTTPError(URL, code, "msg", {}, io.BytesIO(b"body"))  # type: ignore[arg-type]

    def test_retries(self, client: Callable[[list[Any]], Client]) -> None:
        answers = [self.http_error(503), urllib.error.URLError("down"), {"ok": 1}]
        assert client(answers).get(URL) == {"ok": 1}

    def test_not_found(self, client: Callable[[list[Any]], Client]) -> None:
        assert client([self.http_error(404)]).get(URL) is None

    def test_quota(self, client: Callable[[list[Any]], Client]) -> None:
        with pytest.raises(backfill.QuotaExceededError):
            client([self.http_error(403)]).get(URL)

    def test_daily_budget(
        self, client: Callable[[list[Any]], Client], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(backfill, "DAILY_BUDGET", 1)
        c = client([{"ok": 1}])
        assert c.get(URL) == {"ok": 1}
        with pytest.raises(backfill.QuotaExceededError):
            c.get(URL)

    def test_gives_up(self, client: Callable[[list[Any]], Client]) -> None:
        with pytest.raises(ConnectionError):
            client([TimeoutError()] * backfill.ATTEMPTS).get(URL)


class FakeNodely:
    """Answers the backfill calls from memory: accounts by round"""

    def __init__(self, notes: list[tuple[int, bytes]]) -> None:
        self.notes = notes
        self.keyregs = [
            {
                "tx-type": "keyreg",
                "sender": address,
                "confirmed-round": 1,
                "keyreg-transaction": {"vote-participation-key": "K"},
            }
            for address in ("BIG", "SMALL", "GONE")
        ]
        self.accounts: dict[int, dict[str, Json]] = {
            100: {
                "BIG": account(6000),
                "SMALL": account(2000),
                "GONE": account(2000, online=False),
            },
            200: {"BIG": account(5000), "SMALL": account(5000)},
        }
        self.calls: list[str] = []

    def get(self, url: str) -> Json | None:
        self.calls.append(url)
        path = url.split("4160.nodely.dev", 1)[1]
        if path.startswith("/v2/transactions?tx-type=keyreg"):
            txns = [] if "next=" in path else self.keyregs
            return {"transactions": txns, "next-token": "1"}
        if path == "/genesis":
            return {"alloc": [{"addr": "GENESIS", "state": {"onl": 1}}]}
        if "/transactions?" in path:
            return self.published(path)
        return self.ledger(path)

    def published(self, path: str) -> Json:
        if "next=" in path:
            return {"transactions": []}
        txns = [
            {"confirmed-round": r, "note": base64.b64encode(n).decode()}
            for r, n in self.notes
        ]
        # A transaction without a note is skipped
        return {"transactions": [*txns, {"confirmed-round": 1}], "next-token": "1"}

    def ledger(self, path: str) -> Json | None:
        round_ = int(path.split("round=")[1].split("&", maxsplit=1)[0])
        accounts = self.accounts[round_]
        if path.startswith("/v2/ledger/supply"):
            if round_ == 200:  # Not recorded
                return None
            online = [a for a in accounts.values() if a["status"] == "Online"]
            return {"online-money": sum(a["amount"] for a in online)}
        return accounts.get(path.split("/v2/accounts/")[1].split("?", maxsplit=1)[0])


def test_run(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    make_data_point: Callable[..., PPoSDexData],
) -> None:
    notes = [
        (
            r,
            msgpack.packb(
                make_data_point(accounts=20, ppos_online_accounts=0.1, **extra)
            ),
        )
        for r, extra in ((200, {"ppos_dex_v3_liveness": 1}), (100, {}))
    ]
    fake = FakeNodely(notes)
    monkeypatch.setattr(Client, "get", lambda self, url: fake.get(url))
    output = tmp_path / "backfill.csv"
    cache = tmp_path / "cache.sqlite"

    backfill.run("PUBLISHER", cache_path=cache, output=output, max_points=1)
    with output.open() as f:
        assert [row["round"] for row in csv.DictReader(f)] == ["100"]

    backfill.run("PUBLISHER", cache_path=cache, output=output)
    with output.open() as f:
        rows = list(csv.DictReader(f))
    assert [row["round"] for row in rows] == ["100", "200"]
    first, second = rows
    # 6000 and 2000 ALGO online: the larger alone holds more than 1/3
    assert first["ppos_dex_v3_nakamoto"] == "1"
    assert first["ppos_dex_v3_upgrade"] == "2"
    assert first["online_accounts"] == "2"
    assert first["online_accounts_diff"] == "0"
    assert float(first["online_stake_gap"]) == 0
    # GONE is offline at 100: not asked again at 200
    assert not any("GONE?round=200" in c for c in fake.calls)
    assert second["ppos_dex_v3_liveness_published"] == "1"
    assert second["online_stake_gap"] == ""
    # A run with all points written asks only for what is not cached
    calls = len(fake.calls)
    backfill.run("PUBLISHER", cache_path=cache, output=output)
    assert all(
        "/v2/accounts/" not in c or "transactions" in c for c in fake.calls[calls:]
    )
