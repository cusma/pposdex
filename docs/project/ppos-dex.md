# Pure Proof of Stake Decentralization Index

We finally apply the \\(DEX\\) index to Algorand’s PPoS, defining the
\\(PPoS DEX\\) index.

Given the \\(DEX\\) index definition, we say Algorand PPoS is _"completely_
_decentralized"_ iff:

1. Algorand Nodes Hardware is completely decentralized (\\(d_N = 1\\));
1. Algorand Network Topology is completely decentralized (\\(d_T = 1\\));
1. Algorand Validating Stake is completely decentralized (\\(d_S = 1\\)).

As pointed out in previous chapters, due to resource and time constraints, we
assume complete decentralization both for Nodes Hardware and Network Topology,
leaving the refinement of these assumptions to future works (community
contributions are welcome).

The ALGO has a _total supply of 10B_, hardcoded in the genesis block, so the
_Stake Dynamics_ applies to ALGO.

The circulating supply is measured as the ledger's _participating_ supply (the
Algod `total-money`): the genesis supply minus the balances of the accounts
flagged as non-participating. It counts custodial, treasury and exchange
balances as circulating, so it is larger than the economic circulating supply.

We say Algorand Validating Stake is _“completely decentralized”_ iff:

1. All the ALGO genesis supply is circulating in the ecosystem (\\(S_{dyn}\\));
1. All the ALGO circulating supply is taking part to the PPoS (\\(S_{prt}\\));
1. All the accounts that owns ALGOs are taking part to PPoS (\\(A_{prt}\\));
1. All the accounts participating in PPoS hold the same amount of ALGO
(\\(GI\\) or \\(HHI\\));

Combining the 4 points above, we know _"how far"_ PPoS is from its purely
theoretical decentralization, being aware that the PPoS only _tends_ to the
ideal condition, _never reaching it_.

## PPoS DEX v1

\\[ PPoS DEX = d_N \cdot d_T \cdot S_{dyn} \cdot S_{prt} \cdot A_{prt} \cdot
(1 - GI(S)) \\]

## PPoS DEX v2

\\[ PPoS DEX = d_N \cdot d_T \cdot S_{dyn} \cdot S_{prt} \cdot (1 - HHI(S)) \\]

> [!NOTE]
> On Algorand data, each version mostly follows a single factor: since 2023, 90%
> of the variation of v1 comes from the accounts participation, and 96% of the
> variation of v2 from the ALGO participation.

## PPoS DEX v3

Instead of the distance from an ideal, v3 measures the stake against the
thresholds of the consensus: it is a set of four
[Nakamoto Coefficients](stake.md#nakamoto-coefficient), the fewest online
accounts holding together more than a share of the online stake.

\\[ PPoS DEX = \left( NC_{10\\%}, NC_{20\\%}, NC_{33\\%}, NC_{90\\%} \right) \\]

- _Veto_, \\(NC_{10\\%}\\): a coalition above it can block protocol upgrades;
- _Liveness_, \\(NC_{20\\%}\\): a coalition above it can stall the consensus;
- _Nakamoto_, \\(NC_{33\\%}\\): a coalition above it breaks the honest majority
  assumption;
- _Upgrade_, \\(NC_{90\\%}\\): how many accounts it takes to reach the broad
  supermajority that protocol upgrades need.

The higher each coefficient, the more decentralized. Being counts, they are not
per-unit indexes, and they do not include the Nodes Hardware and Network
Topology factors.

The same coefficients of operators, merging the accounts likely run by the same
operator, are published alongside them.

## Metrics summary

| METRIC                 | SYMBOL              | DESCRIPTION                                                                                           |
|------------------------|---------------------|-------------------------------------------------------------------------------------------------------|
| ALGO Dynamics          | \\(S_{dyn}\\)       | 0 = no ALGO circulation, 1 = complete ALGO circulation                                                |
| ALGO Participation     | \\(S_{prt}\\)       | 0 = no PPoS participation, 1 = complete PPoS participation                                            |
| Accounts Participation | \\(A_{prt}\\)       | 0 = no PPoS accounts participation, 1 = complete PPoS accounts participation                          |
| ALGO HHI               | \\(1 - HHI(A)\\)    | Considers all ALGO stakes, whether they participate in the PPoS or not                                |
| PPoS Gini              | \\(1 - GI(S)\\)     | PPoS staking inequality, regardless the number of participating accounts                              |
| PPoS Theil’L           | \\(TL(S)\\)         | PPoS staking inequality, sensitive to differences at the lower end of the distribution (small stakes) |
| PPoS Theil’T           | \\(TT(S)\\)         | PPoS staking inequality, sensitive to differences at the high end of the distribution (large stakes)  |
| PPoS HHI               | \\(1 - HHI(S)\\)    | PPoS staking inequality, takes the number of participating accounts in consideration                  |
| Effective Validators   | \\(N_H, N_{HHI}\\)  | Equal-stake validators the PPoS stake is worth, by entropy and by HHI                                 |
| PPoS Veto              | \\(NC_{10\\%}(S)\\) | Fewest online accounts holding more than 10% of the online stake: able to block upgrades              |
| PPoS Liveness          | \\(NC_{20\\%}(S)\\) | Fewest online accounts holding more than 20% of the online stake: able to stall the consensus         |
| PPoS Nakamoto          | \\(NC_{33\\%}(S)\\) | Fewest online accounts holding more than 1/3 of the online stake: able to break its honest majority   |
| PPoS Upgrade           | \\(NC_{90\\%}(S)\\) | Fewest online accounts holding more than 90% of the online stake: the supermajority upgrades need     |
| PPoS Dex v3 Operators  | \\(NC_{q}(O)\\)     | The four coefficients, merging the online accounts likely run by the same operator                    |

> [!NOTE]
> **Minimum balance filter**
>
> Due to the huge number of accounts already existing on Algorand (more than 30M
> at the time of writing, Sep 2023), fetching and processing all of them would
> be computationally heavy and resource demanding for this project. Therefore, PPoS
> Dex CLI applies an optional _"minimum balance filter"_, to ignore accounts with
> balances lower than a threshold (default 1000 ALGO). Such a filtering operation
> has a _noise-canceling_ effect that makes the data retrieval and process lighter,
> **without compromising data statistical significance of the stake indexes**:
> less than 0.001% of the online stake belongs to accounts below the default
> threshold. The metrics counting accounts, like the Accounts Participation and
> the Gini Index, do depend on the threshold instead.
