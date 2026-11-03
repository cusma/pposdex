# Usage

Interacting with PPoS Dex CLI is pretty easy, just ask for help:

```text
$ uv run pposdex --help
{{#include help/pposdex.txt}}
```

Each command has its own `--help` too, see the next pages.

All commands use Algorand MainNet by default, select another network with
`--test` or `--localhost` (see [Node setup](install.md#node-setup)). Use
`--verbose` to show more details (e.g. Indexer requests retries and published
transactions), or `--quiet` to show errors only.

## Health

Use the `health` command to check Algorand Nodes and Indexer availability:

```text
$ uv run pposdex health --help
{{#include help/health.txt}}
```
