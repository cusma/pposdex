# Nodes Hardware Decentralization

The first factor for the evaluation of a network's decentralization is the
_rate of growth_ of the overall "nodes' hardware" connected to the network.

It is important to remark that this metric takes into account the nodes'
_"growth rate"_ rather than just their _"absolute number"_, for the following
reason: one could easily say that 10 nodes are better than 1 node, or that 100
nodes are better than 10 nodes. But are 1.5 million nodes really _much better_
than 1 million nodes?

What we are trying to state here is that the number of nodes should be analyzed
as a _growth phenomenon_, which tends to reach a _steady state_ after which
adding more nodes does not really impact decentralization in a linear and
proportional way.

_Sigmoid functions_, like the _Logistic function_ or the _Error function_, are a
good way to model growth phenomena. Their characteristic _S_-shaped curve
perfectly models a system, like a network, that progresses from small
beginnings, accelerates, and approaches a climax over time.

_Cumulative Distribution_ functions, similarly, contain information on how a
phenomenon grows or is distributed before or after a certain _"inflection
point"_.

We propose to model the **Nodes Hardware Decentralization** as a _Cumulative
Distribution_:

\\[ d_{N} = 1 - e^{-\left(\frac{N}{\lambda}\right)^k} \\]

which can theoretically range from 0 (no hardware growth) to 1 (complete
hardware growth).

The parameters \\(k\\) and \\(\lambda\\) should be calibrated to best fit the
growth phenomenon with respect to the growth _"inflection point"_:

- \\(k\\) defines the speed of growth of the phenomenon;
- \\(\lambda\\) defines the order of magnitude of the inflection point for a
  given growth phenomenon.

How to tune \\(\lambda\\) for a blockchain network could be debated around the
following question:

**What is the reasonable order of magnitude of nodes at which we can say that a
blockchain network has grown sufficiently?**

Our opinion is that a meaningful _decentralization "inflection point"_ for a
blockchain network should be greater than a few dozen or a few hundred nodes.
In particular, given the context of the analysis, we think it adequate and
reasonable to set:

- \\(k = 2\\) for the speed of growth;
- \\(\lambda = 10^4\\) for the inflection point magnitude.

\\[ d_{N} = 1 - e^{-\left(\frac{N}{10^4}\right)^2} \\]

![Nodes Hardware Decentralization](../images/examples/nodes_hardware.svg)

