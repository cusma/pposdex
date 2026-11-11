# Export

Export the published PPoS Dex data points to a `.csv` file, for your own
analysis.

```text
$ uv run pposdex export --help
{{#include help/export.txt}}
```

The data points published with the selected `--algo-threshold` are written to
`ppos_dex_data.csv`, in the current directory.
