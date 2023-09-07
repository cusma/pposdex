# Algorand Pure Proof of Stake Consensus

---

[Prof. Silvio Micali](https://it.wikipedia.org/wiki/Silvio_Micali)
combined state-of-art distributed computation, cryptography and game theory
into the [Algorand Pure Proof of Stake](https://developer.algorand.org/docs/algorand_consensus/)
Consensus Protocol, to keep the foundational Blockchains' promise.

PPoS consensus is based on the [Verifiable Random Function](https://developer.algorand.org/docs/algorand_consensus/#verifiable-random-function)
(VRF).

The VRF is used to create a fair, tamper-proof, secure and provable
_cryptographic sortition_, in which people are free to take part as long as
they own any amount of Algorand's native cryptocurrency, named **ALGO**.

Each _"participating"_ ALGO acts as a ticket of a cryptographic lottery
that secretly runs in parallel on Algorand network's nodes, for each new block,
with minimal hardware requirements and neglectable energy consumption.

Users participating in Algorand PPoS do not delegate their votes, do not
need a minimum stake to take part in the PPoS, and do not bond their ALGOs.

The cryptographic sortition is used to:

- Randomly and secretly elect a block proposer;
- Randomly and secretly elect a committee of validators _for every proposed block_.

Algorand PPoS solves Blockchains' trilemma acheiving at the same time:

1. Scalability
1. Security
1. Decentralization

**The point is: can we measure these properites?**

---

> Useful references:
>
> - [Algorand](https://arxiv.org/abs/1607.01341)
> - [Algorand PPoS Video](https://www.youtube.com/watch?v=u0ExeqpKJd0)
> - [Algorand Efficency Video](https://www.youtube.com/watch?v=e8s8Ui8vDaY)
