import pytest

from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algokit_utils import (
    Account,
    get_algod_client,
    get_default_localnet_config,
    get_indexer_client,
    get_localnet_default_account,
)


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
    return get_algod_client(get_default_localnet_config("algod"))


@pytest.fixture(scope="session")
def indexer_client() -> IndexerClient:
    return get_indexer_client(get_default_localnet_config("indexer"))


@pytest.fixture(scope="session")
def faucet(algod_client) -> Account:
    return get_localnet_default_account(algod_client)
