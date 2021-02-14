
def get_algo_owners(indexer_client, algo_min_balance):
    """Search for ALGO owners

    Args:
        indexer_client (IndexerClient): Indexer Client V2
        algo_min_balance: ALGO minimum balance (converted in microALGO integer)

    Returns:
        (dict): accounts that owns at least algo_min_balance.

    """

    ALGO_TO_MICROALGO = 10 ** 6

    nexttoken = ""
    numtx = 1
    owners = []
    while numtx > 0:
        response = indexer_client.accounts(
            min_balance=int(algo_min_balance * ALGO_TO_MICROALGO),
            next_page=nexttoken,
            limit=1000)
        accounts = response['accounts']
        owners += accounts
        numtx = len(accounts)
        if numtx > 0:
            # pointer to the next chunk of requests
            nexttoken = response['next-token']
    return owners


def get_asa_owners(indexer_client, asset_id, asa_min_balance=0):
    """Search for ASAs owners

    Args:
        indexer_client (IndexerClient): Indexer Client V2
        asset_id (int): ASA Asset ID
        asa_min_balance (int): Optional; ASA minimum balance expressed as
        minimal int units

    Returns:
        (dict): accounts that owns at least asa_min_balance.

    """
    nexttoken = ""
    numtx = 1
    owners = []
    while numtx > 0:
        result = indexer_client.accounts(
            asset_id=asset_id,
            asa_min_balance=asa_min_balance,
            next_page=nexttoken,
            limit=1000)
        accounts = result['accounts']
        owners += accounts
        numtx = len(accounts)
        if numtx > 0:
            # pointer to the next chunk of requests
            nexttoken = result['next-token']
    return owners


def get_address_txns_note(indexer_client, address, start_block=None,
                          end_block=None):
    nexttoken = ""
    numtx = 1
    address_txns = []
    while numtx > 0:
        result = indexer_client.search_transactions_by_address(
            address=address,
            limit=1000,
            next_page=nexttoken,
            min_round=start_block,
            max_round=end_block
        )
        txns = result['transactions']
        address_txns += txns
        numtx = len(txns)
        if numtx > 0:
            # pointer to the next chunk of requests
            nexttoken = result['next-token']
    txns_note = [txn.get('note') for txn in address_txns]
    return txns_note
