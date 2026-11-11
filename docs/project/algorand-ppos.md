# Algorand Pure Proof of Stake Consensus

[Prof. Silvio Micali](https://en.wikipedia.org/wiki/Silvio_Micali) combined
distributed computation, cryptography and game theory into the
[Algorand Pure Proof of Stake](https://dev.algorand.co/concepts/protocol/overview/)
(PPoS) consensus protocol, to keep the promise of blockchains.

PPoS runs a _cryptographic sortition_ based on a
[Verifiable Random Function](https://dev.algorand.co/concepts/protocol/overview/#verifiable-random-function)
(VRF): a fair, tamper-proof and provable lottery, open to anyone holding
Algorand's native cryptocurrency, **ALGO**.

Each ALGO _online_ in consensus is a ticket of this lottery. For every new
block, the lottery runs secretly on each participating node, with minimal
hardware requirements and negligible energy consumption, to:

- randomly and secretly elect a block proposer;
- randomly and secretly elect a committee of validators _for every proposed
  block_.

At its core, PoW is a random leader election: no one can predict which miner
will first find a nonce hashing below the target, and anyone can verify it
with a single hash. PPoS achieves the same core properties in an elegant and purely
cryptographic way, based on stake instead of work. The election is
**unpredictable**, since no one knows who is elected before they reveal it, and
**provable**, since each elected participant proves it with the VRF output that
anyone can verify. The VRF draws a **random** leader, and a random committee,
with odds proportional to the stake online.

Participants keep their ALGO: they do not delegate their votes, do not need a
minimum stake to take part, and do not bond their ALGO. Protocol staking
rewards are paid only to accounts holding between 30,000 and 70,000,000 ALGO.

PPoS aims to solve the blockchain trilemma, achieving at the same time:

1. [Scalability](scalability.md);
1. [Security](security.md);
1. [Decentralization](decentralization.md).

**The point is: can we measure these properties?**

> [!TIP]
> Useful references:
>
> - [Algorand](https://arxiv.org/abs/1607.01341), the original paper
> - [Algorand PPoS Video](https://www.youtube.com/watch?v=u0ExeqpKJd0)
> - [Algorand Efficiency Video](https://www.youtube.com/watch?v=e8s8Ui8vDaY)
