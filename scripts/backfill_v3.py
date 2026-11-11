"""
PPoS Dex v3 backfill: the v3 coefficients of the data points published before
them, recomputed from the ledger state at the round of each point.

Run `uv run python scripts/backfill_v3.py` to update
`./data/ppos_dex_v3_backfill.csv`.
The past ledger state comes from Nodely Time Travel, cached in `./.backfill`:
a run resumes where the last one stopped, and calls the API only for what is
not cached yet.
"""

import base64
import csv
import json
import logging
import sqlite3
import threading
import time
import urllib.error
import urllib.request
from collections import defaultdict
from collections.abc import Iterable, Iterator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import msgpack

from pposdex import inequality_idx as idx
from pposdex.cli import DEFAULT_PUBLISHER
from pposdex.helpers import Json
from pposdex.ppos_dex_data import (
    RECOMPUTED_PATH,
    V3_SHARES,
    InvalidDataError,
    PPoSDexData,
    online_accounts,
    operator_stakes,
    validate,
)

logger = logging.getLogger(__name__)

ALGOD_URL = "https://mainnet-api.4160.nodely.dev"
INDEXER_URL = "https://mainnet-idx.4160.nodely.dev"
USER_AGENT = "pposdex-backfill (+https://github.com/cusma/pposdex)"
TIMEOUT_SEC = 60
ATTEMPTS = 6
# Polite to the free tier: 10 concurrent calls at most, 60 requests per second
WORKERS = 8
MAX_RATE = 20.0
# Stop before the daily free quota of 200k requests per IP
DAILY_BUDGET = 180_000

CACHE_DIR = Path("./.backfill")
OUTPUT = RECOMPUTED_PATH
MICROALGOS = 10**6
FOREVER = 2**63

V3_FIELDS = [
    f"ppos_dex_v3_{name}{suffix}" for name in V3_SHARES for suffix in ("", "_operators")
]
COLUMNS = [
    "timestamp",
    "round",
    *V3_FIELDS,
    "online_accounts",
    # Checks against the ledger and the published data point
    "online_stake_gap",
    "online_accounts_diff",
    "ppos_gini_diff",
    "ppos_hhi_diff",
    "ppos_dex_v3_liveness_published",
]


class QuotaExceededError(Exception):
    """The daily free quota is used up: run again after 00:00 UTC"""


class Client:
    """GET JSON from Nodely, rate limited, retrying, and counting the calls"""

    def __init__(self, cache: "Cache") -> None:
        self.cache = cache
        self.lock = threading.Lock()
        self.next_call = 0.0

    def _wait_turn(self) -> None:
        with self.lock:
            now = time.monotonic()
            wait = self.next_call - now
            self.next_call = max(now, self.next_call) + 1 / MAX_RATE
        if wait > 0:
            time.sleep(wait)

    def get(self, url: str) -> Json | None:
        """The JSON response, or None when not found"""
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        for attempt in range(ATTEMPTS):
            if self.cache.count_call() > DAILY_BUDGET:
                raise QuotaExceededError(f"{DAILY_BUDGET:,} calls today")
            self._wait_turn()
            try:
                with urllib.request.urlopen(request, timeout=TIMEOUT_SEC) as response:
                    result: Json = json.load(response)
                    return result
            except urllib.error.HTTPError as err:
                with err:
                    body = err.read().decode(errors="replace")
                if err.code == 404:
                    return None
                if err.code == 403:
                    raise QuotaExceededError(body) from err
                logger.debug("%s on %s, attempt %d", err.code, url, attempt + 1)
            except (urllib.error.URLError, TimeoutError) as err:
                logger.debug("%s on %s, attempt %d", err, url, attempt + 1)
            time.sleep(2**attempt)
        raise ConnectionError(f"No answer from {url}")


