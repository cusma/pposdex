# Plot PPoS Dex snapshot

---

Take a snapshot of latest published PPoS Dex data.

```shell
poetry run ppos_dex.py snapshot [--publisher=<p>] [--algo-threshold=<a>] [--start-block=<s>] [--localhost | --test]
```

## Options

1. `[--publisher=<p>]` publisher account address (default: PPoS Dex Oracle account);
1. `[--algo-threshold=<t>]` plot only data of accounts that own more than this
threshold (default: 1000 ALGO);
1. `[--start-block=<s>]` plot data from this block (if availables);
1. `[--localhost | test]` select local hosted Node and Indexer / other API providers,
or default TestNet end-points.

---
