# Usage

---

Intreacting with PPoS Dex CLI is pretty easy, just ask for help (each command
has its own `--help` too):

```bash
$ uv run pposdex --help

usage: pposdex [-h] <command> ...

Algorand PPoS Decentralization Index.

positional arguments:
  <command>
    publish     Publish PPoS Dex data. Requires ALGO_MNEMONIC environment variable.
    timeseries  Plot PPoS Dex timeseries.
    snapshot    Plot latest PPoS Dex data point.
    export      Export PPoS Dex data to `.csv`.
    health      Check Algod and Indexer status.

options:
  -h, --help    show this help message and exit
```

Use the `health` command to check Algorand Nods and Indexer availability:

```bash
uv run pposdex health [--localhost | --test]
```

---
