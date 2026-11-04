# PPoS Insights

Views derived from the published PPoS Dex data, to read decentralization trends
at a glance. Like the other charts, they are refreshed daily.

> [!TIP]
> The PPoS Dex accounts participation, the share of accounts online, measures
> the distance from an ideal where every account takes part in consensus. As a
> trend it misleads, though: when many accounts join the network, the share
> drops while more accounts than ever are online. These views count the
> accounts instead, and lead with absolute numbers.

## At a Glance

The absolute numbers first, then the PPoS Dex metrics, each with its latest
value and its change over the last year in the direction of decentralization.
Inequality indexes are better when lower, so their axes are inverted: up always
means more decentralized.

The ALGO participation also shows how its parts changed in the year: the online
stake, and the circulating supply it is a share of.

![Insights at a Glance](../images/insights/at_a_glance.svg)

## Online Accounts

All the accounts holding at least the threshold, and those online for
consensus: whether more accounts take part in consensus, however many join the
network.

![Insights Online Accounts](../images/insights/participation.svg)

## Effective Validators

The online accounts, and how many validators with equal stake they are worth:
see the [effective number of validators](../project/stake.md#effective-number-of-validators)
for how the entropy and HHI equivalents are computed.

![Insights Effective Validators](../images/insights/effective_validators.svg)

## Online Stake

The ALGO in circulation, \\(S_{dyn}\\) of the genesis supply, and the ALGO
online for consensus, \\(S_{prt}\\) of the circulating supply.

![Insights Online Stake](../images/insights/online_stake.svg)

## Decentralization Trajectory

The online accounts against the effective validators, week by week: moving to
the right means more validators, moving up means more evenly staked ones.

The dashed lines mark where the effective validators are a given share of the
online accounts: 100% means all the online accounts hold the same stake, and
the further below the path runs, the more concentrated the stake is.

![Insights Decentralization Trajectory](../images/insights/trajectory.svg)

## Monthly Change

The change of each metric monthly average, towards more or less
decentralization: trends and turning points across all metrics at once. The
absolute numbers come first, then all the accounts and the circulating supply,
then the PPoS Dex metrics.

![Insights Monthly Change](../images/insights/monthly_change.svg)
