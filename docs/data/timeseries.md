# PPoS Timeseries

The PPoS Dex data published daily, and views derived from it, refreshed daily.

> [!TIP]
> The participation ratios of the PPoS Dex measure the distance from an ideal
> where every account and every ALGO takes part in consensus. As trends they
> mislead, though: when accounts join the network or ALGO enters circulation,
> the ratios drop even if more accounts and ALGO than ever take part. These
> charts lead with absolute numbers, and keep the ratios among the index
> components.

## At a Glance

The absolute numbers first, then the PPoS Dex metrics, each with its latest
value and its change over the last year in the direction of decentralization.
Inequality indexes are better when lower, so their axes are inverted: up always
means more decentralized.

![Timeseries at a Glance](../images/insights/at_a_glance.svg)

## PPoS Dex

The [PPoS Dex](../project/ppos-dex.md) v1 and v2, and the v3: the fewest online
accounts holding more than 20% of the online stake, also counting the accounts
likely run by the same operator as one.

![Timeseries PPoS Dex](../images/timeseries/ppos_dex.svg)

## Effective Validators

The online accounts, and how many validators with equal stake they are worth:
see the [effective number of validators](../project/stake.md#effective-number-of-validators)
for how the entropy and HHI equivalents are computed.

![Timeseries Effective Validators](../images/insights/effective_validators.svg)

## Online Stake

The ALGO in circulation, \\(S_{dyn}\\) of the genesis supply, and the ALGO
online for consensus, \\(S_{prt}\\) of the circulating supply.

![Timeseries Online Stake](../images/insights/online_stake.svg)

## Decentralization Trajectory

The online accounts against the effective validators, week by week: moving to
the right means more validators, moving up means more evenly staked ones.

The dashed lines mark where the effective validators are a given share of the
online accounts: 100% means all the online accounts hold the same stake, and
the further below the path runs, the more concentrated the stake is.

![Timeseries Decentralization Trajectory](../images/insights/trajectory.svg)

## Monthly Change

The change of each metric monthly average, towards more or less
decentralization: trends and turning points across all metrics at once. The
absolute numbers come first, then all the accounts and the circulating supply,
then the PPoS Dex metrics.

![Timeseries Monthly Change](../images/insights/monthly_change.svg)

## Index Components

### ALGO Dynamics

![Timeseries ALGO Dynamics](../images/timeseries/algo_dynamics.svg)

### ALGO Inequality

![Timeseries ALGO Inequality](../images/timeseries/algo_inequality.svg)

### Effective Holders

How many equal holders the ALGO of all the accounts above the threshold is
worth, as the HHI equivalent of the ALGO HHI. Custodians and exchanges hold ALGO
for many owners: this counts accounts, not owners.

![Timeseries Effective Holders](../images/insights/effective_holders.svg)

### PPoS Inequality (Bounded)

The Gini Index rises when small validators join: see the notes on the
[Gini Index](../project/stake.md#gini-index).

![Timeseries PPoS Inequality Bounded](../images/timeseries/ppos_inequality_b.svg)

### PPoS Inequality (Unbounded)

The Theil T Index grows with the number of validators: see the notes on the
[Theil Indexes](../project/stake.md#theil-indexes).

![Timeseries PPoS Inequality Unbounded](../images/timeseries/ppos_inequality_unb.svg)
