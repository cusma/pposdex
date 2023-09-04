# Pure Proof of Stake Decentralization Index

---

The ALGO has a **total supply of 10B**, hardcoded in the genesis block, that will
flow into the ecosystem according to the
[Algorand Dynamics](https://algorand.foundation/the-algo/algo-dynamics) and
spread across participants according to their economical choices.

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

* `ALGO HHI INDEX` considers all ALGO stakes, whether they participate in
  the PPoS or not;

* `PPoS HHI INDEX` considers only ALGO stakes that are participatinf in the
  PPoS;

In order to express our PPoS Decentralization Index homogeneously **we will
consider Gini's Index complement** (rather than its original form) in letter
calculations.

### PPoS Dex Index

Combining all the 4 statements, we know "how far" PPoS is from its purely
theoretical decentralization.

So we will measure this distance form ideality as:

* `PPoS DEX INDEX V3 = ALGO DYNAMICS * ALGO ONLINE STAKE * ONLINE ACCOUNTS * (1 - PPoS HHI)`

  * 0 = complete PPoS centralization
  * 1 = complete PPoS decentralization

Being aware that the PPoS only tends to the ideal condition, never reaching it.

> ⚠️ _NOTE: PPoS Dex Index V1 and V2 were based on PPoS Gini Index instead of PPoS HHI._
