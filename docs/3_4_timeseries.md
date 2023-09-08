# Plot PPoS Dex timeseries

---

Plot PPoS Dex timeseries published to evaluate trends.

```shell
potery run ppos_dex.py timeseries [--publisher=<p>] [--algo-threshold=<a>] [--start-block=<s>] [--end-block=<e>] [--localhost | --test] [--save]
```

## Options

1. `[--publisher=<p>]` publisher account address (default: PPoS Dex Oracle account);
1. `[--algo-threshold=<t>]` plot only data of accounts that own more than this
threshold (default: 1000 ALGO);
1. `[--start-block=<s>]` plot data from this block (if availables);
1. `[--end-block=<e>]` plot data until this block;
1. `[--localhost | test]` select local hosted Node and Indexer / other API providers,
or default TestNet end-points;
1. `[--save]` save plots in `./docs/images/timeseries`.

---
