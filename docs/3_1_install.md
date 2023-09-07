# PPoS Dex CLI

---

PPoS Dex CLI provides the following utilities:

1. Publishing PPoS Dex data point;
1. Monitoring PPoS Dex trend (timeseries);
1. Monitoring PPoS Dex latest state (snapshot);
1. Exporting PPoS Dex data to `.csv` for external analysis.

## Install

PPoS Dex uses [Poetry](https://python-poetry.org/docs/#installation) for
dependencies management.

Clone [PPoS Dex](https://github.com/cusma/pposdex) repository, `cd` into it,
and:

```bash
poetry install
```

You are all set!

## Node setup

PPoS Dex interacts both with Algorand Node and an Indexer. You may choose:

1. Your local hosted Node and Indexer (e.g. [AlgoKit](https://github.com/algorandfoundation/algokit-cli));
2. A third party Node and Indexer APIs.

PPoS Dex uses [AlgoNode APIs](https://algonode.io/api/) by default.

If you prefer using your local hosted Node and Indexer (or other API providers),
the following environment variables must be set:

```bash
export ALGOD_SERVER=...
export ALGOD_TOKEN=...
export INDEXER_SERVER=...
export INDEXER_TOKEN=...
```

---
