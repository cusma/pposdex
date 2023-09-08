# Usage

---

Intreacting with PPoS Dex CLI is pretty easy, just ask for help:

```bash
$ poetry run python3 ppos_dex.py --help

Algorand PPoS Decentralization Index.

Usage:
  ppos_dex.py publish [--algo-threshold=<a>] [--localhost | --test]
  ppos_dex.py timeseries [--publisher=<p>] [--algo-threshold=<a>] [--start-block=<s>] [--end-block=<e>] [--localhost | --test] [--save]
  ppos_dex.py snapshot [--publisher=<p>] [--algo-threshold=<a>] [--start-block=<s>] [--end-block=<e>] [--localhost | --test] [--save]
  ppos_dex.py export [--publisher=<p>] [--algo-threshold=<a>] [--start-block=<s>] [--end-block=<e>] [--localhost | --test]
  ppos_dex.py health [--localhost | --test]
  ppos_dex.py [--help]

Commands:
  publish     Publish PPoS Dex data. Requires ALGO_MNEMONIC environment variable.
  timeseries  Plot PPoS Dex timeseries.
  snapshot    Plot latest PPoS Dex data point.
  export      Export PPoS Dex data to `.csv`.
  health      Check Algod and Indexer status.

Options:
  -a, --algo-threshold=<a>  [default: 1000]
  -p, --publisher=<p>       [default: WIPE4JSUWLXKZZK6GJ6VI32PX6ZWPKBRH5YFRJCHWOVC73P5RI4DGUQUWQ]
  -s, --start-block=<s>     [default: 11476070]
  -e, --end-block=<e>
  -l, --localhost
  -t, --test
  -h, --help
```

Use the `health` command to check Algorand Nods and Indexer availability:

```bash
poetry run ppos_dex.py health [--localhost | --test]
```

---
