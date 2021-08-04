
import time
import json
import base64
import msgpack
from schema import Schema, And, Optional
from datetime import datetime
from algosdk import mnemonic
from algosdk.account import address_from_private_key
from algosdk.error import *
from algosdk.future.transaction import PaymentTxn
from inequality_indexes import *
from algo_query import *


def wait_for_confirmation(algod_client, transaction_id, timeout):
    """Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.

    Args:
        algod_client (AlgodClient): Algod Client
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait

    Returns:
        (dict): pending transaction information, or throws an error if the
        transaction is not confirmed or rejected in the next timeout rounds
    """
    start_round = algod_client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        algod_client.status_after_block(current_round)
        try:
            pending_txn = algod_client.pending_transaction_info(transaction_id)
        except Exception:
            return
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(
            timeout))


def post_ppos_dex_data(algod_client, indexer_client, passphrase,
                       algo_threshold):

    private_key = mnemonic.to_private_key(passphrase)

    account = {'pk': address_from_private_key(private_key),
               'sk': private_key}

    CONNECTION_ATTEMPT_DELAY_SEC = 3
    MAX_CONNECTION_ATTEMPTS = 10
    MICROALGO_TO_ALGO = 1 / 10 ** 6
    MICROALGO_TOTAL_SUPPLY = 10 ** 16

    attempts = 1
    params = None
    ledger = None
    while attempts <= MAX_CONNECTION_ATTEMPTS:
        try:
            params = algod_client.suggested_params()
            ledger = algod_client.ledger_supply()
            break
        except AlgodHTTPError:
            print(f"Algod Client connection attempt "
                  f"{attempts}/{MAX_CONNECTION_ATTEMPTS}")
            print("Trying to contact Algod Client again...")
            time.sleep(CONNECTION_ATTEMPT_DELAY_SEC)
        finally:
            attempts += 1
    if attempts > MAX_CONNECTION_ATTEMPTS:
        quit("Unable to connect to Algod Client.")

    attempts = 1
    algo_owners = None
    while attempts <= MAX_CONNECTION_ATTEMPTS:
        try:
            algo_owners = get_algo_owners(indexer_client, algo_threshold)
            break
        except IndexerHTTPError:
            print(f"Indexer Client connection attempt "
                  f"{attempts}/{MAX_CONNECTION_ATTEMPTS}")
            print("Trying to contact Indexer Client again...")
            time.sleep(CONNECTION_ATTEMPT_DELAY_SEC)
        finally:
            attempts += 1
    if attempts > MAX_CONNECTION_ATTEMPTS:
        quit("Unable to connect to Indexer Client.")

    stakes = [account['amount'] * MICROALGO_TO_ALGO for
              account in algo_owners]
    algo_hhi = herfindahl_hirschman_index(stakes)
    online_stakes = [account['amount'] * MICROALGO_TO_ALGO
                     for account in algo_owners
                     if account['status'] == 'Online']
    algo_dynamics = ledger['total-money'] / MICROALGO_TOTAL_SUPPLY
    ppos_online_stake = ledger['online-money'] / ledger['total-money']
    ppos_online_accounts = len(online_stakes) / len(algo_owners)
    ppos_gini = gini_index(online_stakes)
    ppos_theil_l = theil_l_index(online_stakes)
    ppos_theil_t = theil_t_index(online_stakes)
    ppos_hhi = herfindahl_hirschman_index(online_stakes)
    ppos_dex = (algo_dynamics
                * ppos_online_stake
                * ppos_online_accounts
                * (1 - ppos_gini))

    note = {'algo_threshold': algo_threshold,
            'accounts': len(algo_owners),
            'algo_hhi': algo_hhi,
            'algo_dynamics': algo_dynamics,
            'ppos_online_stake': ppos_online_stake,
            'ppos_online_accounts': ppos_online_accounts,
            'ppos_gini': ppos_gini,
            'ppos_theil_l': ppos_theil_l,
            'ppos_theil_t': ppos_theil_t,
            'ppos_hhi': ppos_hhi,
            'ppos_dex': ppos_dex,
            'timestamp': str(datetime.now())}

    bytes_note = msgpack.packb(note)

    unsigned_txn = PaymentTxn(sender=account['pk'],
                              sp=params,
                              receiver=account['pk'],
                              amt=0,
                              note=bytes_note)

    signed_txn = unsigned_txn.sign(account['sk'])
    txid = algod_client.send_transaction(signed_txn)
    print("Publishing Algorand PPoS Dex data in txID: {}".format(txid))

    try:
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    except Exception as err:
        print(err)
        return

    print("txID: {}".format(txid), " confirmed in round: {}\n".format(
        confirmed_txn.get("confirmed-round", 0)))
    print("Transaction information:\n{}".format(
        json.dumps(confirmed_txn, indent=4)))


def get_ppos_dex_data(indexer_client, ppos_dex_address, algo_threshold,
                      start_block=11476070, end_block=None):

    CONNECTION_ATTEMPT_DELAY_SEC = 3
    MAX_CONNECTION_ATTEMPTS = 10

    attempts = 1
    ppos_dex_txns_note = None
    while attempts <= MAX_CONNECTION_ATTEMPTS:
        try:
            ppos_dex_txns_note = get_address_txns_note(
                indexer_client, ppos_dex_address, start_block, end_block)
            break
        except IndexerHTTPError:
            print(f"Indexer Client connection attempt "
                  f"{attempts}/{MAX_CONNECTION_ATTEMPTS}")
            print("Trying to contact Indexer Client again...")
            time.sleep(CONNECTION_ATTEMPT_DELAY_SEC)
        finally:
            attempts += 1
    if attempts > MAX_CONNECTION_ATTEMPTS:
        quit("Unable to connect to Indexer Client.")

    # TODO: make 'algo_hhi' and 'ppos_hhi' mandatory fileds in the schema
    schema = Schema({
        'algo_threshold': int,
        'accounts': And(int, lambda n: 0 <= n),
        Optional('algo_hhi'): And(float, lambda n: 0 <= n <= 1),
        'algo_dynamics': And(float, lambda n: 0 <= n),
        'ppos_online_stake': And(float, lambda n: 0 <= n <= 1),
        'ppos_online_accounts': And(float, lambda n: 0 <= n <= 1),
        'ppos_gini': And(float, lambda n: 0 <= n <= 1),
        'ppos_theil_l': And(float, lambda n: 0 <= n),
        'ppos_theil_t': And(float, lambda n: 0 <= n),
        Optional('ppos_hhi'): And(float, lambda n: 0 <= n <= 1),
        'ppos_dex': And(float, lambda n: 0 <= n <= 1),
        'timestamp': str
    })

    ppos_dex_data = []
    for txn_note in ppos_dex_txns_note:
        try:
            data = schema.validate(
                msgpack.unpackb(base64.b64decode(txn_note))
            )
            if data['algo_threshold'] == algo_threshold:
                ppos_dex_data += [data]
        except:
            pass

    if not ppos_dex_data:
        quit(f"Impossible to find valid PPos Dex data published by "
             f"{ppos_dex_address} starting from block {start_block}.")

    return ppos_dex_data
