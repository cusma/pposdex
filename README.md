```
 _______  _______           ______    ______                   
|_   __ \|_   __ \        .' ____ \  |_   _ `.                
  | |__) | | |__) | .--.  | (___ \_|   | | `. \ .---.  _   __ 
  |  ___/  |  ___// .'`\ \ _.____`.    | |  | |/ /__ \[ \ [  ]
 _| |_    _| |_   | \__. || \____) |  _| |_.' /| \__., > '  < 
|_____|  |_____|   '.__.'  \______.' |______.'  '.__.'[__]`\_]

Algorand Pure Proof of Stake Decentralization Index (by cusma)
```

# PPoS Dex: Algorand Pure Proof of Stake Decentralization Index monitoring
## What's PPoS Dex?
**PPoS Dex** is a CLI tool with which you can monitor Algorand Pure
Proof of Stake Decentralization Index. The application is ment to be
fully trustless, so you can autonomulsy read Algorand blockchain, do
your math and publish your indexes evaluation on-chain if you want.

Otherwise, if you prefer, you can simply use the data provided by
[PPoS Dex Oracle](https://algoexplorer.io/address/WIPE4JSUWLXKZZK6GJ6VI32PX6ZWPKBRH5YFRJCHWOVC73P5RI4DGUQUWQ).

PPoS Dex plots nice data analytics too (some examples later in this README).

So what **"Decentralization Index"** actually means?

##### Disclaimer
PPoS Dex has not been audited nor officially approved by the Algorand Foundation.
This tool is ment to be only a personal attempt to provide to Algorand community
some stats on the evolution of their ecosystem. **Algorand's decentralization is a
common good**, but it will not happen by itself: the community as a whole should
embrace the path towards the decentalization jointly with the Algorand Foundation,
commiting to preserve it.

## Introduction
Blockchain technology arose to fulfil the promise of the genesis and transfer of
digital native value in disintermediated, safe, decentralized and scalable way.
Billions of people on the planet would have the possibility of transacting
without borders or barriers within a unique global distributed computational
infrastructure that cancel out the needing of third trusted parties in between.

As well as exchange of digital information in the Internet era relies on
Communication Protocols, the **exchange of digital value relies on Consensus
Protocols**: combining distributed computation, cryptography and game theory
into a mathematical equilibrium the **Consensus Protocols are the engines that
power Blockchains**, keeping the history of digital value unique, consistent
and tamper proof within a single distributed data ledger on a global scale.

Blockchains' technological performances depend on their Consensus Protocols.
At the beginning of this technological journey the so-called Proof of Work
(PoW) consensus protocols powered the first generation of Blockchains, with the
merit of showing the existence of digital native value but at the same time
facing the limitation of their own foundation: running a planetary
computational battle one against the other just to validate the next block of
data takes a lot of time, with unacceptable waste of energy. In fact, like
"Proof of Work" suggests itself, showing off a personal commitment in the
ecosystem through the allocation of computational and energetic resources is at
the core of this consensus mechanism. However, Blockchains that run on PoW fail
in fulfilling the promise of scalability, decentralisation, transaction speed
and costs ending up relying on energetically inefficient centralised
computational farms.

**The planet Earth can no longer afford unsustainable technologies**.

Here is where Algorand steps in: thanks to the brilliant work of Prof. Silvio Micali,
a new orchestration of state-of-art distributed computation, cryptography
and game theory turned the original blockchains' aspirations into the brand new [Algorand Pure Proof
of Stake consensus protocol](https://developer.algorand.org/docs/algorand_consensus/).

### Algorand Pure Proof of Stake Consensus
Thanks to Algorand Pure Proof of Stake (PPoS) consensus mechanism, a unique
committee of users is randomly and secretly selected to approve every block,
through a [Verifiable Random Function](https://developer.algorand.org/docs/algorand_consensus/#verifiable-random-function)
(VRF). This cryptographic primitive acts like a fair, tamper proof, secure and
provable cryptographic sortition, in which users are free to take part as long
as they own any amount of Algorand's native cryptocurrency, named ALGO, registered
online as "participating". Each online ALGO could be seen as a ticket of
this cryptographic lottery, that runs secretely in parallel on Algorand network's
nodes, with minimal hardware requirements and neglectable energy consumption.

Algorand permissionless Consensus protocol solves blockchains' trilemma
acheiving at the same time:

1. Scalability
2. Security
3. Decentralization

**The point is: can we measure these properites?**

### Scalability
Scalability can be quantified in serveral ways:

- PPoS finalized transactions per second
- PPoS transactions cost
- PPoS power consumption
- PPoS node minimal hardware requirements

Thanks to its unique consensus protocol Algorand brings the number of finalized 
transactions per second from few dozen achieved by PoW up to 1000 and shrinks
the transactions' confirmation time form PoW’s dozen of minutes to just 4.5
seconds, with no waste of energy, neglectable transaction’s cost (0.001 ALGO)
and no hardware barriers. So we have quantitative evidence of Algorand scalability.

### Security
Quantify security is not that simple and out of the scope of this README.

### Decentralization
Users participating in Algorand Consensus do not delegate their votes, do not
need a minimum stake to take part in the PPoS and do not need to bond their
ALGO stake.

In fact, anyone willing to take part in Pure Proof of Stake consensus protocol
is welcome to do it, showing the real power of Algorand’s decentralization.

Algorand is both a digital and physical infrastructure made of:

- Software: in the form of Algorand native cryptocurrency (the ALGO), 
  representing the power that each member of the ecosystem may have over 
  the PPoS consenusm mechanism
    
- Hardware: in the form of a global network composed by [Relay Nodes 
  and Participation Nodes](https://developer.algorand.org/docs/run-a-node/setup/types/)

We will adopt the following hypotesis:

**Assumption 1**

We will not consider here the degree of geo-delocalization of the physical
infrastrucutre. More insights on this topic can be found [here](https://databricks.com/blog/2020/10/08/analyzing-algorand-blockchain-data-with-databricks-delta.html).

**Assumption 2**

Since a permissionless and public network is pseudonymous by design is there no
way to know if differents public keys belong to the same user. So, we will make
the assumption than **each public key belongs to a different participants in the
Algorand PPoS consensus**, with their own skin in the game.

So how can we quantify PPoS Decentralization? Here is a proposal.

## Pure Proof of Stake Decentralization Index
When mathematicians do not know equations' solutions or when physicists do
not how to measure physical properties, they usually start investigating if
that solutions or that properties have upper or lower bounds.

In order to reach a common understanding of what measuring decentralization
means in this proposal, we should agree on some definitions.

To do that we will go back to the comparison between Consenus Protocols and
engines we made in the **Introducion**, exploring the concept of efficiency of
a machine.

In 1842 the French physicist [Nicolas Léonard Sadi Carnot](https://en.wikipedia.org/wiki/Nicolas_L%C3%A9onard_Sadi_Carnot) discovered that the
efficecy of any classical thermodynamic engine, that converts heat into work
(or vice versa), **must be lower than a theoretical upper bound** represented by
the efficency of a purely ideal machine, named Carnot engine after him. Such as
"perfect" engine is a purely theoretical construct and cannot be built in
practice.

This is **probably the most elegant and general result in classical physics**, it
implies that any system undergoing any kind of thermodinamic cycle can only
tend to the efficiency of a Carnot engine operating under the same conditions,
but **will never reach it**, no matter how cleverly that system has been designed.

In the same way we will try to define an equivalent of a Carnot engine for the
PPoS consensus.

**Does such theoretical decentralization upper bound exsist?**

**When we should say that the Algorand PPoS consenus is completely decentralized?**

The ALGO has a **total supply of 10B**, hardcoded in the genesis block, that will
flow into the ecosystem according to the
[Algorand Dynamics](https://algorand.foundation/the-algo/algo-dynamics) and
spread across participants according their economical choices.

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
    
The statement 4. essentialy implies a measurement of accounts' inequality. So,
we will adopt well knows wealth inequality indexes from Macroeconomics field:
the [Gini's Index](https://en.wikipedia.org/wiki/Gini_coefficient) and
[Theil's Index](https://en.wikipedia.org/wiki/Theil_index).

**Gini's Index** can theoretically range from 0 (complete equality) to 1
(complete inequality).

4. `PPoS GINI INDEX`

    * 1 = complete PPoS inequality
    * 0 = complete PPoS equality
    
In order to express our measure homogeneously **we will consider Gini's
Index complement rather than its original form** in letter calculations.
   
**Theil's Indexs** are called **Theil's L** and **Theil's T**, they also measure the
inequality of a distribution among a set of peoples but with different
sensitivity:

- `Theil's L Index` is sensitive to differences at the lower end of the 
  distribution (small ALGO amounts)
  
