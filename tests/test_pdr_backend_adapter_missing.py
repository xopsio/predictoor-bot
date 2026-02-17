import pytest

from predictoor_bot.backend.errors import BackendNotAvailableError
from predictoor_bot.backend.pdr_backend_adapter import PdrBackendAdapter


def test_pdr_backend_adapter_raises_if_missing() -> None:
    # If pdr-backend is not installed, adapter should raise a clear error.
    with pytest.raises(BackendNotAvailableError):
        PdrBackendAdapter(rpc_url="http://localhost:8545", chain_id=1)
