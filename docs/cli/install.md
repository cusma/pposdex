# Install

The PPoS Dex CLI publishes PPoS Dex data points on-chain, plots their trend
(timeseries) and latest state (snapshot), and exports them to `.csv` for your
own analysis.

PPoS Dex uses [uv](https://docs.astral.sh/uv/getting-started/installation/) to
manage Python and its dependencies. Clone the
[PPoS Dex](https://github.com/cusma/pposdex) repository, `cd` into it, and run:

```bash
uv sync
```

You are all set!

## Node Setup

PPoS Dex reads the blockchain from an Algorand node and an Indexer. Every
command accepts a network option:

| Option | Network | Node and Indexer |
| --- | --- | --- |
| _(none)_ | MainNet | [Nodely APIs](https://nodely.io/docs/free/start) |
| `-t`, `--test` | TestNet | [Nodely APIs](https://nodely.io/docs/free/start) |
| `-l`, `--localhost` | LocalNet | [AlgoKit](https://github.com/algorandfoundation/algokit-cli) LocalNet on `localhost` |

To use AlgoKit LocalNet, start it before running PPoS Dex, and check it is up
with the [`health`](health.md) command:

```bash
uvx algokit localnet start
uv run pposdex health --localhost
```
