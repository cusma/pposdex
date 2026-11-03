# Plot PPoS Dex timeseries

Plot PPoS Dex timeseries published to evaluate trends.

```text
$ uv run pposdex timeseries --help
{{#include help/timeseries.txt}}
```

Only data points published with the selected `--algo-threshold` are plotted, by
default those of the PPoS Dex Oracle account. With `--save` the plots are saved
in `./docs/images/timeseries` instead of being shown.
