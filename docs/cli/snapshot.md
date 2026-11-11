# Snapshot

Plot the latest published PPoS Dex data point, as in the
[Snapshot](../data/snapshot.md).

```text
$ uv run pposdex snapshot --help
{{#include help/snapshot.txt}}
```

The snapshot shows the latest data point published with the selected
`--algo-threshold`, by default by the PPoS Dex Oracle account. With `--save` the
plots are saved in `./docs/images/snapshot` instead of being shown.

The published data has no stake of each account: the online stake treemap reads
the online accounts holding more than `--algo-threshold` live from the Indexer.
