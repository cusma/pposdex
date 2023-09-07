import matplotlib.pyplot as plt

N_XTICKS = 10
XTICKS_ROTATION = 45


def ts_algo_prt(
    algo_dynamics: list[float],
    online_stake: list[float],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
) -> None:
    plot = plt
    plot.suptitle("ALGO Participation in PPoS")
    plot.title("(1 = complete participation)")
    plot.plot(x_axsis, algo_dynamics, label="ALGO Dynamics")
    plot.plot(x_axsis, online_stake, label="ALGO Participation")
    plot.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plot.locator_params(nbins=x_ticks_number)
    plot.legend()
    plot.ylim(0, 1)
    plot.grid(True)
    plot.tight_layout()
    plot.show()


def ts_accounts_prt(
    online_accounts: list[float],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
) -> None:
    plot = plt
    plot.suptitle("Accounts Participation in PPoS")
    plot.title("(1 = complete participation)")
    plot.plot(x_axsis, online_accounts, label="Accounts Participation")
    plot.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plot.locator_params(nbins=x_ticks_number)
    plot.legend()
    plot.ylim(0)
    plot.grid(True)
    plot.tight_layout()
    plot.show()


def ts_algo_inequality(
    algo_hhi: list[float],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
) -> None:
    plot = plt
    plot.suptitle("ALGO Inequality")
    plot.title("(0 = complete equality)")
    plot.plot(x_axsis, algo_hhi, label="HHI")
    plot.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plot.locator_params(nbins=x_ticks_number)
    plot.legend()
    plot.ylim(0)
    plot.grid(True)
    plot.tight_layout()
    plot.show()


def ts_ppos_inequality_b(
    ppos_gini: list[float],
    ppos_hhi: list[float],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
) -> None:
    plot = plt
    plot.suptitle("Validators Stake Inequality (Bounded)")
    plot.title("(0 = complete equality)")
    plot.plot(x_axsis, ppos_gini, label="Gini Index")
    plot.plot(x_axsis, ppos_hhi, label="HHI")
    plot.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plot.locator_params(nbins=x_ticks_number)
    plot.legend()
    plot.ylim(0)
    plot.grid(True)
    plot.tight_layout()
    plot.show()


def ts_ppos_inequality_unb(
    ppos_theil_l: list[float],
    ppos_theil_t: list[float],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
) -> None:
    plot = plt
    plot.suptitle("Validators Stake Inequality (Unbounded)")
    plot.title("(0 = complete equality)")
    plot.plot(x_axsis, ppos_theil_l, label="Theil L Index")
    plot.plot(x_axsis, ppos_theil_t, label="Theil T Index")
    plot.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plot.locator_params(nbins=x_ticks_number)
    plot.legend()
    plot.ylim(0)
    plot.grid(True)
    plot.tight_layout()
    plot.show()


def ts_ppos_dex(
    ppos_dex_v1: list[float],
    ppos_dex_v2: list[float],
    x_axsis: list[int],
    x_ticks: list[str],
    x_ticks_rotation: int = XTICKS_ROTATION,
    x_ticks_number: int = N_XTICKS,
) -> None:
    plot = plt
    plot.suptitle("PPoS Dex")
    plot.title("(1 = perfect decentralization)")
    plot.plot(x_axsis, ppos_dex_v1, label="PPoS Dex V1")
    plot.plot(x_axsis, ppos_dex_v2, label="PPoS Dex V2")
    plot.xticks(x_axsis, x_ticks, rotation=x_ticks_rotation)
    plot.locator_params(nbins=x_ticks_number)
    plot.legend()
    plot.ylim(0)
    plot.grid(True)
    plot.tight_layout()
    plot.show()


def timeseries(ppos_dex_data: list[dict]) -> None:
    ppos_dex_data.reverse()
    x_axsis = list(range(len(ppos_dex_data)))
    x_ticks = [d["timestamp"][:10] for d in ppos_dex_data]

    # Stake Participation
    algo_dynamics = [d["algo_dynamics"] for d in ppos_dex_data]
    online_stake = [d["ppos_online_stake"] for d in ppos_dex_data]
    ts_algo_prt(algo_dynamics, online_stake, x_axsis, x_ticks)

    # Accounts Participation
    online_accounts = [d["ppos_online_accounts"] for d in ppos_dex_data]
    ts_accounts_prt(online_accounts, x_axsis, x_ticks)

    # Stake Inequality
    algo_hhi = []
    for d in ppos_dex_data:
        hhi = d.get("algo_hhi")
        algo_hhi.append(hhi) if hhi is not None else algo_hhi.append(0)
    ts_algo_inequality(algo_hhi, x_axsis, x_ticks)

    # PPoS Inequality Bounded
    ppos_gini = [d["ppos_gini"] for d in ppos_dex_data]
    ppos_hhi = []
    for d in ppos_dex_data:
        hhi = d.get("ppos_hhi")
        ppos_hhi.append(hhi) if hhi is not None else ppos_hhi.append(0)
    ts_ppos_inequality_b(ppos_gini, ppos_hhi, x_axsis, x_ticks)

    # PPoS Inequality Unbounded
    ppos_theil_l = [d["ppos_theil_l"] for d in ppos_dex_data]
    ppos_theil_t = [d["ppos_theil_t"] for d in ppos_dex_data]
    ts_ppos_inequality_unb(ppos_theil_l, ppos_theil_t, x_axsis, x_ticks)

    # PPoS Dex
    ppos_dex_v1 = [d["ppos_dex"] for d in ppos_dex_data]
    ppos_dex_v2 = []
    for d in ppos_dex_data:
        data = d.get("ppos_dex_v2")
        ppos_dex_v2.append(data) if data is not None else ppos_dex_v2.append(0)
    ts_ppos_dex(ppos_dex_v1, ppos_dex_v2, x_axsis, x_ticks)


def snapshot(ppos_dex_data: list[dict]) -> None:
    ppos_dynamics = plt
    ppos_dynamics.style.use("fivethirtyeight")
    ppos_dynamics.suptitle(
        f"ALGO Dynamics\n"
        f"{ppos_dex_data[0]['timestamp'][:10]} - "
        f"Threshold: {ppos_dex_data[0]['algo_threshold']} ALGO, "
        f"Accounts: {ppos_dex_data[0]['accounts']}\n"
        f"(1 = complete participation)"
    )
    ppos_dynamics.subplot(3, 1, 1)
    ppos_dynamics.barh("algo_dynamics", ppos_dex_data[0]["algo_dynamics"])
    ppos_dynamics.xlim(0, 1)
    ppos_dynamics.subplot(3, 1, 2)
    ppos_dynamics.barh("ppos_online_stake", ppos_dex_data[0]["ppos_online_stake"])
    ppos_dynamics.xlim(0, 1)
    ppos_dynamics.subplot(3, 1, 3)
    ppos_dynamics.barh("ppos_online_accounts", ppos_dex_data[0]["ppos_online_accounts"])
    ppos_dynamics.xlim(0, 1)
    ppos_dynamics.tight_layout()
    ppos_dynamics.show()

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
