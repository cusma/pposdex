# PPoS Dex CLI

## Install

PPoS Dex uses Poetry for dependencies management.

```shell
poetry install
```

## Node setup

PPoS Dex interacts with Algorand blockchain both thorugh a Node and an Indexer.
You may want to choose:

1. Your local hosted Node and Indexer (see [AlgoKit](https://github.com/algorandfoundation/algokit-cli))
2. A third party Node and Indexer APIs

PPoS Dex uses AlgoNode APIs by default.

If you prefer using your local hosted Node and Indexer or other API providers,
the following environment variables must be set:

```shell
export ALGOD_SERVER=...
export ALGOD_TOKEN=...
export INDEXER_SERVER=...
export INDEXER_TOKEN=...
```
