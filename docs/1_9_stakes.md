# Stake Decentralization

---

Since in PoS the probability of being elected as block proposer or validator is
directly proportional to validators' stakes, the distribution of such stake
into the system has a fundamental role on PoS decentralization.

We will say that the stake is _"completely decentralized"_ if and only if:

1. All the stake in circulation is taking part to the PoS validation;
1. All the validators participating in PoS validation hold the same amount of
stake.

Statement 1. essentially measures stake participation rate in PoS validation
and could be easily quantified as:

\\[ p = \frac{validation  stake}{circulating  stake} \\]

that can theoretically range from 0 (no participation in PoS validation) to 1
(complete participation in PoS validation).

Statement 2. essentially measures validators' inequality. We could borrow from
Macroeconomics several well-known wealth inequality or concentration indexes,
suc as: the [Gini Index](https://en.wikipedia.org/wiki/Gini_coefficient), the [Theil Indexes](https://en.wikipedia.org/wiki/Theil_index) or the
[Herfindahl–Hirschman Index](https://en.wikipedia.org/wiki/Herfindahl%E2%80%93Hirschman_Index). Those indexes are indicators of
concentration, used mainly to measure the degree of inequality in a society or
the degree of competition in a given market.

## Gini Index

_Gini Index_ is a measure of statistical dispersion intended to represent the
wealth inequality within a nation or any other group of people.

Given a wealth distribution \\(S\\) over a population of \\(N\\) agents, the
Simple Gini Index \\(GI\\) can be calculated as:

\\[ GI(S) = \frac{2}{N} \frac{\sum_{i=1}^{N} i y_i}{\sum_{i=1}^{N} y_i} - \frac{N+1}{N} \\]

where \\( y_1 \le y_2 \le ... \le y_N\\) are the sorted individuals' incomes.

It can theoretically range from 0 (_complete equality_) to 1 (_complete
inequality_).

## Theil Indexes

_Theil's Indexs_, called _Theil's L_ and _Theil's T_, measure the inequality of
a wealth distribution \\(S\\) over a population of \\(N\\) agents, with
different sensitivities:

* _Theil's L_ is sensitive to differences at the lower end of the distribution
(small ALGO amounts):

\\[ T_L = \frac{1}{N} \sum_{i=1}^{N} \frac{y_i}{\mu} \ln{\left(\frac{y_i}{\mu}\right)} \\]

* _Theil's T_ is more sensitive to differences at the top of the distribution
(large ALGO amounts):

\\[ T_T = \frac{1}{N} \sum_{i=1}^{N} \ln{\left(\frac{\mu}{y_i}\right)} \\]

where \\(y_i\\) is the individual's income and \\(\mu\\) is the mean income:

\\[ \mu = \frac{1}{N} \sum_{i=1}^{N} y_i\\]

Both can theoretically range from 0 (_complete equality_) to \\( +\infty \\)
(_complete inequality_) and represent two different evaluations of inequality,
based on what we tend to consider worse: having even a few small ALGO amounts
among many large ones or having even only a very few large ALGO amounts among
many small ones.

## Herfindahl–Hirschman Index

_Herfindahl–Hirschman Index_ is another indicator of concentration, mainly used
to measure the degree of competition in a given market.

\\[ HHI = \sum_{i=1}^{N} {s_i}^2 \\]

where \\(s\\) is the market share of firm \\(i\\) in the total market \\(S\\)
(or, in our case, the stake share of the validator \\(i\\) in the total
validating stake \\(S\\)), and \\(N\\) is the number of firms (or, in our case,
the total number of validators).

It can theoretically range from 0 (_perfectly competitive market_) to 1
(_monopoly_).

The \\(HHI\\) takes into account both the stake distribution among the
validators accounts and the absolute number of validators accounts. This is
accomplished by taking a summation of the square of each participant's stake
percentage.

* **Example 1**: the largest validator holds 80% of the stake, the next 5 largest
validators hold 2% each, the reminder is equally distributed among 10
validators:

\\[ HHI = {0.80}^2 + 5 \cdot {0.02}^2 + 10 \cdot {0.01}^2 = 0.643 \\]

* **Example 2**: the 6 largest validators hold 15% of the stake each, the reminder
is equally distributed among 10 validators:

\\[ HHI = 6 \cdot {0.15}^2 + 10 \cdot {0.01}^2 = 0.136 \\]

* **Example 3**: All the stake is equally distributed among 20 validators:

\\[ HHI = 20 \cdot {0.05}^2 = 0.005 \\]

* **Example 4**: All the stake is equally distributed among 100 validators:

\\[ HHI = 100 \cdot {0.01}^2 = 0.001 \\]

For sake of completenss we will evaluate all the indexes.
