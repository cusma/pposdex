# PPoS Dex CLI

PPoS Dex CLI provides the following utilities:

1. Publishing PPoS Dex data point;
1. Monitoring PPoS Dex trend (timeseries);
1. Monitoring PPoS Dex latest state (snapshot);
1. Exporting PPoS Dex data to `.csv` for external analysis.

## Install

PPoS Dex uses [uv](https://docs.astral.sh/uv/getting-started/installation/)
for Python and dependencies management.

Clone [PPoS Dex](https://github.com/cusma/pposdex) repository, `cd` into it,
and:

```bash
uv sync
```

You are all set!

## Node setup

PPoS Dex interacts both with Algorand Node and an Indexer. Every command
accepts a network option:

| Option | Network | Node and Indexer |
| --- | --- | --- |
| _(none)_ | MainNet | [Nodely APIs](https://nodely.io/docs/free/start) |
| `-t`, `--test` | TestNet | [Nodely APIs](https://nodely.io/docs/free/start) |
| `-l`, `--localhost` | LocalNet | [AlgoKit](https://github.com/algorandfoundation/algokit-cli) LocalNet on `localhost` |

To use AlgoKit LocalNet, start it before running PPoS Dex:

```bash
uvx algokit localnet start
uv run pposdex health --localhost
```
