# Health

Check the Algorand node and Indexer of the selected network are available.

```text
$ uv run pposdex health --help
{{#include help/health.txt}}
```

Run it before the other commands, for example after starting AlgoKit LocalNet
(see [Node Setup](install.md#node-setup)), or when a command fails to reach the
APIs.
