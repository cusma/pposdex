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

Counting the online accounts tells how many validators there are, not how much
each one weighs in consensus: a thousand accounts where one holds almost all the
stake are barely more decentralized than a single validator.

The _effective number of validators_ answers a more telling question: how many
validators, all holding the _same_ stake, would be exactly as decentralized as
the actual ones? With equal stakes it is the number of online accounts, and it
drops as the stake concentrates, down to 1 when a single account holds it all.

### Entropy Equivalent

The entropy of the online stake measures how uncertain it is which validator
holds a randomly picked ALGO. Given the stake shares \\(s_i\\) of the \\(N\\)
online accounts:

\\[ H(S) = - \sum_{i=1}^{N} s_i \ln s_i \\]

With \\(n\\) equal stakes the entropy is \\(\ln n\\), so a distribution with
entropy \\(H\\) is as diverse as \\(e^H\\) equal validators: its _entropy
equivalent_. Since the Theil T index is how far the entropy is from its
maximum, \\(T_T(S) = \ln N - H(S)\\), it is computed from the published data as:

\\[ N_{H} = e^{H(S)} = N \cdot e^{-T_T(S)} \\]

### HHI Equivalent

The Herfindahl-Hirschman index is the sum of the squared stake shares: \\(n\\)
equal stakes have \\(HHI = 1/n\\), so the _HHI equivalent_ is:

\\[ N_{HHI} = \frac{1}{HHI(S)} \\]

Squaring the shares weighs the largest stakes more, so the HHI equivalent is
always the lowest of the three counts:

\\[ N \geq N_{H} \geq N_{HHI} \\]

### Example

Four validators, one holding 70% of the stake and three holding 10% each:

| Count                | Value                                               |
|----------------------|-----------------------------------------------------|
| Online accounts      | \\(N = 4\\)                                         |
| Entropy equivalent   | \\(N_{H} = e^{0.940} \approx 2.56\\)                |
| HHI equivalent       | \\(N_{HHI} = 1 / 0.52 \approx 1.92\\)               |

Four validators, as decentralized as about two and a half equal ones by entropy,
or two by HHI, which is most sensitive to the dominant one.

> [!NOTE]
> An entity can control many accounts: the effective numbers count accounts
> holding at least the threshold, and are an upper bound for the entities
> behind them.

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
