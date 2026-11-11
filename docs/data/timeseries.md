# PPoS Timeseries

The PPoS Dex data published daily, and views derived from it, refreshed daily.

## Overview

### At a Glance

The online stake, the online accounts and the
[entropy equivalent](../project/stake.md#entropy-equivalent) validators, then
the PPoS Dex v3 coefficients, with their operators, and the PPoS Dex v1 and v2:
each with its latest value and its change over the last year in the direction
of decentralization. The index components have their own charts below.

![Timeseries at a Glance](../images/insights/at_a_glance.svg)

### Monthly Change

The change of each metric monthly average, towards more or less
decentralization: trends and turning points across all metrics at once. The
network first, with all the accounts holding more than 1,000 ALGO, then the
PPoS Dex v3 coefficients, then the PPoS Dex v1 and v2 and the concentration of
the online stake and of all the ALGO.

![Timeseries Monthly Change](../images/insights/monthly_change.svg)

## The Network

### Online Stake

The ALGO in circulation, \\(S_{dyn}\\) of the genesis supply, and the ALGO
online for consensus, \\(S_{prt}\\) of the circulating supply: see the
[Stake Participation Index](../project/stake.md#stake-participation-index).

![Timeseries Online Stake](../images/insights/online_stake.svg)

### Effective Validators

The online accounts, and how many validators with equal stake they are worth:
see the [effective number of validators](../project/stake.md#effective-number-of-validators)
for how the entropy and HHI equivalents are computed.

![Timeseries Effective Validators](../images/insights/effective_validators.svg)

### Decentralization Trajectory

The online accounts against the
[effective validators](../project/stake.md#effective-number-of-validators),
week by week: moving to the right means more validators, moving up means more
evenly staked ones.

The dashed lines mark where the effective validators are a given share of the
online accounts: 100% means all the online accounts hold the same stake, and
the further below the path runs, the more concentrated the stake is.

![Timeseries Decentralization Trajectory](../images/insights/trajectory.svg)

## PPoS Dex

### PPoS Dex v3

The [PPoS Dex v3](../project/ppos-dex.md#ppos-dex-v3) since its first
publication: the fewest online accounts holding more than 10% (veto), 20%
(liveness), 1/3 (Nakamoto) and 90% (upgrade) of the online stake, by account and
counting the accounts likely run by the same operator as one.

![Timeseries PPoS Dex v3](../images/timeseries/ppos_dex_v3.svg)

### PPoS Dex v1 and v2

The [PPoS Dex](../project/ppos-dex.md) v1 and v2: how far the stake is from a
platonic ideal of decentralization, where every ALGO and every account takes
part in consensus with equal stakes. Real networks only tend to that ideal, so
these trends read as a direction rather than as a distance to cover.

![Timeseries PPoS Dex](../images/timeseries/ppos_dex.svg)

## Index Components

### Participation

How much of the ALGO and of the accounts takes part in consensus: the
[Stake Participation Index](../project/stake.md#stake-participation-index) and
the [Account Participation Index](../project/stake.md#account-participation-index).

#### ALGO Dynamics

The ALGO Supply \\(S_{dyn}\\) and the ALGO Participation \\(S_{prt}\\) of the
[Stake Participation Index](../project/stake.md#stake-participation-index).

> [!TIP]
> The ALGO Participation is a ratio: it drops when ALGO enters circulation, even
> if more ALGO than ever is online. See the [Online Stake](#online-stake) for the
> absolute numbers behind it.

![Timeseries ALGO Dynamics](../images/timeseries/algo_dynamics.svg)

#### Accounts Participation

The [Account Participation Index](../project/stake.md#account-participation-index).

> [!TIP]
> The Accounts Participation is a ratio: it drops when accounts join the
> network, even if more accounts than ever are online. The panel below shows the
> accounts behind it.

![Timeseries Accounts Participation](../images/timeseries/accounts_prt.svg)

### Online Stake Inequality

How unequally the online stake is spread across the validators: the
[Stake Inequality Index](../project/stake.md#stake-inequality-index).

#### PPoS Inequality (Bounded)

The [Gini Index](../project/stake.md#gini-index) and the
[HHI](../project/stake.md#herfindahlhirschman-index) of the online stake.

> [!TIP]
> The Gini Index rises when small validators join, even as the stake spreads
> across more of them: see the notes on the [Gini Index](../project/stake.md#gini-index).

![Timeseries PPoS Inequality Bounded](../images/timeseries/ppos_inequality_b.svg)

#### PPoS Inequality (Unbounded)

The [Theil Indexes](../project/stake.md#theil-indexes) of the online stake.

> [!TIP]
> The Theil T Index grows with the number of validators, even as the stake
> spreads across more of them: the [entropy equivalent](../project/stake.md#entropy-equivalent)
> turns it into a count that does not.

![Timeseries PPoS Inequality Unbounded](../images/timeseries/ppos_inequality_unb.svg)

### All ALGO Concentration

How concentrated all the ALGO is, online or not: the ALGO HHI of the
[PPoS Dex metrics](../project/ppos-dex.md#metrics-summary).

#### ALGO Inequality

The [Herfindahl–Hirschman Index](../project/stake.md#herfindahlhirschman-index)
of all the accounts holding more than the threshold, online or not.

![Timeseries ALGO Inequality](../images/timeseries/algo_inequality.svg)

#### Effective Holders

How many equal holders the ALGO of all the accounts above the threshold is
worth, as the [HHI equivalent](../project/stake.md#hhi-equivalent) of the ALGO
HHI. Custodians and exchanges hold ALGO for many owners: this counts accounts,
not owners.

![Timeseries Effective Holders](../images/insights/effective_holders.svg)
