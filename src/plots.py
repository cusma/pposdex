import matplotlib.pyplot as plt

N_XTICKS = 10
XTICKS_ROTATION = 45


def ts_algo_prt(
    algo_dynamics: list[float | None],
    online_stake: list[float | None],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
) -> None:
    plt.suptitle("ALGO Participation in PPoS")
    plt.title("(1 = complete participation)")
    plt.plot(x_axsis, algo_dynamics, label="ALGO Dynamics")
    plt.plot(x_axsis, online_stake, label="ALGO Participation")
    plt.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plt.locator_params(nbins=x_ticks_number)
    plt.legend()
    plt.ylim(0, 1)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def ts_accounts_prt(
    online_accounts: list[float | None],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
) -> None:
    plt.suptitle("Accounts Participation in PPoS")
    plt.title("(1 = complete participation)")
    plt.plot(x_axsis, online_accounts, label="Accounts Participation")
    plt.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plt.locator_params(nbins=x_ticks_number)
    plt.legend()
    plt.ylim(0)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def ts_algo_inequality(
    algo_hhi: list[float | None],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
) -> None:
    plt.suptitle("ALGO Inequality")
    plt.title("(0 = complete equality)")
    plt.plot(x_axsis, algo_hhi, label="HHI")
    plt.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plt.locator_params(nbins=x_ticks_number)
    plt.legend()
    plt.ylim(0)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def ts_ppos_inequality_b(
    ppos_gini: list[float | None],
    ppos_hhi: list[float | None],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
) -> None:
    plt.suptitle("Validators Stake Inequality (Bounded)")
    plt.title("(0 = complete equality)")
    plt.plot(x_axsis, ppos_gini, label="Gini Index")
    plt.plot(x_axsis, ppos_hhi, label="HHI")
    plt.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plt.locator_params(nbins=x_ticks_number)
    plt.legend()
    plt.ylim(0)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def ts_ppos_inequality_unb(
    ppos_theil_l: list[float | None],
    ppos_theil_t: list[float | None],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
) -> None:
    plt.suptitle("Validators Stake Inequality (Unbounded)")
    plt.title("(0 = complete equality)")
    plt.plot(x_axsis, ppos_theil_l, label="Theil L Index")
    plt.plot(x_axsis, ppos_theil_t, label="Theil T Index")
    plt.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plt.locator_params(nbins=x_ticks_number)
    plt.legend()
    plt.ylim(0)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def ts_ppos_dex(
    ppos_dex_v1: list[float | None],
    ppos_dex_v2: list[float | None],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
) -> None:
    plt.suptitle("PPoS Dex")
    plt.title("(1 = perfect decentralization)")
    plt.plot(x_axsis, ppos_dex_v1, label="PPoS Dex V1")
    plt.plot(x_axsis, ppos_dex_v2, label="PPoS Dex V2")
    plt.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plt.locator_params(nbins=x_ticks_number)
    plt.legend()
    plt.ylim(0)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def snap_algo_prt(
    timestamp: str,
    algo_threshold: int,
    accounts: int,
    algo_dynamics: float | None,
    online_stake: float | None,
) -> None:
    plt.style.use("fivethirtyeight")
    plt.suptitle(
        f"ALGO Dynamics\n{timestamp} - Threshold: {algo_threshold} ALGO, "
        f"Accounts: {accounts}\n(1 = complete participation)"
    )
    plt.subplot(2, 1, 1)
    plt.barh("ALGO Dynamics", algo_dynamics)
    plt.xlim(0, 1)
    plt.subplot(2, 1, 2)
    plt.barh("ALGO Participation", online_stake)
    plt.xlim(0, 1)
    plt.tight_layout()
    plt.show()


def snap_accounts_prt(
    timestamp: str,
    algo_threshold: int,
    accounts: int,
    online_accounts: float | None,
) -> None:
    plt.style.use("fivethirtyeight")
    plt.suptitle(
        f"ALGO Dynamics\n{timestamp} - Threshold: {algo_threshold} ALGO, "
        f"Accounts: {accounts}\n(1 = complete participation)"
    )
    plt.barh("Accounts Participation", online_accounts)
    plt.xlim(0, 1)
    plt.tight_layout()
    plt.show()


