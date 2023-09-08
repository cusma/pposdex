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
    save: bool = False,
) -> None:
    plt.suptitle("ALGO Dynamics")
    plt.title("(1 = full circulation or complete participation)", fontsize="medium")
    plt.plot(x_axsis, algo_dynamics, label="ALGO Supply")
    plt.plot(x_axsis, online_stake, label="ALGO Participation in PPoS")
    plt.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plt.locator_params(nbins=x_ticks_number)
    plt.legend()
    plt.ylim(0, 1)
    plt.grid(True)
    plt.tight_layout()
    if save:
        plt.savefig(fname="./docs/images/timeseries/algo_dynamics")
    else:
        plt.show()
    plt.close()


def ts_accounts_prt(
    online_accounts: list[float | None],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
    save: bool = False,
) -> None:
    plt.suptitle("Accounts Participation in PPoS")
    plt.title("(1 = complete participation)", fontsize="medium")
    plt.plot(x_axsis, online_accounts, label="Accounts Participation")
    plt.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plt.locator_params(nbins=x_ticks_number)
    plt.legend()
    plt.ylim(0)
    plt.grid(True)
    plt.tight_layout()
    if save:
        plt.savefig(fname="./docs/images/timeseries/accounts_prt")
    else:
        plt.show()
    plt.close()


def ts_algo_inequality(
    algo_hhi: list[float | None],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
    save: bool = False,
) -> None:
    plt.suptitle("ALGO Inequality")
    plt.title("(0 = complete equality)", fontsize="medium")
    plt.plot(x_axsis, algo_hhi, label="HHI")
    plt.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plt.locator_params(nbins=x_ticks_number)
    plt.legend()
    plt.ylim(0)
    plt.grid(True)
    plt.tight_layout()
    if save:
        plt.savefig(fname="./docs/images/timeseries/algo_inequality")
    else:
        plt.show()
    plt.close()


def ts_ppos_inequality_b(
    ppos_gini: list[float | None],
    ppos_hhi: list[float | None],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
    save: bool = False,
) -> None:
    plt.suptitle("Validators Stake Inequality (Bounded)")
    plt.title("(0 = complete equality)", fontsize="medium")
    plt.plot(x_axsis, ppos_gini, label="Gini Index")
    plt.plot(x_axsis, ppos_hhi, label="HHI")
    plt.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plt.locator_params(nbins=x_ticks_number)
    plt.legend()
    plt.ylim(0)
    plt.grid(True)
    plt.tight_layout()
    if save:
        plt.savefig(fname="./docs/images/timeseries/ppos_inequality_b")
    else:
        plt.show()
    plt.close()


def ts_ppos_inequality_unb(
    ppos_theil_l: list[float | None],
    ppos_theil_t: list[float | None],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
    save: bool = False,
) -> None:
    plt.suptitle("Validators Stake Inequality (Unbounded)")
    plt.title("(0 = complete equality)", fontsize="medium")
    plt.plot(x_axsis, ppos_theil_l, label="Theil L Index")
    plt.plot(x_axsis, ppos_theil_t, label="Theil T Index")
    plt.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plt.locator_params(nbins=x_ticks_number)
    plt.legend()
    plt.ylim(0)
    plt.grid(True)
    plt.tight_layout()
    if save:
        plt.savefig(fname="./docs/images/timeseries/ppos_inequality_unb")
    else:
        plt.show()
    plt.close()


def ts_ppos_dex(
    ppos_dex_v1: list[float | None],
    ppos_dex_v2: list[float | None],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
    save: bool = False,
) -> None:
    plt.suptitle("PPoS Dex")
    plt.title("(1 = perfect decentralization)", fontsize="medium")
    plt.plot(x_axsis, ppos_dex_v1, label="PPoS Dex V1")
    plt.plot(x_axsis, ppos_dex_v2, label="PPoS Dex V2")
    plt.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plt.locator_params(nbins=x_ticks_number)
    plt.legend()
    plt.ylim(0)
    plt.grid(True)
    plt.tight_layout()
    if save:
        plt.savefig(fname="./docs/images/timeseries/ppos_dex")
    else:
        plt.show()
    plt.close()


def snap_suptitle(timestamp: str, algo_threshold: int, accounts: int) -> str:
    return f"{timestamp}\nThreshold: {algo_threshold} ALGO\nAccounts: {accounts}"


