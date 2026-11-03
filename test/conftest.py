import time
from collections.abc import Callable

import pytest
from algosdk.kmd import KMDClient
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from pposdex.helpers import Account
from pposdex.networks import (
    LOCALNET,
    LOCALNET_TOKEN,
    get_algod_client,
    get_indexer_client,
)

LOCALNET_KMD_URL = "http://localhost:4002"
LOCALNET_WALLET = "unencrypted-default-wallet"
FAUCET_MIN_BALANCE = 1_000_000_000


@pytest.fixture(scope="session")
def small_equal_distribution() -> list[float]:
    return [0.20] * 5


@pytest.fixture(scope="session")
def large_equal_distribution() -> list[float]:
    return [0.01] * 100


@pytest.fixture(scope="session")
def inequal_distribution() -> list[float]:
    return [0.15] * 6 + [0.01] * 10


@pytest.fixture(scope="session")
def very_inequal_distribution() -> list[float]:
    return [0.80] + [0.02] * 5 + [0.01] * 10


@pytest.fixture(scope="session")
def low_end_inequal_distribution() -> list[float]:
    return [1.0] + [1000.0] * 99


@pytest.fixture(scope="session")
def high_end_inequal_distribution() -> list[float]:
    return [1.0] * 99 + [1000.0]


@pytest.fixture(scope="session")
def algod_client() -> AlgodClient:
    return get_algod_client(LOCALNET)


@pytest.fixture(scope="session")
def indexer_client() -> IndexerClient:
    return get_indexer_client(LOCALNET)


@pytest.fixture(scope="session")
def faucet(algod_client: AlgodClient) -> Account:
    # LocalNet genesis accounts live in the default KMD wallet: pick a funded one
    kmd = KMDClient(LOCALNET_TOKEN, LOCALNET_KMD_URL)
    wallet_id = next(
        w["id"] for w in kmd.list_wallets() if w["name"] == LOCALNET_WALLET
    )
    handle = kmd.init_wallet_handle(wallet_id, "")
    try:
        for address in kmd.list_keys(handle):
            info = algod_client.account_info(address)
            assert isinstance(info, dict)
            if info["status"] != "Offline" and info["amount"] > FAUCET_MIN_BALANCE:
                return Account(private_key=kmd.export_key(handle, "", address))
    finally:
        kmd.release_wallet_handle(handle)
    raise RuntimeError("No funded account found in LocalNet default wallet")


@pytest.fixture(scope="session")
def wait_for_indexer(indexer_client) -> Callable[[int], None]:
    def wait(confirmed_round: int, timeout_sec: float = 30) -> None:
        # Algod confirms a transaction before the Indexer has caught up to its round
        deadline = time.monotonic() + timeout_sec
        while indexer_client.health()["round"] < confirmed_round:
            if time.monotonic() > deadline:
                raise TimeoutError(f"Indexer did not reach round {confirmed_round}")
            time.sleep(0.5)

    return wait
