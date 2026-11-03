import logging
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any, cast

import matplotlib
import pytest
from algosdk import account, mnemonic
from fakes import FakeAlgod, FakeIndexer
from hypothesis import settings

from pposdex.helpers import Account, Json
from pposdex.ppos_dex_data import PPoSDexData

matplotlib.use("Agg")

# Same examples on every run: property tests explore widely but never flake
settings.register_profile("pposdex", derandomize=True, database=None)
settings.load_profile("pposdex")


@pytest.fixture(autouse=True)
def _restore_logger() -> Iterator[None]:
    # The CLI configures the "pposdex" logger: don't leak it into other tests
    logger = logging.getLogger("pposdex")
    state = (logger.handlers[:], logger.level, logger.propagate)
    yield
    logger.handlers, logger.level, logger.propagate = state


@pytest.fixture
def algod() -> FakeAlgod:
    return FakeAlgod()


@pytest.fixture
def indexer(monkeypatch: pytest.MonkeyPatch) -> FakeIndexer:
    monkeypatch.setattr("pposdex.helpers.ATTEMPT_DELAY_SEC", 0)
    return FakeIndexer()


@pytest.fixture
def publisher() -> Account:
    private_key, _ = account.generate_account()
    return Account(private_key=private_key)


@pytest.fixture
def publisher_mnemonic(publisher: Account) -> str:
    return str(mnemonic.from_private_key(publisher.private_key))


@pytest.fixture
def make_holders() -> Callable[[int], list[Json]]:
    def make(n: int) -> list[Json]:
        """Accounts with distinct balances, one in three online"""
        return [
            {
                "address": f"ACCOUNT{i:04}",
                "amount": (i * 7919 % 100_003 + 1) * 10**6,
                "status": "Online" if i % 3 == 0 else "Offline",
            }
            for i in range(n)
        ]

    return make


@pytest.fixture
def make_data_point() -> Callable[..., PPoSDexData]:
    def make(**overrides: Any) -> PPoSDexData:
        data: dict[str, Any] = {
            "algo_threshold": 1000,
            "accounts": 42,
            "algo_dynamics": 0.7,
            "ppos_online_stake": 0.5,
            "ppos_online_accounts": 0.1,
            "algo_hhi": 0.01,
            "ppos_gini": 0.9,
            "ppos_theil_l": 3.2,
            "ppos_theil_t": 2.1,
            "ppos_hhi": 0.02,
            "ppos_dex": 0.03,
            "ppos_dex_v2": 0.3,
            "timestamp": "2026-11-03 00:00:00.000000",
        }
        data.update(overrides)
        return cast(PPoSDexData, data)

    return make


@pytest.fixture
def images(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Run in a temporary folder where plots can be saved"""
    monkeypatch.chdir(tmp_path)
    for kind in ("timeseries", "snapshot"):
        (tmp_path / "docs" / "images" / kind).mkdir(parents=True)
    return tmp_path / "docs" / "images"
