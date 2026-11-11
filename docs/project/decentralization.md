# Decentralization

Defining a quantitative _Decentralization Index_ for a blockchain network
running on Proof of Stake (PoS) consensus is not simple: a precise and rigorous
definition of such a metric could easily be the subject of academic research
(which is not the intent of this project).

**So, how can we quantify PPoS decentralization?**

Here is a proposal.

## Consensus Protocol as Blockchain "Engine"

To present our arguments for the definition of a Decentralization Index, let's
compare blockchain networks running on PoS _Consensus Protocols_ with
_engines_, exploring the concept of efficiency of a machine.

When mathematicians search for the solutions of equations, or when physicists
do not know how to measure physical properties, they usually start by
investigating whether such solutions or properties have upper or lower bounds.

In 1824 the French physicist
[Nicolas Léonard Sadi Carnot](https://en.wikipedia.org/wiki/Nicolas_L%C3%A9onard_Sadi_Carnot)
discovered that the efficiency of any classical thermodynamic engine, converting
heat into work (or vice versa), _must be lower than a theoretical upper bound_:
the efficiency of a purely ideal machine, named _Carnot engine_ after him. Such
a "perfect" engine is just a theoretical construct and cannot be built in
practice.

This is probably the most elegant and general result in Classical Physics: it
implies that **any** system undergoing **any** kind of thermodynamic cycle can
only _tend_ to the efficiency of a Carnot engine operating under the same
conditions, never reach it, no matter how cleverly that system has been
designed.

In the same way, we try here to define an equivalent of a "Carnot engine" for
PoS consensus decentralization.

**Does such a theoretical decentralization upper bound even exist?**

**When should we say that a blockchain running on PoS consensus is completely
decentralized?**

## Decentralization Factors

To reach a common understanding of what measuring decentralization even means,
we should agree on some definitions.

We consider three different factors of decentralization that concur to define a
_Decentralization Index_ (\\(DEX\\)) of PoS networks:

1. [Nodes Hardware Decentralization](nodes.md) (\\(d_N\\))
1. [Network Topology Decentralization](topology.md) (\\(d_T\\))
1. [Stake Decentralization](stake.md) (\\(d_S\\))

We have to quantify each of these three factors as a _bounded per-unit metric_,
so that the _Decentralization Index_ can express "how far" a PoS blockchain
network is from "purely theoretical decentralization".

The index can range from 0 (_completely centralized_) to 1 (_completely
decentralized_):

\\[ DEX = d_N \cdot d_T \cdot d_S \\]

Let's first define an ideal theoretical condition of decentralization for each
of these three per-unit factors. Then, everything deviating from those
conditions will make a PoS blockchain more real, and far from platonic ideality.
