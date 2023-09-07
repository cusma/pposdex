# Export Plot PPoS Dex data

---

Export PPoS Dex data to `csv` file for external analysis.

```shell
poetry run ppos_dex.py export [--publisher=<p>] [--algo-threshold=<a>] [--start-block=<s>] [--end-block=<e>] [--localhost | --test]
```

## Options

1. `[--publisher=<p>]` publisher account address (default: PPoS Dex Oracle account);
1. `[--algo-threshold=<t>]` export only data of accounts that own more than this
threshold (default: 1000 ALGO);
1. `[--start-block=<s>]` export data from this block (if availables);
1. `[--end-block=<e>]` export data until this block;
1. `[--localhost | test]` select local hosted Node and Indexer / other API providers,
or default TestNet end-points.
