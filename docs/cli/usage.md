# Usage

Ask the PPoS Dex CLI for help:

```text
$ uv run pposdex --help
{{#include help/pposdex.txt}}
```

| Command | Use it to |
| --- | --- |
| [`publish`](publish.md) | Publish a PPoS Dex data point on-chain |
| [`timeseries`](timeseries.md) | Plot the published data points over time |
| [`snapshot`](snapshot.md) | Plot the latest published data point |
| [`export`](export.md) | Export the published data points to `.csv` |
| [`health`](health.md) | Check the Algorand node and Indexer are available |

Each command has its own `--help` too, shown in its page.

All commands use Algorand MainNet by default: select another network with
`--test` or `--localhost` (see [Node Setup](install.md#node-setup)). Use
`--verbose` to show more details (e.g. Indexer request retries and published
transactions), or `--quiet` to show errors only.
