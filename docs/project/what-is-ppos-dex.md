# Algorand PPoS Decentralization Index

**PPoS Dex** is the Algorand Pure Proof of Stake (PPoS) Decentralization Index.

This project defines the index and provides a CLI tool to monitor it.

The monitoring tool is trustless: anyone can autonomously read the Algorand
blockchain, do some client-side math, and publish the index on-chain.

The official Algod and Indexer APIs serve only the current account balances: the
published data points are the record of the past ones. Historical state APIs,
like [Nodely Time Travel](https://nodely.io/docs/access/time-travel/), serve the
balances of any past round instead: PPoS Dex uses them to
[recompute](ppos-dex.md#recomputed-history) the metrics added after a data
point was published, checked against what it published.

Open index data are published daily by the [PPoS Dex Oracle](https://lora.algokit.io/mainnet/account/WIPE4JSUWLXKZZK6GJ6VI32PX6ZWPKBRH5YFRJCHWOVC73P5RI4DGUQUWQ)
and then plotted as [timeseries](../data/timeseries.md) and [snapshots](../data/snapshot.md).

PPoS Dex CLI provides also simple data analytics plots.

**So, what _"Decentralization Index"_ actually means?**

> [!WARNING]
> **Disclaimer:** PPoS Dex has not been audited nor officially approved by the
> Algorand Foundation. This project is just a personal attempt to provide some
> metrics on Algorand's decentralization to the community. **Algorand's
> decentralization is a common good**, but will not happen by itself: the
> community as a whole should embrace the path towards the decentralization
> jointly with the Algorand Foundation, committing to preserve it.
