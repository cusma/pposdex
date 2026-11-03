"""
Algorand networks and API clients
"""

from dataclasses import dataclass

from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

LOCALNET_TOKEN = "a" * 64


@dataclass(frozen=True)
class Network:
    algod_url: str
    indexer_url: str
    token: str = ""


MAINNET = Network(
    algod_url="https://mainnet-api.algonode.cloud",
    indexer_url="https://mainnet-idx.algonode.cloud",
)
TESTNET = Network(
    algod_url="https://testnet-api.algonode.cloud",
    indexer_url="https://testnet-idx.algonode.cloud",
)
LOCALNET = Network(
    algod_url="http://localhost:4001",
    indexer_url="http://localhost:8980",
    token=LOCALNET_TOKEN,
)


def get_algod_client(network: Network) -> AlgodClient:
    return AlgodClient(network.token, network.algod_url)


def get_indexer_client(network: Network) -> IndexerClient:
    return IndexerClient(network.token, network.indexer_url)
