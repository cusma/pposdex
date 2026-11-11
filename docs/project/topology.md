# Network Topology

A blockchain's public ledger is distributed across multiple nodes in a network.
All these nodes work together, using the same set of software rules (the
_Consensus Protocol_), to verify transactions that are eventually added to the
finalized ledger.

To keep the state of such a distributed system unique, coherent and
synchronized, information must flow across the network, ensuring efficient
paths of communication between the nodes.

So, _how_ nodes are connected to each other, forming a network, is the second
relevant factor of decentralization, commonly known as _Network Topology_.

Messages can be passed through the network by routing the traffic with
different techniques. In Algorand, information is spread across the network
through "message gossiping", handled by the Relay Nodes and by a peer-to-peer
network running alongside them. Relay Nodes route blocks to all connected
nodes, finding highly efficient communication paths and reducing communication
hops, while the peer-to-peer network adds direct communication paths between
nodes.

Paths of communication are therefore essential to ensure that no one is
excluded from the communication: everybody should be able to _talk_ and
_listen_ to each other without relying on a few dominant paths.

**The more communication paths between nodes, the more robust and
decentralized the network.**

Let's try to visualize some examples of communication paths between two generic
nodes \\(N_1\\) and \\(N_2\\), connected through graphs that are intuitively
different from each other:

![Topology examples](../images/diagrams/topologies.svg)

We can intuitively glimpse the difference between networks \\(A\\), \\(B\\),
\\(C\\) and \\(D\\) with respect to the concept of "topology decentralization".
Graph \\(D\\) is intuitively "more decentralized" than graph \\(A\\), since it
offers a larger set of communication paths between nodes \\(N_1\\) and
\\(N_2\\).

Graph theory and network analysis define rigorous indicators of centrality,
distribution and decentralization of a distributed system, assigning numbers or
rankings to nodes within a graph according to their network position.

Networks in which traffic is obliged to pass through a few dominant nodes, for
example, are less "decentralized" than networks in which the traffic is free to
flow through several possible communication paths.

Other metrics like
[Betweenness Centrality](https://en.wikipedia.org/wiki/Betweenness_centrality)
or [Closeness Centrality](https://en.wikipedia.org/wiki/Closeness_centrality)
are measures of centrality in a graph based on the evaluation of the shortest
paths.

One possible metric that fits our requirements for **Network Topology
Decentralization** well (being a per-unit metric bounded between 0 and 1) is
the _Central Point Dominance_ (\\(CPD\\)), which measures the maximum centrality
of a node in a graph. This metric ranges from 0 to 1:

- 0 represents a network in which there is no node such that all shortest paths
  have to pass through it;
- 1 means all routes have to pass through that node.

Network \\(C\\) in the examples above, for instance, is a graph with _Central
Point Dominance_ equal to 1, since any message must pass through the central
node to reach the others.

To stay consistent with the rest of the decentralization metrics used in this
project (1 meaning maximum decentralization), we consider the _one's
complement_ of the _Central Point Dominance_:

\\[ d_T = 1 - CPD \\]

## Algorand Topology

The Algorand node implementation
([go-algorand](https://github.com/algorand/go-algorand)) shapes the graph with
two kinds of nodes:

- **Relays** listen for incoming connections (up to 2,400 by default) and
  forward the messages they receive. Each relay also keeps outgoing connections
  to other relays: together, they form a mesh.
- **Non-relay nodes**, including the validator nodes, accept no incoming
  connections by default: each keeps up to 4 outgoing connections to relays,
  and regularly swaps the slowest for a random one.

Messages between non-relay nodes always pass through at least one relay: the
relays are the hubs of the graph, the nodes with the highest centrality. The
mesh between them offers many paths, so that no single relay lies on all of
them. Relays route the messages: relaying needs no stake, and a relay cannot
forge the votes, which validators sign.

Nodes can also enable the peer-to-peer (P2P) network. With P2P, any node that
listens for connections can relay messages, and other nodes find it through
the DHT (see below): relaying is no longer limited to the relays in the DNS
list. _Hybrid_ relays and nodes use both networks, and a hybrid node keeps up
to 4 outgoing links on each.

![Algorand topology](../images/diagrams/algorand_topology.svg)

In the example above, the nodes on the left use WebSocket only, with 4 links to
the relays each. The nodes on the right mix WebSocket and P2P links, some of
them to a relay serving P2P only. Thick links connect the relays to each other,
thin ones the nodes to the relays.

### Finding the Relays

By default, a node finds the relays in DNS records published under the
network's bootstrap domain: 69 relays on MainNet, as of November 2026. This
list is a default, not a permission. Any node configured to listen relays
messages, and node operators can add relays to their own phonebook, or point
their node to another bootstrap domain: relays run by third parties outside
the list serve the network too.

The P2P network, built on [libp2p](https://libp2p.io/), also bootstraps from
DNS, where the hybrid relays are listed. Nodes enabling it can then discover
other peers accepting connections through a distributed hash table (DHT),
beyond the DNS list.

Who runs the relays, where they are hosted, and how many nodes rely on the
default list are measurable properties of the topology: see
[Infrastructure Diversity](#infrastructure-diversity).

### Measuring the Topology

The \\(CPD\\) requires the whole graph, which is not public: nodes are
pseudonymous, and their connections change over time. This is why PPoS Dex
does not compute \\(d_T\\) yet.

## Infrastructure Diversity

Graph metrics measure how the nodes are connected, not where they run. Nodes
hosted by the same network (the same cloud provider or Internet service
provider) can fail together in an outage, or be cut off together by its
policies; nodes in the same country answer to the same jurisdiction.

The same question as the [Nakamoto Coefficient](stake.md#nakamoto-coefficient)
applies to infrastructure, counting nodes instead of stake: how few hosting
networks, or countries, host more than 10%, 20% and 1/3 of the nodes? The
[Nodely dashboard](https://g.nodely.io/d/network/network) shows the nodes by
hosting network and by country.

> [!IMPORTANT]
> Nodes are not weighted by stake: a node with no stake online counts as much as
> one with millions of ALGO. Infrastructure diversity tells how resilient the
> network that relays the messages is, not who votes.

> [!NOTE]
> Network Topology Decentralization does not consider the infrastructure
> diversity. More insights on the geo-delocalization of the physical
> infrastructure can be found in [Analyzing Algorand Blockchain Data with
> Databricks Delta](https://databricks.com/blog/2020/10/08/analyzing-algorand-blockchain-data-with-databricks-delta.html).
> For the scope of this project, we consider a _perfect_ Network Topology
> Decentralization (\\( d_T = 1 \\)), leaving the refinement of the calculation
> of this decentralization factor to future works.
>
> [Community contributions are welcome!](https://github.com/cusma/pposdex)
