import pytest

from pposdex import networks
from pposdex.networks import Network


@pytest.mark.parametrize(
    "network",
    [networks.MAINNET, networks.TESTNET, networks.LOCALNET],
    ids=["mainnet", "testnet", "localnet"],
)
def test_clients(network: Network) -> None:
    algod = networks.get_algod_client(network)
    indexer = networks.get_indexer_client(network)
    assert (algod.algod_address, algod.algod_token) == (
        network.algod_url,
        network.token,
    )
    assert (indexer.indexer_address, indexer.indexer_token) == (
        network.indexer_url,
        network.token,
    )
