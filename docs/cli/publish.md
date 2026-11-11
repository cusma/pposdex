# Publish

Anyone can publish trustless PPoS Dex data points on the Algorand blockchain,
paying just the minimum transaction fee (currently 0.001 ALGO).

Set the _mnemonic_ of your publisher account as an environment variable:

```bash
export ALGO_MNEMONIC=...
```

and use the `publish` command:

```text
$ uv run pposdex publish --help
{{#include help/publish.txt}}
```

The published data point is printed once confirmed, for example:

```text
📈 PPoS Dex published data:
{   'accounts': 147633,
    'algo_dynamics': 0.9816195500486596,
    'algo_hhi': 0.011881330526539167,
    'algo_threshold': 1000,
    'ppos_dex': 0.00018605998214704048,
    'ppos_dex_v2': 0.197653743427405,
    'ppos_dex_v3_liveness': 7,
    'ppos_dex_v3_liveness_operators': 2,
    'ppos_dex_v3_nakamoto': 13,
    'ppos_dex_v3_nakamoto_operators': 3,
    'ppos_dex_v3_upgrade': 135,
    'ppos_dex_v3_upgrade_operators': 111,
    'ppos_dex_v3_veto': 4,
    'ppos_dex_v3_veto_operators': 1,
    'ppos_gini': 0.9030210736028383,
    'ppos_hhi': 0.01606794676611987,
    'ppos_online_accounts': 0.009550710207067525,
    'ppos_online_stake': 0.20464292567467565,
    'ppos_theil_l': 2.266361842976268,
    'ppos_theil_t': 2.4749568856442137,
    'round': 66605064,
    'timestamp': '2026-11-01 03:31:36.875492'}
```

> [!WARNING]
> Lower values of `--algo-threshold` require many more queries. Avoid lowering
> the default threshold, especially when using third-party API services.