- `Theil's T Index` is more sensitive to differences at the top of the 
  distribution (large ALGO amounts)
  
they can theoretically range from 0 (complete equality) to +inf (complete
inequality) and represent two different evaluations of inequality, based on
what we tend to consider worse: having even a few small ALGO amounts among
many large ones or having even only a very few large ALGO amounts among many
small ones.

For sake of completenss we will evaluate them both.

### PPoS Dex Index
Combining all the 4 statements we will know "how far" PPoS is from its purely
theoretical decentralization.

So we will measure this distance form ideality as:

- `PPoS DEX INDEX = ALGO DYNAMICS * ALGO ONLINE STAKE * ONLINE ACCOUNTS * (1 - PPoS GINI)`

    * 0 = complete PPoS centralization
    * 1 = complete PPoS decentralization
    
Being aware that the PPoS only tends to the ideal condition, never reaching it.

## Install PPoS Dex
### Step 1 - Python modules
PPoS Dex uses the following Python3 modules:
1. `msgpack`
2. `docopt`
3. `py-algorand-sdk`
4. `schema`
5. `matplotlib`

so you need to install them (if not already present):

```bash
$ pip3 install --upgrade msgpack
$ pip3 install --upgrade docopt
$ pip3 install --upgrade py-algorand-sdk
$ pip3 install --upgrade schema
$ pip3 install --upgrade matplotlib
```

