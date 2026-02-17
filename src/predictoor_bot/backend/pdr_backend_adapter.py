from __future__ import annotations

from .errors import BackendNotAvailableError
from .protocol import Backend, MarketState, TxReceipt


class PdrBackendAdapter(Backend):
    """
    Adapter that bridges predictoor-bot to pdr-backend.

    IMPORTANT:
    - This is the ONLY place in predictoor-bot that is allowed to import pdr_backend.
    - Import is done lazily so predictoor-bot can be installed/run without pdr-backend
      unless this adapter is instantiated/used.
    """

    def __init__(self, *, rpc_url: str, chain_id: int) -> None:
        self._rpc_url = rpc_url
        self._chain_id = chain_id

        # Lazy import check (does not import at module import time)
        self._pdr = self._try_import_pdr_backend()

    @staticmethod
    def _try_import_pdr_backend():
        try:
            import pdr_backend  # type: ignore
        except Exception as e:  # ImportError + any dependency errors
            raise BackendNotAvailableError(
                "pdr-backend is not available. Install dev extras: pip install -e '.[dev]' "
                "or provide a different Backend implementation."
            ) from e
        return pdr_backend

    def get_market_state(self, market_id: str) -> MarketState:
        # TODO: Replace placeholder with real pdr-backend calls.
        # Keep returning the bot's own types (MarketState, TxReceipt).
        return MarketState(market_id=market_id, price=0.0)

    def submit_prediction(self, market_id: str, prediction: float, stake: float) -> TxReceipt:
        # TODO: Replace placeholder with real pdr-backend calls.
        return TxReceipt(tx_hash="TODO")
