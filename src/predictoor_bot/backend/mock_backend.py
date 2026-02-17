from __future__ import annotations

from .protocol import Backend, MarketState, TxReceipt


class MockBackend(Backend):
    def get_market_state(self, market_id: str) -> MarketState:
        return MarketState(market_id=market_id, price=1.0)

    def submit_prediction(self, market_id: str, prediction: float, stake: float) -> TxReceipt:
        return TxReceipt(tx_hash="mock_tx_hash")
