# Usage

Intreacting with PPoS Dex from your CLI is pretty easy, just ask for help:

**Input**

```shell
python3 ppos_dex.py --help
```

**Output**

```shell
Algorand PPoS Decentralization Index.

Usage:
  ppos_dex.py publish [--algo-threshold=<t>] [--localhost]
  ppos_dex.py plot [--publisher=<p>] [--algo-threshold=<t>] [--start-block=<s>] [--end-block=<e>] [--localhost]
  ppos_dex.py snapshot [--publisher=<p>] [--algo-threshold=<t>] [--start-block=<s>] [--localhost]
  ppos_dex.py export [--publisher=<p>] [--algo-threshold=<t>] [--start-block=<s>] [--end-block=<e>] [--localhost]
  ppos_dex.py health [--localhost]
  ppos_dex.py [--help]

Commands:
  publish   Publish PPoS Dex data. Requires ALGO_MNEMONIC environment variable.
  plot      Plot PPoS Dex timeseries.
  snapshot  Plot latest PPoS Dex data point.
  export    Export PPoS Dex data to ".csv".
  health    Check Algod and Indexer status.

Options:
  -t, --algo-threshold=<t>  [default: 1000]
  -p, --publisher=<p>       [default: WIPE4JSUWLXKZZK6GJ6VI32PX6ZWPKBRH5YFRJCHWOVC73P5RI4DGUQUWQ]
  -s, --start-block=<s>     [default: 11476070]
  -e, --end-block=<e>
  -h, --help
```
