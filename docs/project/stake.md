# Stake Decentralization

Since in PoS the probability of being elected as a block proposer or as a validator
is directly proportional to validators' stakes, the distribution of such stake
into the system is the last fundamental factor of PoS Blockchains decentralization.

We will say that the stake is _"completely decentralized"_ (\\(d_S = 1\\)) if and
only if:

1. All the stake in circulation is participating in the PoS validation;
1. All the validators participating in PoS validation hold the same amount of stake.

The first condition is quantified by the _Stake Participation Index_ (\\(S_P\\))
while the second conditions is quantified by the _Stake Inequality Index_ (\\(S_I\\)).

One could still argue that even if all the participating stake is equally distributed
among validators, a PoS consensus could still be _centralized_ due to the concentration
of stake in a few accounts. So an additional _Account Participation Index_ (\\(A_P\\))
is introduced.

Therefore:

\\[ d_S = S_P \cdot S_I \cdot A_P \\]

## Stake Participation Index

The _Stake Participation Index_ (\\(S_P\\)) measures stake participation rate in
PoS validation. It can be quantified as:

\\[ S_P = S_{dyn} \cdot S_{p}\\]

Where:

* _Stake Dynamics_ \\(S_{dyn}\\): is the fraction of _circulating supply_ (\\(S_c\\))
over the _genesis supply_ (\\( S_g\\)). It only applies to fixed genesis supply
Blockchains;
* _Stake Participation_ \\(S_{p}\\): is the fraction of _validation supply_ (\\(S_v\\))
over the _circulating supply_ (\\( S_c\\)).

\\(S_P\\) can theoretically range from 0 (no participation in PoS validation)
to 1 (complete participation in PoS validation).

How the circulating supply is measured depends on the Blockchain: see the
[PPoS Dex](ppos-dex.md) for Algorand.

> [!NOTE]
> On Algorand, \\(S_{dyn}\\) has reached 0.98 and barely moves anymore: the
> stake participation \\(S_{p}\\) drives \\(S_P\\).

## Stake Inequality Index

