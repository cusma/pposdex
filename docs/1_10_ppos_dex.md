# Pure Proof of Stake Decentralization Index

---

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

We say Algorand Validating Stake is _“completely decentralized”_ iff:

1. All the ALGO genesis supply is circulating in the ecosystem (\\(S_{dyn}\\));
1. All the ALGO circulating supply is taking part to the PPoS (\\(S_{prt}\\));
1. All the accounts that owns ALGOs are taking part to PPoS  (\\(A_{prt}\\));
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

## Metrics summary

| METRIC                 | SYMBOL           | DESCRIPTION                                                                                           |
|------------------------|------------------|-------------------------------------------------------------------------------------------------------|
| ALGO Dynamics          | \\(S_{dyn}\\)    | 0 = no ALGO circulation, 1 = complete ALGO circulation                                                |
| ALGO Participation     | \\(S_{prt}\\)    | 0 = no PPoS participation, 1 = complete PPoS participation                                            |
| Accounts Participation | \\(A_{prt}\\)    | 0 = no PPoS accounts participation, 1 = complete PPoS accounts participation                          |
| ALGO HHI               | \\(1 - HHI(A)\\) | Considers all ALGO stakes, whether they participate in the PPoS or not                                |
| PPoS Gini              | \\(1 - GI(S)\\)  | PPoS staking inequality, regardless the number of participating accounts                              |
| PPoS Theil’L           | \\(TL(S)\\)      | PPoS staking inequality, sensitive to differences at the lower end of the distribution (small stakes) |
| PPoS Theil’T           | \\(TT(S)\\)      | PPoS staking inequality, sensitive to differences at the high end of the distribution (large stakes)  |
| PPoS HHI               | \\(1 - HHI(S)\\) | PPoS staking inequality, takes the number of participating accounts in consideration                  |

---

> **Minimum balance filter**
>
> Due to the huge number of accounts already existing on Algorand (more than 30M
> at the time of writing, Sep 2023), fetching and processing all of them would
> be computationally heavy and resource demaning for this project. Therefore, PPoS
> Dex CLI applies an optional _"minimum balance filter"_, to ignore accounts with
> balances lower than a threshold (default 1000 ALGO). Such a filtering operation
> has a _noise-canceling_ effect that makes the data retrieval and procces lighter,
> **without compromising data statistical significancy of the indexes**.
