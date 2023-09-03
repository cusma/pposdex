# Plot PPoS Dex snapshot

Take a snapshot of PPoS Dex Index data published by PPoS Dex Oracle (or by
yourself).

**Input**

```shell
python3 ppos_dex.py snapshot
```

**Options**

1. `[--publisher=<p>]` publisher account address (default: PPoS Dex Oracle account);
2. `[--algo-threshold=<t>]` plot only data of accounts that own more than this threshold (default: 1000 ALGO);
3. `[--start-block=<s>]` plot data from this block (if availables);
4. `[--localhost]` select local hosted Node and Indexer or other API providers;
