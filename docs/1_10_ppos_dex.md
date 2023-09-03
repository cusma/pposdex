# Pure Proof of Stake Decentralization Index

---

The ALGO has a **total supply of 10B**, hardcoded in the genesis block, that will
flow into the ecosystem according to the
[Algorand Dynamics](https://algorand.foundation/the-algo/algo-dynamics) and
spread across participants according to their economical choices.

Since the probability of being elecetd as block proposer or as member of the
committee of validator is **directly proportional to user's ALGO online stake**,
the distribution of ALGOs into the ecosystem has a foundamental role on PPoS
decentralization.

Let's try first to define an **ideal theoretical conditions of decentralization**.
Then, everything deviating from those conditions will make
PPoS more real and far from platonic ideality.

### Definitions

We will say that PPoS is **"completely decentralized"** if and only if:

1. All the ALGO genesis supply is circulating in the ecosystem;
2. All the ALGO circulating supply is taking part to the PPoS;
3. All the accounts that owns ALGOs are taking part to PPoS;
4. All the accounts participating in PPoS hold the same amount of ALGO;

Now we need to **quantify each of these 4 statements** to express "how far" we are
with respect the purely theoretical decentralization.

1. `ALGO DYNAMICS = circulating supply / total supply`

    * 0 = no ALGO circulation
    * 1 = complete ALGO circulation

2. `ALGO ONLINE STAKE = total online stake / circulating supply`

   * 0 = no PPoS participation
   * 1 = complete PPoS participation

3. `ONLINE ACCOUNTS = online accounts / existing accounts`

    * 0 = no PPoS participation
    * 1 = complete PPoS participation

The statement 4. essentialy implies a measurement of participating accounts'
inequality. So, we will adopt well-know wealth inequality or concentration
indexes from Macroeconomics field: the [Gini's Index](https://en.wikipedia.org/wiki/Gini_coefficient),
the [Theil's Index](https://en.wikipedia.org/wiki/Theil_index) and the
[Herfindahl–Hirschman Index](https://en.wikipedia.org/wiki/Herfindahl%E2%80%93Hirschman_Index).

**Gini's Index** is a measure of statistical dispersion intended to represent
the wealth inequality within a nation or any other group of people. It can
theoretically range from 0 (complete equality) to 1 (complete inequality).

4. `PPoS GINI INDEX`

    * 1 = complete PPoS inequality
    * 0 = complete PPoS equality

In order to express our PPoS Decentralization Index homogeneously **we will
consider Gini's Index complement** (rather than its original form) in letter
calculations.

**Theil's Indexs** are called **Theil's L** and **Theil's T**, they also
measure the inequality of a distribution among a set of peoples but with
different sensitivity:

* `THEIL's L INDEX` is sensitive to differences at the lower end of the
  distribution (small ALGO amounts);

* `THEIL's T INDEX` is more sensitive to differences at the top of the
  distribution (large ALGO amounts);

both can theoretically range from 0 (complete equality) to +inf (complete
inequality) and represent two different evaluations of inequality, based on
what we tend to consider worse: having even a few small ALGO amounts among
many large ones or having even only a very few large ALGO amounts among many
small ones.

**Herfindahl–Hirschman Index (HHI)** is another indicator of concentration, used
mainly to measure the degree of competition in a given market. It can
theoretically range from 0 (perfectly competitive market) to 1 (monopoly).

* `ALGO HHI INDEX` considers all ALGO stakes, whether they participate in
  the PPoS or not;

* `PPoS HHI INDEX` considers only ALGO stakes that are participatinf in the
  PPoS;

For sake of completenss we will evaluate them all.

### PPoS Dex Index

Combining all the 4 statements, we know "how far" PPoS is from its purely
theoretical decentralization.

So we will measure this distance form ideality as:

* `PPoS DEX INDEX V3 = ALGO DYNAMICS * ALGO ONLINE STAKE * ONLINE ACCOUNTS * (1 - PPoS HHI)`

  * 0 = complete PPoS centralization
  * 1 = complete PPoS decentralization

Being aware that the PPoS only tends to the ideal condition, never reaching it.

> ⚠️ _NOTE: PPoS Dex Index V1 and V2 were based on PPoS Gini Index instead of PPoS HHI._