The chart shows the curve for \\(\lambda = 10^4\\), next to
\\(\lambda = 10^3\\) and \\(\lambda = 10^5\\), and the range of nodes
Algorand has today (see [below](#full-time-nodes-on-algorand)). With
\\(\lambda = 10^4\\), the Nodes Hardware Decentralization stays low up to a
few thousand nodes, and saturates past twenty thousand:

| Nodes \\(N\\) | 1,000 | 3,000 | 5,000 | 10,000 | 20,000 |
|---------------|-------|-------|-------|--------|--------|
| \\(d_N\\)     | 0.01  | 0.09  | 0.22  | 0.63   | 0.98   |

## A Necessary Condition

The number of nodes alone does not make a network decentralized: a thousand
nodes run by the same operator, or hosted by the same provider, are not a
thousand independent ones. But it bounds decentralization: \\(N\\) nodes are
at most \\(N\\) independent points of failure, however the stake is spread.
Few nodes guarantee concentration; many nodes make decentralization possible,
without proving it.

Stake metrics cannot see this bound. Two examples:

- **Many accounts on one node**: participation keys of many accounts can be
  hosted on the same node (possible, though not recommended). The accounts look
  like independent validators, yet a single failure, compromise or wrong
  upgrade of that node takes them all offline together.
- **Few API nodes**: if only a few nodes accept transactions, a few providers
  can censor, throttle or fail to serve them, whatever the stake distribution.

\\(d_N\\) is then an upper bound, like the efficiency of the Carnot engine:
it is low with few nodes, and saturates when more nodes no longer change the
picture. The saturation also limits how much counting nodes can be gamed:
pseudonymous nodes cost little to add, but past the inflection point adding
them barely raises \\(d_N\\). The other side, how independent the nodes are,
is measured by their distribution: see
[Infrastructure Diversity](topology.md#infrastructure-diversity).

The inflection point \\(\lambda\\) remains a judgment call: with
\\(\lambda = 10^3\\) instead of \\(10^4\\), a few thousand nodes would already
be close to \\(d_N = 1\\).

## Counting the Nodes

Algorand nodes are pseudonymous: anyone can run one, and no registry lists
them. They can only be observed, from the relays they connect to: as of 2025,
each node keeps a connection to four relays at a time, and regularly swaps the
slowest for a random one. Counting the distinct IP addresses a few relays see
is no longer reliable: home nodes change address, and short-lived bots connect
and leave.

[Nodely](https://nodely.io/blog/algorand-node-counting/) estimates instead the
_full-time node equivalents_: a node online half of the time counts as half a
node. Every hour, a sample of relays records the nodes connected to them, and
the _Chao-1_ estimator infers from it how many nodes no relay saw.

### Chao-1 Estimator

Ecologists face the same problem when counting the species of an environment:
some are too rare to be found in a sample. Anne Chao's estimator uses the
rarest ones found to estimate those missed. Given the \\(S_{obs}\\) nodes
observed, of which \\(F_1\\) were seen by a single relay and \\(F_2\\) by
exactly two:

\\[ S_{Chao1} = S_{obs} + \frac{F_1^2}{2 F_2} \\]

Many nodes seen by a single relay mean many more were likely seen by none: the
estimate grows. Few of them mean the relays saw almost every node: it stays
close to \\(S_{obs}\\). For example, 2,000 nodes observed in an hour, 300 by a
single relay and 200 by two, estimate:

\\[ S_{Chao1} = 2000 + \frac{300^2}{2 \cdot 200} = 2225 \\]

The estimate is a lower bound, and does not depend on how many relays observe.
Nodely averages the hourly estimates over 7 days, to smooth out the hours of
the day.

> [!NOTE]
> The estimate counts IP addresses, not machines: nodes sharing an address
> (behind NAT) count as one, and nodes changing it within the hour as many.
> Nodes connected only to private relays are missed, and the relays observing
> may not be representative of the whole network.

### Which Nodes Count

The estimate counts every node connecting to the relays: validator nodes, which
vote with the online stake, but also API, archival and idle nodes, which only
follow the chain. It is the hardware running the network, not the number of
validators.

The ledger cannot tell the validators either: it shows the online accounts, not
the nodes hosting them. A node can host the participation keys of many
accounts, and an operator can run many nodes. The
[Nakamoto Coefficient of operators](stake.md#nakamoto-coefficient) groups the
online accounts likely run by the same operator, from the stake side.

The two examples [above](#a-necessary-condition) call for two different
counts, neither of which can be observed today: the nodes hosting online stake,
for the validators, and the nodes accepting transactions, for the access to the
network. A refined \\(d_N\\) should count them separately.

### Full-Time Nodes on Algorand

The estimate ranged from about 1,200 to 3,700 full-time nodes since 2024: see
the [Nodely dashboard](https://g.nodely.io/d/network/network). With
\\(\lambda = 10^4\\), that is a Nodes Hardware Decentralization \\(d_N\\)
between 0.01 and 0.13: how to calibrate the inflection point remains an open
question.

> [!NOTE]
> PPoS Dex v1 and v2 consider a _perfect_ Nodes Hardware Decentralization
> (\\( d_N = 1 \\)), leaving the refinement of the calculation of this
> decentralization factor to future works.
>
> [Community contributions are welcome!](https://github.com/cusma/pposdex)

## Growing the Nodes

Two factors drive the growth of the nodes:

- **Hardware**: a validator node runs on a mid-range server (see
  [Scalability](scalability.md)), so the hardware is not a barrier to entry;
- **Incentives**: running a validator node takes time and care. The
  [staking rewards](https://dev.algorand.co/concepts/protocol/staking-rewards/),
  live since January 2025, pay block proposers holding between 30,000 and
  70,000,000 ALGO, because fewer ALGO holders ran validator nodes than the
  network's security needed.

## Node Versions

Algorand upgrades its consensus protocol when more than 90% of the
[stake](stake.md#nakamoto-coefficient) agrees. Nodes still running a version
that does not support the live protocol cannot follow the consensus anymore:
the share of nodes on an incompatible version tells how many fell behind the
last upgrade. Nodely's
[upgrade stats](https://g.nodely.io/d/bea312nluusxse/upgrade-stats) show it.

## Software Diversity

Every node announces its software to the peers it connects to: the
[go-algorand](https://github.com/algorand/go-algorand) node sends a
`User-Agent` with its version, operating system and CPU architecture, for
example `algod/5.1 (stable; ...) linux(amd64)`. Relays can therefore observe
how many nodes run on each operating system (such as Linux or macOS) and on
each architecture (such as `amd64` or `arm64`), the same way they observe the
node versions.

Platform diversity limits correlated failures: a bug specific to an operating
system or an architecture affects only the nodes running on it.

## Geographical Distribution

Where the nodes run, by hosting network and by country, is part of the network
topology: see [Infrastructure Diversity](topology.md#infrastructure-diversity).