The _Stake Inequality Index_ (\\(S_I\\)) measures validators' inequality. We can
borrow from Macroeconomics well-known wealth inequality or concentration indexes,
such as: the [Gini Index](https://en.wikipedia.org/wiki/Gini_coefficient),
the [Theil Indexes](https://en.wikipedia.org/wiki/Theil_index)
or the [Herfindahl–Hirschman Index](https://en.wikipedia.org/wiki/Herfindahl%E2%80%93Hirschman_Index).
Those indexes are indicators of concentration, used mainly to measure the degree
of inequality in a society or the degree of competition in a given market.

### Gini Index

_Gini Index_ is a measure of statistical dispersion intended to represent the wealth
inequality within a nation or any other group of people.

Given a stake distribution \\(S\\) over a set of \\(N\\) validators, the _Simple
Gini Index_ \\(GI\\) can be calculated as:

\\[ GI(S) = \frac{2}{N} \frac{\sum_{i=1}^{N} i y_i}{\sum_{i=1}^{N} y_i} -
\frac{N+1}{N} \\]

where \\( y_1 \le y_2 \le ... \le y_N\\) are the sorted validators' stake.

\\(GI\\) can theoretically range from 0 (_complete equality_) to 1 (_complete inequality_),
therefore it _one’s complement_ \\((1 - GI)\\) is a good candidate for the \\(DEX\\)
index.

> [!NOTE]
> On Algorand, the Gini Index tracks how many small validators take part more
> than how concentrated the stake is: it rises when small validators join. It
> stayed flat through the January 2025 surge, when online accounts grew fivefold
> and the [effective number of validators](#effective-number-of-validators)
> tripled.

### Theil Indexes

_Theil's Indexes_, called _Theil's L_ and _Theil's T_, measure the inequality of
a stake distribution \\(S\\) over a set of \\(N\\) validators, with different
sensitivities:

* _Theil's L_ is more sensitive to differences at the lower end of the distribution
(small stakes):

\\[ T_L = \frac{1}{N} \sum_{i=1}^{N} \ln{\left(\frac{\mu}{y_i}\right)} \\]

* _Theil's T_ is more sensitive to differences at the top of the distribution (large
stakes):

\\[ T_T = \frac{1}{N} \sum_{i=1}^{N} \frac{y_i}{\mu} \ln{\left(\frac{y_i}{\mu}
\right)} \\]

where \\(y_i\\) is the validator's stake and \\(\mu\\) is the mean stake:

\\[ \mu = \frac{1}{N} \sum_{i=1}^{N} y_i\\]

Both \\(T_L\\) and \\(T_T\\) can theoretically range from 0 (_complete equality_)
to \\( +\infty \\) (_complete inequality_) and represent two different evaluations
of inequality, depending on what we tend to consider worse: having even a few small
stakes among many large ones or having even a few large stakes among many small
ones.

> [!NOTE]
> _Theil’s Indexes_ are not upper bounded, so are not good candidates for the \\(DEX\\)
> index. For sake of completeness we will evaluate them separately.
>
> Theil's T is the gap between the maximum entropy, \\(\ln N\\), and the entropy
> of the stake: it grows with the number of validators, even when the stake
> spreads across more of them. The [entropy equivalent](#entropy-equivalent)
> turns it into a count that does not.

### Herfindahl–Hirschman Index

_Herfindahl–Hirschman Index_ is another indicator of concentration, mainly used
to measure the degree of competition in a given market.

Given a stake distribution \\(S\\) over a set of \\(N\\) validators, the \\(HHI\\)
index can be calculated as:

\\[ HHI(S) = \sum_{i=1}^{N} {s_i}^2 \\]

where \\(s_i\\) is the stake share of validator \\(i\\) in the total validating
stake \\(S\\).

\\(HHI\\) can theoretically range from 0 (_perfectly competitive market_) to 1
(_monopoly_), therefore it _one’s complement_ \\((1 - HHI)\\) is a good candidate
for the \\(DEX\\) index.

> [!NOTE]
> The \\(HHI\\) implicitly considers both the stake distribution among the validators
> accounts and the _absolute number of validators accounts_. Therefore, in order
> to avoid double counting of the _account participation_ factor, \\(A_P = 1\\)
> when \\(S_I = 1 - HHI\\).
>
> On Algorand, \\(1 - HHI\\) stays between 0.96 and 0.99, so it barely moves:
> the [HHI equivalent](#hhi-equivalent) reads its changes better.

### Effective Number of Validators

Counting the validators tells how many there are, not how much each one weighs
in consensus: a thousand validators where one holds almost all the stake are
barely more decentralized than a single validator.

The _effective number of validators_ answers a more telling question: how many
validators, all holding the _same_ stake, would be exactly as decentralized as
the actual ones? With equal stakes it is the number of validators, and it drops
as the stake concentrates, down to 1 when a single validator holds it all.

#### Entropy Equivalent

The entropy of the stake measures how uncertain it is which validator holds a
randomly picked unit of stake. Given the stake shares \\(s_i\\) of the \\(N\\)
validators:

\\[ H(S) = - \sum_{i=1}^{N} s_i \ln s_i \\]

With \\(n\\) equal stakes the entropy is \\(\ln n\\), so a distribution with
entropy \\(H\\) is as diverse as \\(e^H\\) equal validators: its _entropy
equivalent_. Since the Theil T index is how far the entropy is from its maximum,
\\(T_T(S) = \ln N - H(S)\\), it can be computed as:

\\[ N_{H} = e^{H(S)} = N \cdot e^{-T_T(S)} \\]

#### HHI Equivalent

\\(n\\) equal stakes have \\(HHI = 1/n\\), so the _HHI equivalent_ is:

\\[ N_{HHI} = \frac{1}{HHI(S)} \\]

Squaring the shares weighs the largest stakes more, so the HHI equivalent is
always the lowest of the three counts:

\\[ N \geq N_{H} \geq N_{HHI} \\]

> [!NOTE]
> A participant can control many accounts: counting accounts, the effective
> numbers are an upper bound for the participants behind them.

#### Stake Evenness

The effective numbers grow both with how many validators there are and with how
evenly they share the stake. Their ratios keep the evenness alone: a network ten
times larger, with stakes shared the same way, has the same ratios.

The _overall evenness_ is the entropy equivalent as a share of the validators:

\\[ E = \frac{N_H}{N} = e^{-T_T(S)} \\]

so the entropy equivalent is the number of validators times their evenness,
\\(N_H = N \cdot E\\). The _top evenness_ is the HHI equivalent as a share of the
entropy equivalent:

\\[ E_{top} = \frac{N_{HHI}}{N_H} \\]

Both are 1 when all the validators hold the same stake, and lower the less even
the stake is. Small validators joining lower the overall evenness, as they
raise the Theil T index, and the top evenness less: the HHI weighs them little,
so the top evenness tells how much the largest validators outweigh the rest. In
ecology, where they measure the diversity of species, these ratios are the
evenness of the Hill numbers.

> [!IMPORTANT]
> Evenness is not decentralization: it ignores how many validators there are.
> 20 equal validators are as even as 100, and a single validator holding 80% of
> the stake is more even at the top than one holding 30% among 70 small ones:
> see the [examples](#examples). Read it next to the effective numbers, not as
> a score.

### Nakamoto Coefficient

The _Nakamoto Coefficient_ (\\(NC\\)) counts the fewest validators holding
together more than a share \\(q\\) of the stake: the smallest coalition able to
threaten the consensus. Given the validators' stakes sorted from the largest,
\\( y_1 \ge y_2 \ge ... \ge y_N\\):

\\[ NC_q(S) = \min \left\\{ k : \sum_{i=1}^{k} y_i > q \sum_{i=1}^{N} y_i
\right\\} \\]

Unlike the inequality indexes, it measures the stake against the thresholds of
the consensus. On Algorand, four thresholds matter:

| Coefficient | Threshold        | Meaning                                                                            |
|-------------|------------------|------------------------------------------------------------------------------------|
| Veto        | \\(NC_{10\\%}\\) | A coalition above it can block protocol upgrades                                   |
| Liveness    | \\(NC_{20\\%}\\) | A coalition above it can stall the consensus by not voting, conservatively         |
| Nakamoto    | \\(NC_{33\\%}\\) | A coalition above it breaks the honest majority assumption of the consensus        |
| Upgrade     | \\(NC_{90\\%}\\) | How many accounts it takes to reach the broad supermajority protocol upgrades need |

Together they are the [PPoS Dex v3](ppos-dex.md#ppos-dex-v3). The higher the
threshold, the more accounts it takes:
\\(NC_{10\\%} \le NC_{20\\%} \le NC_{33\\%} \le NC_{90\\%}\\).

Accounts rekeyed to the same address, or registering their participation keys
with the same validity window, are likely run by the same operator. Merging
them gives the _Nakamoto Coefficient of operators_: a heuristic, lower than or
equal to the accounts one.

> [!TIP]
> [Related projects](../data/related-projects.md) look at these thresholds from
> other angles: [Valar Decentralization](https://decentralization.valar.solutions/)
> names the operators the heuristic cannot see, like custodians and staking
> providers running many accounts; [Partlife](https://partlife.app/) shows when
> the participation keys of the online accounts expire, a risk to liveness; and
> [Ⱥ Surf Upgrades](https://algo.surf/upgrades) shows how each consensus upgrade
> reached its supermajority.

### Examples

Six stake distributions, from a single dominant validator to 100 equal ones:

1. _One at 80%_: the largest validator holds 80% of the stake, the next 5 hold
   2% each, the remaining 10 hold 1% each;
1. _Six at 15%_: the 6 largest validators hold 15% each, the remaining 10 hold
   1% each;
1. _20 equal_: 20 validators hold 5% each;
1. _One at 30%_: the largest validator holds 30% of the stake, the remaining 70
   hold 1% each: a whale among many small validators;
1. _20 large, 80 small_: 20 validators hold 4% each, 80 hold 0.25% each: a long
   tail, the shape of real networks;
1. _100 equal_: 100 validators hold 1% each.

![Examples: who holds the stake, each validator a rectangle sized by its stake](../images/examples/stakes.svg)

Compared by every metric:

| Metric                       | 1. One at 80% | 2. Six at 15% | 3. 20 equal | 4. One at 30% | 5. 20 large, 80 small | 6. 100 equal |
|------------------------------|--------------:|--------------:|------------:|--------------:|----------------------:|-------------:|
| Validators \\(N\\)           |            16 |            16 |          20 |            71 |                   100 |          100 |
| Gini \\(GI\\)                |         0.769 |         0.525 |           0 |         0.286 |                 0.600 |            0 |
| Theil L \\(T_L\\)            |          1.34 |          0.82 |           0 |          0.29 |                  0.83 |            0 |
| Theil T \\(T_T\\)            |          1.74 |          0.61 |           0 |          0.68 |                  0.83 |            0 |
| HHI                          |         0.643 |         0.136 |        0.05 |         0.097 |                0.0325 |         0.01 |
| Entropy equivalent \\(N_H\\) |           2.8 |           8.7 |          20 |          36.0 |                  43.5 |          100 |
| HHI equivalent \\(N_{HHI}\\) |           1.6 |           7.4 |          20 |          10.3 |                  30.8 |          100 |
| Overall evenness \\(E\\)     |          0.18 |          0.55 |           1 |          0.51 |                  0.44 |            1 |
| Top evenness \\(E_{top}\\)   |          0.56 |          0.84 |           1 |          0.29 |                  0.71 |            1 |
| Veto \\(NC_{10\\%}\\)        |             1 |             1 |           3 |             1 |                     3 |           11 |
| Liveness \\(NC_{20\\%}\\)    |             1 |             2 |           5 |             1 |                     6 |           21 |
| Nakamoto \\(NC_{33\\%}\\)    |             1 |             3 |           7 |             5 |                     9 |           34 |
| Upgrade \\(NC_{90\\%}\\)     |             7 |             7 |          19 |            62 |                    61 |           91 |

The Nakamoto Coefficients are where the stake of the largest validators crosses
each threshold:

![Examples: the stake of the largest validators against the four thresholds](../images/examples/coalitions.svg)

The inequality indexes cannot tell 20 equal validators from 100: both are
perfectly equal. The effective numbers and the Nakamoto Coefficients can: they
grow with how many validators share the stake, from less than 3 to 100, and from
a single validator able to threaten the consensus to dozens.

The whale shows what the inequality indexes miss: with a Gini Index of 0.29 and
an entropy equivalent of 36, its stake looks widely shared, yet a single
validator is enough to veto an upgrade and to stall the consensus. The HHI
equivalent, the top evenness and the Veto and Liveness Coefficients show it.

The long tail shows the opposite blind spot: adding 80 small validators to 20
large ones takes the Gini Index from 0 to 0.6, as if the stake had concentrated,
while every count of validators grows. The [Snapshot](../data/snapshot.md)
shows where the real network stands.

![Examples: validators and their entropy and HHI equivalents](../images/examples/effective_numbers.svg)

## Account Participation Index

The _Account Participation Index_ (\\(A_P\\)) represents the fraction of _validator
accounts_ (\\(A_v\\)) over the _total accounts_ (\\( A_{tot}\\)):

\\[ A_P = \frac{A_v}{A_{tot}} \\]

It can theoretically range from 0 (no account participating in PoS validation)
to 1 (all existing accounts participating in PoS validation).

> [!NOTE]
> On Algorand, the accounts holding ALGO grow faster than the online ones: the
> index fell from 1.6% to 1% between 2021 and 2026, while the online accounts
> grew sixfold.

> [!IMPORTANT]
> In _account-based_ Blockchains (like Algorand), accounts are identified by _public
> keys_. Permissionless and public networks are pseudonymous by design, therefore
> there is no way to assert if different public keys belong to different users.
> We assume that each public key belongs to a different participant in the PPoS
> consensus, with their own skin in the game.
