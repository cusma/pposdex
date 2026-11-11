"""
Fake Algod and Indexer clients: they answer the calls PPoS Dex makes from memory,
paginating like the real APIs, and never reach the network.
"""

import base64
from typing import Any

from algosdk import transaction
from algosdk.error import IndexerHTTPError
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from pposdex.helpers import Json

TOTAL_MONEY = 9_876_543_210_000_000
ONLINE_MONEY = 1_965_436_120_000_000


class FakeAlgod(AlgodClient):
    """Algod client answering the calls PPoS Dex makes, recording sent txns"""

    def __init__(self) -> None:
        super().__init__("", "http://fake-algod")
        self.sent: list[transaction.GenericSignedTransaction] = []

    def status(self, *args: Any, **kwargs: Any) -> Json:
        return {"last-round": 1000}

    def ledger_supply(self, *args: Any, **kwargs: Any) -> Json:
        return {
            "current_round": 1000,
            "online-money": ONLINE_MONEY,
            "total-money": TOTAL_MONEY,
        }

    def suggested_params(self, *args: Any, **kwargs: Any) -> Any:
        return transaction.SuggestedParams(
            fee=1000,
            first=1000,
            last=2000,
            gh="wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=",
            gen="mainnet-v1.0",
            flat_fee=True,
        )

    def send_transaction(self, txn: Any, *args: Any, **kwargs: Any) -> str:
        self.sent.append(txn)
        return "TXID"

    def pending_transaction_info(self, *args: Any, **kwargs: Any) -> Json:
        return {"confirmed-round": 1001, "pool-error": ""}


class FakeIndexer(IndexerClient):
    """Indexer client paginating in-memory accounts and notes like the real API"""

    def __init__(self) -> None:
        # untyped_calls_exclude does not cover super() calls
        super().__init__("", "http://fake-indexer")  # type: ignore[no-untyped-call]
        self.holders: list[Json] = []
        self.notes: dict[str, list[bytes]] = {}
        self.requests: list[Json] = []
        self.failures = 0

    def _page(self, items: list[Json], kwargs: Json, default_limit: int) -> Json:
        self.requests.append(kwargs)
        if self.failures:
            self.failures -= 1
            raise IndexerHTTPError("Service Unavailable")
        start = int(kwargs.get("next_page") or 0)
        limit = kwargs.get("limit") or default_limit
        page = items[start : start + limit]
        return {"page": page} | ({"next-token": str(start + limit)} if page else {})

    def health(self, *args: Any, **kwargs: Any) -> Json:
        return {"db-available": True, "round": 1000}

    def accounts(self, *args: Any, **kwargs: Any) -> Json:
        min_balance = kwargs.get("min_balance") or 0
        holders = [
            h
            for h in self.holders
            if h["amount"] > min_balance
            and (h["status"] == "Online" or not kwargs.get("online_only"))
        ]
        result = self._page(holders, kwargs, default_limit=100)
        return {"accounts": result.pop("page")} | result

    def search_transactions_by_address(self, *args: Any, **kwargs: Any) -> Json:
        txns: list[Json] = [
            {"note": base64.b64encode(note).decode()}
            for note in self.notes.get(kwargs["address"], [])
        ]
        # Transactions without a note are skipped
        txns.insert(len(txns) // 2, {"id": "NO-NOTE"})
        result = self._page(txns, kwargs, default_limit=1000)
        return {"transactions": result.pop("page")} | result