def timeseries(ppos_dex_data: list[dict]) -> None:
    ppos_dex_data.reverse()
    x_axsis = list(range(len(ppos_dex_data)))
    x_ticks = [d["timestamp"][:10] for d in ppos_dex_data]

    # Stake Participation
    algo_dynamics = [d.get("algo_dynamics") for d in ppos_dex_data]
    online_stake = [d.get("ppos_online_stake") for d in ppos_dex_data]
    ts_algo_prt(algo_dynamics, online_stake, x_axsis, x_ticks)

    # Accounts Participation
    online_accounts = [d.get("ppos_online_accounts") for d in ppos_dex_data]
    ts_accounts_prt(online_accounts, x_axsis, x_ticks)

    # Stake Inequality
    algo_hhi = [d.get("algo_hhi") for d in ppos_dex_data]
    ts_algo_inequality(algo_hhi, x_axsis, x_ticks)

    # PPoS Inequality Bounded
    ppos_gini = [d.get("ppos_gini") for d in ppos_dex_data]
    ppos_hhi = [d.get("ppos_hhi") for d in ppos_dex_data]
    ts_ppos_inequality_b(ppos_gini, ppos_hhi, x_axsis, x_ticks)

    # PPoS Inequality Unbounded
    ppos_theil_l = [d.get("ppos_theil_l") for d in ppos_dex_data]
    ppos_theil_t = [d.get("ppos_theil_t") for d in ppos_dex_data]
    ts_ppos_inequality_unb(ppos_theil_l, ppos_theil_t, x_axsis, x_ticks)

    # PPoS Dex
    ppos_dex_v1 = [d.get("ppos_dex") for d in ppos_dex_data]
    ppos_dex_v2 = [d.get("ppos_dex_v2") for d in ppos_dex_data]
    ts_ppos_dex(ppos_dex_v1, ppos_dex_v2, x_axsis, x_ticks)


def snapshot(ppos_dex_data: list[dict]) -> None:
    timestamp = ppos_dex_data[0]["timestamp"][:10]
    algo_threshold = ppos_dex_data[0]["algo_threshold"]
    accounts = ppos_dex_data[0]["accounts"]

    # Stake Participation
    algo_dynamics = ppos_dex_data[0].get("algo_dynamics")
    online_stake = ppos_dex_data[0].get("ppos_online_stake")
    snap_algo_prt(timestamp, algo_threshold, accounts, algo_dynamics, online_stake)

    # Accounts Participation
    online_accounts = ppos_dex_data[0].get("ppos_online_accounts")
    snap_accounts_prt(timestamp, algo_threshold, accounts, online_accounts)

    # Stake Inequality

    # PPoS Inequality
    ppos_inequality = plt
    x_upper_lim = (
        round(max(ppos_dex_data[0]["ppos_theil_l"], ppos_dex_data[0]["ppos_theil_t"]))
        + 1
    )
    ppos_inequality.style.use("fivethirtyeight")
    ppos_inequality.suptitle(
        f"ALGO Distribution\n"
        f"{ppos_dex_data[0]['timestamp'][:10]} - "
        f"Threshold: {ppos_dex_data[0]['algo_threshold']} ALGO, "
        f"Accounts: {ppos_dex_data[0]['accounts']}\n"
        f"(0 = perfect equality)"
    )
    ppos_inequality.subplot(4, 1, 1)
    ppos_inequality.barh("ppos_gini", ppos_dex_data[0]["ppos_gini"], color="g")
    ppos_inequality.xlim(0, 1)
    if ppos_dex_data[0].get("ppos_hhi") is not None:
        ppos_inequality.subplot(4, 1, 2)
        ppos_inequality.barh("ppos_hhi", ppos_dex_data[0]["ppos_hhi"], color="g")
        ppos_inequality.xlim(0, 1)
    ppos_inequality.subplot(4, 1, 3)
    ppos_inequality.barh("ppos_theil_l", ppos_dex_data[0]["ppos_theil_l"])
    ppos_inequality.xlim(0, x_upper_lim)
    ppos_inequality.subplot(4, 1, 4)
    ppos_inequality.barh("ppos_theil_t", ppos_dex_data[0]["ppos_theil_t"])
    ppos_inequality.xlim(0, x_upper_lim)
    ppos_inequality.tight_layout()
    ppos_inequality.show()

    # PPoS Dex
    ppos_dex_index = plt
    ppos_dex_index.style.use("fivethirtyeight")
    ppos_dex_index.suptitle(
        f"Algorand PPoS Decentralization Index\n"
        f"Threshold: {ppos_dex_data[0]['algo_threshold']} ALGO, "
        f"Accounts: {ppos_dex_data[0]['accounts']}\n"
        f"(1 = perfect decentralization)"
    )
    ppos_dex_index.barh("ppos_dex", ppos_dex_data[0]["ppos_dex"])
    ppos_dex_index.xlim(0, 1)
    ppos_dex_index.tight_layout()
    ppos_dex_index.show()
