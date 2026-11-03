"""
Algorand PPoS Dex Helpers
"""

import functools
import json
import os
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from algosdk import account, mnemonic
from algosdk.atomic_transaction_composer import (
    AccountTransactionSigner,
    sign_transaction_with_signer,
)
from algosdk.error import IndexerHTTPError
from algosdk.transaction import PaymentTxn, wait_for_confirmation
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

ATTEMPT_DELAY_SEC = 3
MAX_ATTEMPTS = 10
ACCOUNTS_PAGE_SIZE = 1000  # Indexer maximum, the default page is 100 accounts
ENV_MNEMONIC = "ALGO_MNEMONIC"

# Indexer and Algod JSON responses
type Json = dict[str, Any]


@dataclass(frozen=True)
class Account:
    """Algorand account, its private key is never shown in logs"""

    private_key: str = field(repr=False)

    @property
    def address(self) -> str:
        address: str = account.address_from_private_key(self.private_key)
        return address


def indexer_request[**P, R](request: Callable[P, R]) -> Callable[P, R]:
    """
    Wraps a request to the Indexer adding connection attempts management.

    Args:
        request: Request to IndexerClient

    Returns:
        Wrapped Indexer request
    """

    @functools.wraps(request)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        attempts = 1
        while attempts <= MAX_ATTEMPTS:
            try:
                return request(*args, **kwargs)
            except IndexerHTTPError as err:
                print(err)
                print(f"Indexer request attempt {attempts}/{MAX_ATTEMPTS}")
                print("Trying submit request again...")
                time.sleep(ATTEMPT_DELAY_SEC)
            finally:
                attempts += 1
        sys.exit("Algorand Indexer request failed.")

    return wrapper


def get_publisher_account() -> Account:
    env_mnemonic = os.getenv(f"{ENV_MNEMONIC}")
    if env_mnemonic is None:
        raise Exception(f"Mnemonic environment variable not set: {ENV_MNEMONIC}")
    return Account(private_key=mnemonic.to_private_key(env_mnemonic))


@indexer_request
def get_algo_holders(
    indexer_client: IndexerClient,
    microalgo_min_balance: int | None = None,
) -> list[Json]:
    """
    Get Accounts holding a balance greater than `microalgo_min_balance`

    Args:
        indexer_client: Algorand Indexer Client
        microalgo_min_balance: microALGO minimum balance

    Returns:
        Accounts holding a balance greater than `microalgo_min_balance`
    """
    nexttoken = ""
    has_result = True

    holders: list[Json] = []
    while has_result:
        result = indexer_client.accounts(
            next_page=nexttoken,
            min_balance=microalgo_min_balance,
            exclude="all",
            limit=ACCOUNTS_PAGE_SIZE,
        )

        accounts = result["accounts"]
        has_result = len(accounts) > 0
        holders += accounts

        if has_result:
            nexttoken = result["next-token"]

    if not holders:
        sys.exit(f"No account with {microalgo_min_balance} microAlgo balance found.")

    return holders


@indexer_request
def get_address_txns_note(
    indexer_client: IndexerClient,
    address: str,
    start_block: int | None = None,
    end_block: int | None = None,
) -> list[str]:
    """
    Get transaction notes published by `address`

    Args:
        indexer_client: Algorand Indexer Client
        address: Note publisher address
        start_block: Note research starting block
        end_block: Note research ending block

    Returns:
        Notes published by `address`
    """
    nexttoken = ""
    has_result = True

    address_txns: list[Json] = []
    while has_result:
        result = indexer_client.search_transactions_by_address(
            address=address,
            next_page=nexttoken,
            min_round=start_block,
            max_round=end_block,
        )
        txns = result["transactions"]
        has_result = len(txns) > 0
        address_txns += txns

        if has_result:
            nexttoken = result["next-token"]

    txns_note: list[str] = []
    for txn in address_txns:
        note = txn.get("note")
        if note is not None:
            txns_note.append(note)

    if not txns_note:
        sys.exit(f"No published note found for account {address}.")

    return txns_note


def post_note(
    algod_client: AlgodClient,
    publisher: Account,
    note: bytes,
    wait_rounds: int = 0,
    verbose: bool = False,
) -> Json:
    """
    Post a note on Algorand

    Args:
        algod_client: Algod Client
        publisher: Publisher account
        note: Note to publish
        wait_rounds: Wait rounds for note publishing confirmation
        verbose: Show publication details

    Returns:
        Confirmed publication transaction
    """
    sp = algod_client.suggested_params()
    unsigned_txn = PaymentTxn(
        sender=publisher.address,
        sp=sp,
        receiver=publisher.address,
        amt=0,
        note=note,
    )

    signed_txn = sign_transaction_with_signer(
        unsigned_txn, AccountTransactionSigner(publisher.private_key)
    )
    txid = algod_client.send_transaction(signed_txn)
    if verbose:
        print(f"Publishing Algorand PPoS Dex data in txID: {txid}\n")

    confirmed_txn: Json = wait_for_confirmation(algod_client, txid, wait_rounds)

    if verbose:
        print(f"Confirmed in round: {confirmed_txn.get('confirmed-round', 0)}\n")
        print(f"Transaction information:\n{json.dumps(confirmed_txn, indent=4)}")
    return confirmed_txn