def snap_algo_prt(
    algo_dynamics: float | None,
    online_stake: float | None,
    timestamp: str,
    algo_threshold: int,
    accounts: int,
    save: bool = False,
) -> None:
    plt.style.use("fivethirtyeight")
    plt.suptitle(
        f"ALGO Dynamics\n(1 = full circulation or complete participation)\n"
        + snap_suptitle(timestamp, algo_threshold, accounts),
        fontsize="medium",
    )
    if algo_dynamics is not None:
        plt.subplot(2, 1, 1)
        plt.barh("ALGO Supply", algo_dynamics)
        plt.xlim(0, 1)
    if online_stake is not None:
        plt.subplot(2, 1, 2)
        plt.barh("ALGO Participation", online_stake)
        plt.xlim(0, 1)
    plt.tight_layout()
    if save:
        plt.savefig(fname="./docs/images/snapshot/algo_dynamics")
    else:
        plt.show()
    plt.close()


def snap_accounts_prt(
    online_accounts: float | None,
    timestamp: str,
    algo_threshold: int,
    accounts: int,
    save: bool = False,
) -> None:
    plt.style.use("fivethirtyeight")
    plt.suptitle(
        f"Accounts Participation\n(1 = complete participation)\n"
        + snap_suptitle(timestamp, algo_threshold, accounts),
        fontsize="medium",
    )
    if online_accounts is not None:
        plt.barh("Accounts Participation", online_accounts)
        plt.xlim(0, min([1, 10 * online_accounts]))
    plt.tight_layout()
    if save:
        plt.savefig(fname="./docs/images/snapshot/accounts_prt")
    else:
        plt.show()
    plt.close()


def snap_algo_inequality(
    algo_hhi: float | None,
    timestamp: str,
    algo_threshold: int,
    accounts: int,
    save: bool = False,
) -> None:
    plt.style.use("fivethirtyeight")
    plt.suptitle(
        f"ALGO Inequality\n(0 = complete equality)\n"
        + snap_suptitle(timestamp, algo_threshold, accounts),
        fontsize="medium",
    )
    if algo_hhi is not None:
        plt.barh("ALGO Inequality", algo_hhi)
        plt.xlim(0, 1)
    plt.tight_layout()
    if save:
        plt.savefig(fname="./docs/images/snapshot/algo_inequality")
    else:
        plt.show()
    plt.close()


def snap_ppos_inequality(
    ppos_gini: float | None,
    ppos_theil_l: float | None,
    ppos_theil_t: float | None,
    ppos_hhi: float | None,
    timestamp: str,
    algo_threshold: int,
    accounts: int,
    save: bool = False,
) -> None:
    plt.style.use("fivethirtyeight")
    plt.suptitle(
        f"Validators Stake Inequality\n(0 = complete equality)\n"
        + snap_suptitle(timestamp, algo_threshold, accounts),
        fontsize="medium",
    )
    # Boundend
    if ppos_gini is not None:
        plt.subplot(4, 1, 1)
        plt.barh("Gini Index", ppos_gini, color="g")
        plt.xlim(0, 1)
    if ppos_hhi is not None:
        plt.subplot(4, 1, 2)
        plt.barh("HHI", ppos_hhi, color="g")
        plt.xlim(0, 1)
    # Unbounded
    if ppos_theil_l is not None and ppos_theil_t is not None:
        x_upper_lim = round(max(ppos_theil_l, ppos_theil_t)) + 1
        plt.subplot(4, 1, 3)
        plt.barh("Theil L Index", ppos_theil_l)
        plt.xlim(0, x_upper_lim)
        plt.subplot(4, 1, 4)
        plt.barh("Theil T Index", ppos_theil_t)
        plt.xlim(0, x_upper_lim)
    plt.tight_layout()
    if save:
        plt.savefig(fname="./docs/images/snapshot/ppos_inequality")
    else:
        plt.show()
    plt.close()


