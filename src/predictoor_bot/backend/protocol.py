from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class MarketState:
    market_id: str
    price: float


@dataclass(frozen=True, slots=True)
class TxReceipt:
    tx_hash: str


class Backend(Protocol):
    def get_market_state(self, market_id: str) -> MarketState:
        ...

    def submit_prediction(self, market_id: str, prediction: float, stake: float) -> TxReceipt:
        ...