@dataclass(frozen=True)
class State:
    """What PPoS Dex needs of an account at a round"""

    online: bool
    amount: int
    auth_addr: str | None
    vote_first: int | None
    vote_last: int | None

    @classmethod
    def from_account(cls, account: Json) -> "State":
        keys = account.get("participation") or {}
        return cls(
            online=account.get("status") == "Online",
            amount=account["amount"],
            auth_addr=account.get("auth-addr"),
            vote_first=keys.get("vote-first-valid"),
            vote_last=keys.get("vote-last-valid"),
        )

    def as_account(self, address: str) -> Json:
        """As the Indexer returns accounts, for `operator_stakes`"""
        account: Json = {"address": address, "amount": self.amount}
        if self.auth_addr:
            account["auth-addr"] = self.auth_addr
        if self.vote_first is not None:
            account["participation"] = {
                "vote-first-valid": self.vote_first,
                "vote-last-valid": self.vote_last,
            }
        return account


class Cache:
    """SQLite cache of the past ledger state, the key registrations and the
    calls made each UTC day"""

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.lock = threading.Lock()
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS states (
                round INTEGER, address TEXT, online INTEGER, amount INTEGER,
                auth_addr TEXT, vote_first INTEGER, vote_last INTEGER,
                PRIMARY KEY (round, address)
            ) WITHOUT ROWID;
            CREATE TABLE IF NOT EXISTS supply (
                round INTEGER PRIMARY KEY, online_money INTEGER
            );
            CREATE TABLE IF NOT EXISTS keyregs (
                round INTEGER, intra INTEGER, address TEXT, online INTEGER,
                PRIMARY KEY (round, intra, address)
            ) WITHOUT ROWID;
            CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
            """
        )

    def close(self) -> None:
        self.db.close()

    def meta(self, key: str) -> str | None:
        with self.lock:
            row = self.db.execute(
                "SELECT value FROM meta WHERE key = ?", (key,)
            ).fetchone()
        return None if row is None else str(row[0])

    def set_meta(self, key: str, value: str) -> None:
        with self.lock, self.db:
            self.db.execute("REPLACE INTO meta VALUES (?, ?)", (key, value))

    def count_call(self) -> int:
        """Count a call made today, and return today's calls"""
        key = f"calls:{datetime.now(UTC).date().isoformat()}"
        with self.lock, self.db:
            self.db.execute(
                "INSERT INTO meta VALUES (?, '1') "
                "ON CONFLICT (key) DO UPDATE SET value = value + 1",
                (key,),
            )
            row = self.db.execute(
                "SELECT value FROM meta WHERE key = ?", (key,)
            ).fetchone()
        return int(row[0])

    def states(self, round_: int) -> dict[str, State]:
        with self.lock:
            rows = self.db.execute(
                "SELECT address, online, amount, auth_addr, vote_first, vote_last "
                "FROM states WHERE round = ?",
                (round_,),
            ).fetchall()
        return {r[0]: State(bool(r[1]), *r[2:]) for r in rows}

    def add_states(self, round_: int, states: dict[str, State]) -> None:
        with self.lock, self.db:
            self.db.executemany(
                "REPLACE INTO states VALUES (?, ?, ?, ?, ?, ?, ?)",
                [
                    (
                        round_,
                        a,
                        int(s.online),
                        s.amount,
                        s.auth_addr,
                        s.vote_first,
                        s.vote_last,
                    )
                    for a, s in states.items()
                ],
            )

    def supply(self, round_: int) -> tuple[bool, int | None]:
        """Whether the online money at the round is cached, and its value"""
        with self.lock:
            row = self.db.execute(
                "SELECT online_money FROM supply WHERE round = ?", (round_,)
            ).fetchone()
        return (False, None) if row is None else (True, row[0])

    def add_supply(self, round_: int, online_money: int | None) -> None:
        with self.lock, self.db:
            self.db.execute("REPLACE INTO supply VALUES (?, ?)", (round_, online_money))

    def keyregs(self) -> list[tuple[int, str, bool]]:
        with self.lock:
            rows = self.db.execute(
                "SELECT round, address, online FROM keyregs ORDER BY round, intra"
            ).fetchall()
        return [(r, a, bool(o)) for r, a, o in rows]

    def add_keyregs(self, keyregs: list[tuple[int, int, str, bool]]) -> None:
        with self.lock, self.db:
            self.db.executemany(
                "REPLACE INTO keyregs VALUES (?, ?, ?, ?)",
                [(r, i, a, int(o)) for r, i, a, o in keyregs],
            )


