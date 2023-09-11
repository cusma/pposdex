# Algorand PPoS Decentralization Index

---

**PPoS Dex** is the Algorand Pure Proof of Stake (PPoS) Decentralization Index.

This project defines the index and provides a CLI tool to monitor it.

The monitoring tool is fully trustless: anyone can autonomulsy read the Algorand
blockchain, do some client-side math, and publish the index on-chain.

Open index data are published daily by the [PPoS Dex Oracle](https://algoexplorer.io/address/WIPE4JSUWLXKZZK6GJ6VI32PX6ZWPKBRH5YFRJCHWOVC73P5RI4DGUQUWQ)
and then plotted as [timeseries](./2_1_timeseries.md) and [snapshots](./2_2_snapshot.md).

PPoS Dex CLI provides also simple data analytics plots.

**So, what _"Decentralization Index"_ actually means?**

---

> **DISCLAIMER**
>
> PPoS Dex has not been audited nor officially approved by the Algorand Foundation.
> This project is just a personal attempt to provide some metrics on Algorand's
> decentralization to the community. **Algorand's decentralization is a common good**,
> but will not happen by itself: the community as a whole should embrace the path
> towards the decentalization jointly with the Algorand Foundation, commiting to
> preserve it.
