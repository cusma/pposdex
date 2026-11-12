# PPoS Snapshot

The latest PPoS Dex data point published, in the same order as the
[Timeseries](timeseries.md).

## The Network

### Validators

The online accounts, and the [effective number of
validators](../project/stake.md#effective-number-of-validators) they are worth:
how many validators with equal stake would be as decentralized, by entropy and
by HHI.

![Snapshot Validators](../images/snapshot/validators.svg)

### Online Stake

Who holds the online stake, by account and by [likely
operator](../project/ppos-dex.md#ppos-dex-v3): the same view as the
[examples](../project/stake.md#examples), with the real validators.[^live]
[Valar Decentralization](https://decentralization.valar.solutions/) shows the
same stake by named operator and staking solution.

![Snapshot Online Stake](../images/snapshot/stakes.svg)

[^live]: The published data has no stake of each account: this chart reads it
    live from the Indexer when the docs are deployed.

## PPoS Dex

### PPoS Dex v3

The four [PPoS Dex v3](../project/ppos-dex.md#ppos-dex-v3) coefficients, on
the scale of the online accounts: first by account, then merging the accounts
likely run by the same
[operator](../project/stake.md#nakamoto-coefficient). Merged, the operators
can only be fewer, so their coefficients are lower or equal.

![Snapshot PPoS Dex v3](../images/snapshot/ppos_dex_v3.svg)

![Snapshot PPoS Dex v3 by operator](../images/snapshot/ppos_dex_v3_operators.svg)

### PPoS Dex v1 and v2

The [PPoS Dex v1](../project/ppos-dex.md#ppos-dex-v1) and
[v2](../project/ppos-dex.md#ppos-dex-v2): how far the stake is from a platonic
ideal of decentralization, where every ALGO and every account takes part in
consensus with equal stakes. Real networks only tend to that ideal, so their
[trend](timeseries.md#ppos-dex-v1-and-v2) tells more than a single value.

![Snapshot PPoS Dex](../images/snapshot/ppos_dex.svg)

## Index Components

### ALGO Dynamics

The ALGO Supply \\(S_{dyn}\\) of the
[Stake Participation Index](../project/stake.md#stake-participation-index): the
share of the genesis supply in circulation.

![Snapshot ALGO Dynamics](../images/snapshot/algo_dynamics.svg)

### PPoS Inequality

The [Stake Inequality Index](../project/stake.md#stake-inequality-index) of the
online stake: the Gini, HHI and Theil indexes. The Gini and Theil T indexes rise
as small validators join: see the
[tips on reading them](timeseries.md#online-stake-inequality).

![Snapshot PPoS Inequality](../images/snapshot/ppos_inequality.svg)
