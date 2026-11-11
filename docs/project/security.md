# Security

Security has no single metric, and quantifying it is out of the scope of this
project. Its foundations, though, can be stated precisely, and the main one is
about stake.

## Honest Supermajority

PPoS is secure as long as more than 2/3 of the online stake is in honest hands.
How few accounts it would take to break this assumption is a measure of
decentralization: the [Nakamoto Coefficient](stake.md#nakamoto-coefficient)
counts them, and the [PPoS Dex v3](ppos-dex.md#ppos-dex-v3) publishes it every
day.

Under this assumption:

- **No forks**: at most one block is certified per round, so a block is final
  as soon as it is appended, and the history cannot be reorganized. If the
  network is partitioned, the consensus stops rather than fork, and resumes
  once the network heals.
- **Secret election**: the sortition runs privately on each node. Every step of
  the agreement is run by a new committee, whose members stay secret until
  they send their first and only message (_player replaceability_): by then,
  it is too late to DDoS, corrupt or threaten them.
- **Forward security**: the participation keys voting on blocks are separate
  from the spending keys, and the ephemeral key of each round is deleted once
  used ([participation keys](https://dev.algorand.co/concepts/protocol/partkey-management/)):
  an attacker compromising a node later can neither move its funds nor sign
  past rounds again.

These are not just design claims. The Algorand Agreement (Chen, Gorbunov,
Micali and Vlachos, 2018) is proven to reach agreement under a > 2/3 honest
majority, and to be resilient to network partitions of any length. Benhamouda,
Blum, Katz, Leung, Loss and Rabin (ACM CCS 2023) analyze the protocol as
deployed on MainNet: they prove it provides _consistency_ (no forks) under arbitrary
network conditions, except with negligible probability, and _liveness_ under intermittent
network partitions, characterizing the network conditions and parameters this requires.

> [!TIP]
> Academic references:
>
> - [Algorand](https://arxiv.org/abs/1607.01341), Chen and Micali (2016)
> - [Algorand Agreement: Super Fast and Partition Resilient Byzantine
>   Agreement](https://eprint.iacr.org/2018/377), Chen, Gorbunov, Micali and
>   Vlachos (2018)
> - [Analyzing the Real-World Security of the Algorand
>   Blockchain](https://eprint.iacr.org/2023/1344), Benhamouda, Blum, Katz,
>   Leung, Loss and Rabin (ACM CCS 2023)

## Liveness

The consensus makes progress only if enough of the online stake votes: a
coalition holding more than 20% of it could, conservatively, stall the
consensus by not voting. Online stake whose node is down weakens liveness just
the same. Since the [staking rewards](https://dev.algorand.co/concepts/protocol/staking-rewards/)
upgrade (January 2025), online accounts that fail to propose as often as their
stake predicts, or to answer random challenges, can be suspended and taken
offline.

## State Proofs

Every 256 rounds (about 12 minutes), Algorand
[State Proofs](https://dev.algorand.co/concepts/protocol/state-proofs/) commit to
the transactions of the interval, signed by the online accounts with
post-quantum resistant [Falcon signatures](https://falcon-sign.info/): other
chains and light clients can verify Algorand's history without trusting an
intermediary.

## Track Record

At the time of writing (November 2026), [Algorand](https://algorand.co/)
reports no downtime since its genesis block (June 2019), and, being fork-free,
its history has no reorgs.
