# Publish PPoS Dex data points

---

Contribute publishing trustless PPos Dex data points on Algorand blockchain paying
just the minimum transaction fee (currently 0.001 ALGO).

Set your publisher _mnemonic_ as environment variable:

```bash
export ALGO_MNEMONIC=...
```

and use the `publish` command:

```bash
$ poetry run python3 ppos_dex.py publish [--algo-threshold=<a>] [--localhost | --test]

📈 PPoS Dex published data:

{
  "algo_threshold": 1000,
  "accounts": 13346,
  "algo_dynamics": 0.3741854092978301,
  "ppos_online_stake": 0.598241416943984,
  "ppos_online_accounts": 0.01715869923572606,
  "ppos_gini": 0.829793933948626,
  "ppos_theil_l": 4.640220128476622,
  "ppos_theil_t": 1.5593480873810057,
  "ppos_dex": 0.0006537665878508702,
  "timestamp": "2021-01-06 00:22:09.607573"
}
```

## Options

1. `[--algo-threshold=<at>]` consider only accounts that own more than this threshold
(default: 1000 ALGO);
1. `[--localhost | test]` select local hosted Node and Indexer / other API providers,
or default TestNet end-points.

Is worth noting that lower values of `[--algo-threshold=<at>]` will require more
querying efforts. You should avoid lowering the default threshold, expecially if
you are using third party API services.

---
