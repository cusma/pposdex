# Stake Decentralization

---

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
among validators, a PoS consenus could still be _centralized_ due to the concentrarion
of stake in a few accounts. So an additional _Account Participation Index_ (\\(A_P\\))
is introduced.

Therefore:

\\[ d_S = S_P \cdot S_I \cdot A_P \\]

## Stake Participation Index

The _Stake Participation Index_ (\\(S_P\\)) measures stake participation rate in
PoS validation. It can be quantified as:

\\[ S_P = S_{dyn} \cdot S_{p}\\]

Where:

* _Stake Dynamics_ \\(S_{dyn}\\): is the fraction of _ciruclating supply_ (\\(S_c\\))
over the _genesis supply_ (\\( S_g\\)) (only applies to fixed genesis supply Blockchains);
* _Stake Participation_ \\(S_{p}\\): is the fraction of _validation supply_ (\\(S_v\\))
over the _circulating supply_ (\\( S_c\\)).

It can theoretically range from 0 (no participation in PoS validation) to 1 (complete
participation in PoS validation).

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

It can theoretically range from 0 (_complete equality_) to 1 (_complete inequality_),
therefore it _one’s complement_ \\(1 - GI(S)\\) is a good candidate for the \\(DEX\\)
index.

### Theil Indexes

_Theil's Indexs_, called _Theil's L_ and _Theil's T_, measure the inequality of
a wealth distribution \\(S\\) over a population of \\(N\\) agents, with different
sensitivities:

* _Theil's L_ is more sensitive to differences at the lower end of the distribution
(small stakes):

\\[ T_L = \frac{1}{N} \sum_{i=1}^{N} \frac{y_i}{\mu} \ln{\left(\frac{y_i}{\mu}
\right)} \\]

* _Theil's T_ is more sensitive to differences at the top of the distribution (large
stakes):

\\[ T_T = \frac{1}{N} \sum_{i=1}^{N} \ln{\left(\frac{\mu}{y_i}\right)} \\]

where \\(y_i\\) is the validator's stake and \\(\mu\\) is the mean stake:

\\[ \mu = \frac{1}{N} \sum_{i=1}^{N} y_i\\]

Both can theoretically range from 0 (_complete equality_) to \\( +\infty \\) (_complete
inequality_) and represent two different evaluations of inequality, based on what
we tend to consider worse: having even a few small stakes among many large ones
or having even a few large stakes among many small ones.

> _Theil’s Indexes_ are not upper bounded they are not good candidate for the \\(DEX\\)
> index. For sake of completeness we will evaluate them separately.

### Herfindahl–Hirschman Index

_Herfindahl–Hirschman Index_ is another indicator of concentration, mainly used
to measure the degree of competition in a given market.

Given a wealth stake \\(S\\) over a set of \\(N\\) validators, the \\(HHI\\) index
can be calculated as:

\\[ HHI(S) = \sum_{i=1}^{N} {s_i}^2 \\]

where \\(s\\) is the stake share of validator \\(i\\) in the total validating stake
\\(S\\).

It can theoretically range from 0 (_perfectly competitive market_) to 1 (_monopoly_),
therefore it _one’s complement_ \\(1 - GI(S)\\) is a good candidate for the \\(DEX\\)
index.

> The \\(HHI\\) implicitly considers both the stake distribution among the validators
> accounts and the _absolute number of validators accounts_. Therefore, in order
> to avoid double counting of the _account participation_ factor, \\(A_P = 1\\)
> when \\(S_I = 1 - HHI\\).

### Example 1

The largest validator holds 80% of the stake, the next 5 largest validators hold
2% each, the reminder is equally distributed among 10 validators:

\\[ HHI = {0.80}^2 + 5 \cdot {0.02}^2 + 10 \cdot {0.01}^2 = 0.643 \\]

### Example 2

The 6 largest validators hold 15% of the stake each, the reminder is equally distributed
among 10 validators:

\\[ HHI = 6 \cdot {0.15}^2 + 10 \cdot {0.01}^2 = 0.136 \\]

### Example 3

All the stake is equally distributed among 20 validators:

\\[ HHI = 20 \cdot {0.05}^2 = 0.005 \\]

### Example 4

All the stake is equally distributed among 100 validators:

\\[ HHI = 100 \cdot {0.01}^2 = 0.001 \\]

## Account Participation Index

The _Account Participation Index_ (\\(A_P\\)) represents the fraction of _validator
accounts_ (\\(A_v\\)) over the _total accounts_ (\\( A_{tot}\\)):

\\[ A_P = \frac{A_v}{A_{tot}} \\]

It can theoretically range from 0 (no account participating in PoS validation)
to 1 (all existing accounts participating in PoS validation).

> In _account-based_ Blockchains (like Algorand), accounts are identified by _public
> keys_. Permissionless and public networks are pseudonymous by design, therefore
> there is no way to assert if different public keys belong to different users.
> We assume that each public key belongs to a different participant in the PPoS
> consensus, with their own skin in the game.

---