def _keyregs_of(txn: Json) -> Iterator[tuple[str, bool]]:
    """The key registrations of a transaction and of its inner ones: their
    sender, and whether they register online"""
    keyreg = txn.get("keyreg-transaction")
    if txn.get("tx-type") == "keyreg" and keyreg is not None:
        online = bool(keyreg.get("vote-participation-key")) and not keyreg.get(
            "non-participation"
        )
        yield txn["sender"], online
    for inner in txn.get("inner-txns", []):
        yield from _keyregs_of(inner)


def fetch_keyregs(client: Client, cache: Cache) -> None:
    """Cache every key registration from genesis, resuming the last fetch"""
    token = cache.meta("keyregs:next") or ""
    pages = 0
    while True:
        url = f"{INDEXER_URL}/v2/transactions?tx-type=keyreg&limit=1000"
        page = client.get(url + (f"&next={token}" if token else ""))
        assert page is not None
        txns = page.get("transactions", [])
        if not txns:
            break
        cache.add_keyregs(
            [
                (txn["confirmed-round"], txn.get("intra-round-offset", 0), a, online)
                for txn in txns
                for a, online in _keyregs_of(txn)
            ]
        )
        token = page["next-token"]
        cache.set_meta("keyregs:next", token)
        pages += 1
        if pages % 50 == 0:
            logger.info("Key registrations: %d pages", pages)


def genesis_online(client: Client) -> list[str]:
    """Accounts online from genesis, without a key registration"""
    genesis = client.get(f"{ALGOD_URL}/genesis")
    assert genesis is not None
    return [a["addr"] for a in genesis["alloc"] if a.get("state", {}).get("onl") == 1]


@dataclass(frozen=True)
class Point:
    round: int
    data: PPoSDexData


def published_points(client: Client, publisher: str, threshold: int) -> list[Point]:
    """The published data points, oldest first, with the round of their note"""
    points: list[Point] = []
    token = ""
    while True:
        url = f"{INDEXER_URL}/v2/accounts/{publisher}/transactions?limit=1000"
        page = client.get(url + (f"&next={token}" if token else ""))
        assert page is not None
        txns = page.get("transactions", [])
        if not txns:
            break
        for txn in txns:
            try:
                data = validate(msgpack.unpackb(base64.b64decode(txn["note"])))
            except (KeyError, InvalidDataError, ValueError, msgpack.ExtraData):
                continue
            if data["algo_threshold"] == threshold:
                points.append(Point(txn["confirmed-round"], data))
        token = page["next-token"]
    return sorted(points, key=lambda p: p.round)


class Candidates:
    """The accounts that may be online at a round: only a key registration
    takes an account online, so one seen offline stays so until its next"""

    def __init__(self, keyregs: Iterable[tuple[int, str, bool]], genesis: list[str]):
        self.onlines: dict[str, list[int]] = defaultdict(list)
        for round_, address, online in keyregs:
            if online:
                self.onlines[address].append(round_)
        for address in genesis:
            self.onlines[address].insert(0, 0)
        # Since when each account is known offline
        self.offline_since: dict[str, int] = {}

    def at(self, round_: int) -> list[str]:
        candidates = []
        for address, onlines in self.onlines.items():
            if onlines[0] > round_:
                continue
            since = self.offline_since.get(address)
            if since is not None and not any(since < r <= round_ for r in onlines):
                continue
            candidates.append(address)
        return candidates

    def observe(self, round_: int, states: dict[str, State]) -> None:
        for address, state in states.items():
            if state.online:
                self.offline_since.pop(address, None)
            else:
                self.offline_since[address] = round_


