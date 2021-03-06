
import matplotlib.pyplot as plt


def timeseries_plot(data):
    data.reverse()
    x_axsis = list(range(len(data)))
    algo_dynamics = [ppos_dex_data['algo_dynamics']
                     for ppos_dex_data in data]

    ppos_online_stake = [ppos_dex_data['ppos_online_stake']
                         for ppos_dex_data in data]

    ppos_online_accounts = [ppos_dex_data['ppos_online_accounts']
                            for ppos_dex_data in data]

    ppos_gini = [ppos_dex_data['ppos_gini']
                 for ppos_dex_data in data]

    ppos_theil_l = [ppos_dex_data['ppos_theil_l']
                    for ppos_dex_data in data]

    ppos_theil_t = [ppos_dex_data['ppos_theil_t']
                    for ppos_dex_data in data]

    ppos_dex = [ppos_dex_data['ppos_dex']
                for ppos_dex_data in data]

    x_ticks = [ppos_dex_data['timestamp'][:10]
               for ppos_dex_data in data]

    ppos_dynamics = plt
    ppos_dynamics.suptitle("Algorand PPoS Dynamics")
    ppos_dynamics.title("(1 = complete participation)")
    ppos_dynamics.plot(x_axsis, algo_dynamics,
                       label="Algo Dynamics")
    ppos_dynamics.plot(x_axsis, ppos_online_stake,
                       label="PPoS Online Stake")
    ppos_dynamics.plot(x_axsis, ppos_online_accounts,
                       label="PPoS Online Accounts")
    ppos_dynamics.xticks(x_axsis, x_ticks, rotation='45')
    ppos_dynamics.legend()
    ppos_dynamics.ylim(0, 1)
    ppos_dynamics.grid(True)
    ppos_dynamics.tight_layout()
    ppos_dynamics.show()

    ppos_inequality = plt
    ppos_inequality.suptitle("Algorand PPoS Distribution")
    ppos_inequality.title("(0 = perfect equality)")
    ppos_inequality.plot(x_axsis, ppos_gini,
                         label="PPoS Gini Index")
    ppos_inequality.plot(x_axsis, ppos_theil_l,
                         label="PPoS Theil's L Index")
    ppos_inequality.plot(x_axsis, ppos_theil_t,
                         label="PPoS Theil's T Index")
    ppos_inequality.xticks(x_axsis, x_ticks, rotation='45')
    ppos_inequality.legend()
    ppos_inequality.ylim(0)
    ppos_inequality.grid(True)
    ppos_inequality.tight_layout()
    ppos_inequality.show()

    ppos_dex_index = plt
    ppos_dex_index.suptitle("Algorand PPoS Decentralization Index")
    ppos_dex_index.title("(1 = perfect decentralization)")
    ppos_dex_index.plot(x_axsis, ppos_dex,
                        label="PPoS Dex Index")
    ppos_dex_index.xticks(x_axsis, x_ticks, rotation='45')
    ppos_dex_index.legend()
    ppos_dex_index.ylim(0, 1)
    ppos_dex_index.grid(True)
    ppos_dex_index.tight_layout()
    ppos_dex_index.show()


def snapshot_plot(data):

    ppos_dynamics = plt
    ppos_dynamics.style.use('fivethirtyeight')
    ppos_dynamics.suptitle(f"Algorand PPoS Dynamics\n"
                           f"{data[0]['timestamp'][:10]} - "
                           f"Threshold: {data[0]['algo_threshold']} ALGO, "
                           f"Accounts: {data[0]['accounts']}\n"
                           f"(1 = complete participation)")
    ppos_dynamics.subplot(3, 1, 1)
    ppos_dynamics.barh('algo_dynamics', data[0]['algo_dynamics'])
    ppos_dynamics.xlim(0, 1)
    ppos_dynamics.subplot(3, 1, 2)
    ppos_dynamics.barh('ppos_online_stake', data[0]['ppos_online_stake'])
    ppos_dynamics.xlim(0, 1)
    ppos_dynamics.subplot(3, 1, 3)
    ppos_dynamics.barh('ppos_online_accounts', data[0]['ppos_online_accounts'])
    ppos_dynamics.xlim(0, 1)
    ppos_dynamics.tight_layout()
    ppos_dynamics.show()

    ppos_inequality = plt
    x_upper_lim = round(max(data[0]['ppos_theil_l'],
                            data[0]['ppos_theil_t'])) + 1
    ppos_inequality.style.use('fivethirtyeight')
    ppos_inequality.suptitle(f"Algorand PPoS Distribution\n"
                             f"{data[0]['timestamp'][:10]} - "
                             f"Threshold: {data[0]['algo_threshold']} ALGO, "
                             f"Accounts: {data[0]['accounts']}\n"
                             f"(0 = perfect equality)")
    ppos_inequality.subplot(4, 1, 1)
    ppos_inequality.barh('ppos_gini', data[0]['ppos_gini'], color='g')
    ppos_inequality.xlim(0, 1)
    if data[0].get('ppos_hhi') is not None:
        ppos_inequality.subplot(4, 1, 2)
        ppos_inequality.barh('ppos_hhi', data[0]['ppos_hhi'], color='g')
        ppos_inequality.xlim(0, 1)
    ppos_inequality.subplot(4, 1, 3)
    ppos_inequality.barh('ppos_theil_l', data[0]['ppos_theil_l'])
    ppos_inequality.xlim(0, x_upper_lim)
    ppos_inequality.subplot(4, 1, 4)
    ppos_inequality.barh('ppos_theil_t', data[0]['ppos_theil_t'])
    ppos_inequality.xlim(0, x_upper_lim)
    ppos_inequality.tight_layout()
    ppos_inequality.show()

    ppos_dex_index = plt
    ppos_dex_index.style.use('fivethirtyeight')
    ppos_dex_index.suptitle(f"Algorand PPoS Decentralization Index\n"
                            f"Threshold: {data[0]['algo_threshold']} ALGO, "
                            f"Accounts: {data[0]['accounts']}\n"
                            f"(1 = perfect decentralization)")
    ppos_dex_index.barh('ppos_dex', data[0]['ppos_dex'])
    ppos_dex_index.xlim(0, 1)
    ppos_dex_index.tight_layout()
    ppos_dex_index.show()