def snap_ppos_dex(
    ppos_dex_v1: float | None,
    ppos_dex_v2: float | None,
    timestamp: str,
    algo_threshold: int,
    accounts: int,
    save: bool = False,
) -> None:
    plt.style.use("fivethirtyeight")
    plt.suptitle(
        f"PPoS Dex\n(1 = perfect decentralization)\n"
        + snap_suptitle(timestamp, algo_threshold, accounts),
        fontsize="medium",
    )
    if ppos_dex_v1 is not None:
        plt.subplot(2, 1, 1)
        plt.barh("PPoS Dex v1", ppos_dex_v1)
        plt.xlim(0, min([1, 10 * ppos_dex_v1]))
    if ppos_dex_v2 is not None:
        plt.subplot(2, 1, 2)
        plt.barh("PPoS Dex v2", ppos_dex_v2)
        plt.xlim(0, min([1, 10 * ppos_dex_v2]))
    plt.tight_layout()
    if save:
        plt.savefig(fname="./docs/images/snapshot/ppos_dex")
    else:
        plt.show()
    plt.close()


def timeseries(ppos_dex_data: list[dict], save: bool = False) -> None:
    ppos_dex_data.reverse()
    x_axsis = list(range(len(ppos_dex_data)))
    x_ticks = [d["timestamp"][:10] for d in ppos_dex_data]

    # Stake Participation
    algo_dynamics = [d.get("algo_dynamics") for d in ppos_dex_data]
    online_stake = [d.get("ppos_online_stake") for d in ppos_dex_data]
    ts_algo_prt(algo_dynamics, online_stake, x_axsis, x_ticks, save=save)

    # Accounts Participation
    online_accounts = [d.get("ppos_online_accounts") for d in ppos_dex_data]
    ts_accounts_prt(online_accounts, x_axsis, x_ticks, save=save)

    # Stake Inequality
    algo_hhi = [d.get("algo_hhi") for d in ppos_dex_data]
    ts_algo_inequality(algo_hhi, x_axsis, x_ticks, save=save)

    # PPoS Inequality Bounded
    ppos_gini = [d.get("ppos_gini") for d in ppos_dex_data]
    ppos_hhi = [d.get("ppos_hhi") for d in ppos_dex_data]
    ts_ppos_inequality_b(ppos_gini, ppos_hhi, x_axsis, x_ticks, save=save)

    # PPoS Inequality Unbounded
    ppos_theil_l = [d.get("ppos_theil_l") for d in ppos_dex_data]
    ppos_theil_t = [d.get("ppos_theil_t") for d in ppos_dex_data]
    ts_ppos_inequality_unb(ppos_theil_l, ppos_theil_t, x_axsis, x_ticks, save=save)

    # PPoS Dex
    ppos_dex_v1 = [d.get("ppos_dex") for d in ppos_dex_data]
    ppos_dex_v2 = [d.get("ppos_dex_v2") for d in ppos_dex_data]
    ts_ppos_dex(ppos_dex_v1, ppos_dex_v2, x_axsis, x_ticks, save=save)


def snapshot(ppos_dex_data: list[dict], save: bool = False) -> None:
    timestamp = ppos_dex_data[0]["timestamp"][:10]
    algo_threshold = ppos_dex_data[0]["algo_threshold"]
    accounts = ppos_dex_data[0]["accounts"]

    # Stake Participation
    algo_dynamics = ppos_dex_data[0].get("algo_dynamics")
    online_stake = ppos_dex_data[0].get("ppos_online_stake")
    snap_algo_prt(
        algo_dynamics, online_stake, timestamp, algo_threshold, accounts, save=save
    )

    # Accounts Participation
    online_accounts = ppos_dex_data[0].get("ppos_online_accounts")
    snap_accounts_prt(online_accounts, timestamp, algo_threshold, accounts, save=save)

    # PPoS Inequality
    ppos_gini = ppos_dex_data[0].get("ppos_gini")
    ppos_theil_l = ppos_dex_data[0].get("ppos_theil_l")
    ppos_theil_t = ppos_dex_data[0].get("ppos_theil_t")
    ppos_hhi = ppos_dex_data[0].get("ppos_hhi")
    snap_ppos_inequality(
        ppos_gini,
        ppos_theil_l,
        ppos_theil_t,
        ppos_hhi,
        timestamp,
        algo_threshold,
        accounts,
        save=save,
    )

    # PPoS Dex
    ppos_dex_v1 = ppos_dex_data[0].get("ppos_dex")
    ppos_dex_v2 = ppos_dex_data[0].get("ppos_dex_v2")
    snap_ppos_dex(
        ppos_dex_v1, ppos_dex_v2, timestamp, algo_threshold, accounts, save=save
    )