def fetch_round(
    client: Client, cache: Cache, round_: int, addresses: list[str]
) -> dict[str, State]:
    """The state of the addresses at the round, from the cache or the API"""
    states = cache.states(round_)
    missing = [a for a in addresses if a not in states]

    def fetch(address: str) -> tuple[str, State]:
        account = client.get(
            f"{ALGOD_URL}/v2/accounts/{address}?round={round_}&exclude=all"
        )
        if account is None:  # Not created yet
            return address, State(False, 0, None, None, None)
        return address, State.from_account(account)

    if missing:
        with ThreadPoolExecutor(WORKERS) as pool:
            fetched = dict(pool.map(fetch, missing))
        cache.add_states(round_, fetched)
        states |= fetched
    if not cache.supply(round_)[0]:
        supply = client.get(f"{ALGOD_URL}/v2/ledger/supply?round={round_}")
        cache.add_supply(round_, None if supply is None else supply["online-money"])
    return {a: states[a] for a in addresses}


def rebuild(point: Point, states: dict[str, State], online_money: int | None) -> Json:
    """The v3 coefficients at the point, and their checks"""
    data = point.data
    threshold = data["algo_threshold"] * MICROALGOS
    online = {a: s for a, s in states.items() if s.online}
    accounts = [s.as_account(a) for a, s in online.items() if s.amount > threshold]
    stakes = sorted(account["amount"] for account in accounts)
    operators = sorted(operator_stakes(accounts))
    row: Json = {
        "timestamp": data["timestamp"],
        "round": point.round,
        "online_accounts": len(stakes),
    }
    for name, share in V3_SHARES.items():
        row[f"ppos_dex_v3_{name}"] = idx.nakamoto_coefficient(stakes, share)
        row[f"ppos_dex_v3_{name}_operators"] = idx.nakamoto_coefficient(
            operators, share
        )
    total = sum(s.amount for s in online.values())
    row["online_stake_gap"] = f"{1 - total / online_money:.2e}" if online_money else ""
    row["online_accounts_diff"] = round(len(stakes) - online_accounts(data))
    row["ppos_gini_diff"] = f"{idx.gini(stakes) - data['ppos_gini']:.2e}"
    hhi = data.get("ppos_hhi")
    row["ppos_hhi_diff"] = (
        "" if hhi is None else f"{idx.herfindahl_hirschman(stakes) - hhi:.2e}"
    )
    row["ppos_dex_v3_liveness_published"] = data.get("ppos_dex_v3_liveness", "")
    return row


def written_rounds(path: Path) -> set[int]:
    if not path.exists():
        return set()
    with path.open(encoding="utf8") as f:
        return {int(row["round"]) for row in csv.DictReader(f)}


def run(
    publisher: str,
    threshold: int = 1000,
    cache_path: Path = CACHE_DIR / "cache.sqlite",
    output: Path = OUTPUT,
    max_points: int | None = None,
) -> None:
    """Rebuild the published points not written yet, at most `max_points`"""
    cache = Cache(cache_path)
    try:
        client = Client(cache)
        if cache.meta("keyregs:done") is None:
            fetch_keyregs(client, cache)
            cache.set_meta("keyregs:done", "1")
        candidates = Candidates(cache.keyregs(), genesis_online(client))
        points = published_points(client, publisher, threshold)
        done = written_rounds(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        new_file = not output.exists()
        with output.open("a", encoding="utf8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS)
            if new_file:
                writer.writeheader()
            for n, point in enumerate(points, 1):
                new = point.round not in done
                if new and max_points is not None:
                    if max_points <= 0:
                        break
                    max_points -= 1
                # Points already written are read again from the cache: the
                # candidates of the next ones depend on them
                states = fetch_round(
                    client, cache, point.round, candidates.at(point.round)
                )
                candidates.observe(point.round, states)
                if not new:
                    continue
                _, online_money = cache.supply(point.round)
                writer.writerow(rebuild(point, states, online_money))
                f.flush()
                logger.info(
                    "%d/%d round %d: %d candidates",
                    n,
                    len(points),
                    point.round,
                    len(states),
                )

    finally:
        cache.close()


def main() -> None:  # pragma: no cover
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    try:
        run(DEFAULT_PUBLISHER)
    except QuotaExceededError as err:
        logger.warning("Stopping, run again after 00:00 UTC: %s", err)


if __name__ == "__main__":
    main()