### Step 2 - Clients
PPoS Dex interacts with Algorand blockchain both thorugh a Node and an Indexer.
You may want to choose:

1. Your local hosted Node and Indexer
2. A third party Node and Indexer services

PPoS Dex by default uses PureStake API as a service, so if you want
to avoid running your own Node and Indexer all you need to do is creating an
account on [PureStake](https://developer.purestake.io/) and get yout API token.

### Step 3 - PPoS files
Copy following PPoS Dex files on your machine:

1. `ppos_dex.py`
2. `ppos_dex_data.py`
3. `ppos_dex_plots.py`
4. `algo_query.py`
5. `inequality_indexes.py`

## Usage
Intreacting with PPoS Dex from your CLI is pretty easy, just ask for help:

**Input**
```bash
$ python3 ppos_dex.py --help
```
**Output**
```
Usage:
  ppos_dex.py publish <api-token> <publisher-mnemonic> [--local-host]
                      [--algod-address=<ca>] [--indexer-address=<ia>]
                      [--algo-threshold=<at>]
  ppos_dex.py plot <api-token> [--local-host] [--indexer-address=<ia>]
                   [--data-address=<da>] [--algo-threshold=<at>]
                   [--starting-block=<sb>] [--ending-block=<eb>]
  ppos_dex.py snapshot <api-token> [--local-host] [--indexer-address=<ia>]
                       [--data-address=<da>] [--algo-threshold=<at>]
                       [--starting-block=<sb>]
  ppos_dex.py export <api-token> [--local-host] [--indexer-address=<ia>]
                     [--data-address=<da>] [--algo-threshold=<at>]
                     [--starting-block=<sb>] [--ending-block=<eb>]
  ppos_dex.py [--help]

Commands:
  publish   Contribute publishing PPoS Decentralization Index data on chain.
  plot      Plots PPoS Decentralization Index evolution over time.
  snapshot  Plots latest PPoS Decentralization Index data.
  export    Exports PPoS Decentralization Index data to csv.

Options:
  --local-host                      Use your Algorand Node (default: PureStake)

  -c <ca> --algod-address=<ca>      Algod Client address
        [default: https://testnet-algorand.api.purestake.io/ps2].
  -i <ia> --indexer-address=<ia>    Indexer Client address
        [default: https://testnet-algorand.api.purestake.io/idx2].
  -t <at> --algo-threshold=<ta>     Algo minimum balance to query
        [default: 1000].
  -a <da> --data-address=<da>       Algorand address data source
        [default: 2EJ4FCM5XVVNTRCP44GQIJIFG2O2MI3C3R47VZZSNVZZKZE3GVPJCDY4MA].
  -s <sb> --starting-block=<sb>     Data starting block (int)
        [default: 11476070].
  -e <eb> --ending-block=<eb>       Data ending block (int)

  -h --help
```

### Publish PPoS Dex data
Contribute publishing trustless reliable data on Algorand blockchain paying
just the minimum network fee (currently 0.001 ALGO).

**Input**
```bash
$ python3 ppos_dex.py publish <your-api-token> <your-mnemonic>
```
**Options**
1. `[--local-host]` select your local hosted Node and Indexer;
2. `[--algod-address=<ca>]` address of your local Algod Client;
3. `[--indexer-address=<ia>]` address of your local Indexer Client;
4. `[--algo-threshold=<at>]` consider only accounts that own more than this threshold (default: 1000 ALGO);

Is worth noting that lower values of `[--algo-threshold=<at>]` will require more
querying efforts, so you should avoid going under default threshold,
expecially if you are using a third party API service.

**Output**
```bash
{
  "algo_threshold": 1000,
  "accounts": 13346,
  "algo_dynamics": 0.3741854092978301,
  "ppos_online_stake": 0.598241416943984,
  "ppos_online_accounts": 0.01715869923572606,
  "ppos_gini": 0.829793933948626,
  "ppos_theil_l": 4.640220128476622,
  "ppos_theil_t": 1.5593480873810057,
  "ppos_dex": 0.0006537665878508702,
  "timestamp": "2021-01-06 00:22:09.607573"
}
```

You can then find your result published on-chain ([example](https://algoexplorer.io/tx/NPAAMBUEAIIYJJDFZWMYAHJBBSXDO2PV5TTSCD3SKWNBCLOU2AYA)).

### Plot PPoS Dex timeseries
Plot PPoS Dex Index timeseries data published by PPoS Dex Oracle (or by
yourself).

**Input**
```bash
$ python3 ppos_dex.py plot <your-api-token>
```
**Options**
1. `[--local-host]` select your local hosted Node and Indexer;
2. `[--indexer-address=<ia>]` address of your local Indexer Client;
3. `[--data-address=<da>]` publisher account address (default: PPoS Dex Oracle account);
4. `[--algo-threshold=<at>]` plot only data of accounts that own more than this threshold (default: 1000 ALGO);
5. `[--starting-block=<sb>]` plot data from this block (if availables);
6. `[--ending-block=<eb>]` plot data until this block;

**Output**
![](images/timeseries_ppos_dynamics.png)

![](images/timeseries_ppos_distribution.png)

### Plot PPoS Dex snapshot
Take a snapshot of PPoS Dex Index data published by PPoS Dex Oracle (or by
yourself).

**Input**
```bash
$ python3 ppos_dex.py snapshot <your-api-token>
```
**Options**
1. `[--local-host]` select your local hosted Node and Indexer;
2. `[--indexer-address=<ia>]` address of your local Indexer Client;
3. `[--data-address=<da>]` publisher account address (default: PPoS Dex Oracle account);
4. `[--algo-threshold=<at>]` plot only data of accounts that own more than this threshold (default: 1000 ALGO);
5. `[--starting-block=<sb>]` plot data from this block (if availables);

**Output**
![](images/snapshot_ppos_dynamics.png)

![](images/snapshot_ppos_distribution.png)

### Export Plot PPoS Dex data
Export PPoS Dex Index data published by PPoS Dex Oracle (or by yourself) to csv file.

**Input**
```bash
$ python3 ppos_dex.py export <your-api-token>
```
**Options**
1. `[--local-host]` select your local hosted Node and Indexer;
2. `[--indexer-address=<ia>]` address of your local Indexer Client;
3. `[--data-address=<da>]` publisher account address (default: PPoS Dex Oracle account);
4. `[--algo-threshold=<at>]` plot only data of accounts that own more than this threshold (default: 1000 ALGO);
5. `[--starting-block=<sb>]` plot data from this block (if availables);
6. `[--ending-block=<eb>]` plot data until this block;

**Output**
```bash
ppos_dex_data.csv
```

### Conclusion
If you think that PPoS Dex Index represents a good and useful tool please consider
tipping the PPoS Dex Oracle account:

`WIPE4JSUWLXKZZK6GJ6VI32PX6ZWPKBRH5YFRJCHWOVC73P5RI4DGUQUWQ`

to cover the transactions fee.
