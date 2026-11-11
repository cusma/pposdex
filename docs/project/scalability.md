# Scalability

Scalability is the easiest of the three properties to measure: the ledger and
the protocol parameters tell it, and anyone can check them. It can be
quantified in several ways:

- **Finality latency**: a block is final as soon as it is appended, with no
  confirmations to wait for, unlike the probabilistic finality of PoW, where
  confidence grows with each block appended after it. Since the _dynamic round
  times_ upgrade, MainNet appends a block about every 2.8 seconds (2.76 seconds
  on average over the last million rounds, as of November 2026).
- **Throughput**: a block holds up to 5 MiB of transactions, about 25,000
  payments: at the current block time, a ceiling of about 9,000 transactions
  per second.
- **Transaction cost**: the minimum fee is 0.001 ALGO, and fees rise above it
  only when blocks are congested.
- **Energy consumption**: there is no computational race. Each node is a single
  server, and its consumption does not grow with the stake it validates.
- **Node hardware**: a validator node needs 8 vCPU, 16 GB of RAM, and 100 GB NVMe
  SSD ([Algorand docs](https://dev.algorand.co/nodes/types/)): a mid-range server,
  not specialized hardware.

Scaling has trade-offs too. A network can also scale by raising the hardware
its nodes need, leaving fewer people able to run one: that is the trilemma at
work, trading decentralization for scalability. This is why node requirements
belong among the scalability metrics, and why the
[Nodes Hardware Decentralization](nodes.md) looks at the same nodes from the
decentralization side.

So Algorand's _scalability_ can be measured, and verified by anyone.
