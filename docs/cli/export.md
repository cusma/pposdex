# Export PPoS Dex data

Export PPoS Dex data to `csv` file for external analysis.

```text
$ uv run pposdex export --help
{{#include help/export.txt}}
```

Data points published with the selected `--algo-threshold` are written to
`ppos_dex_data.csv`, in the current directory.
