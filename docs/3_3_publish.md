# Publish PPoS Dex data

Contribute publishing trustless reliable data on Algorand blockchain paying
just the minimum network fee (currently 0.001 ALGO).

Set your publisher mnemonic as environment variable:

```shell
export ALGO_MNEMONIC=...
```

**Input**

```bash
python3 ppos_dex.py publish
```

**Options**

1. `[--algo-threshold=<at>]` consider only accounts that own more than this threshold (default: 1000 ALGO);
2. `[--localhost]` select local hosted Node and Indexer or other API providers;

Is worth noting that lower values of `[--algo-threshold=<at>]` will require more
querying efforts, so you should avoid going under default threshold, expecially
if you are using a third party API service.

**Output**

```shell
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

You can then find your result published on-chain ([example](https://algoexplorer.io/tx/NPAAMBUEAIIYJJDFZWMYAHJBBSXDO2PV5TTSCD3SKWNBCLOU2AYA)).
