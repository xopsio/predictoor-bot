from predictoor_bot.backend.mock_backend import MockBackend


def test_mock_backend_contract() -> None:
    backend = MockBackend()

    state = backend.get_market_state("TEST")
    assert state.market_id == "TEST"
    assert state.price == 1.0

    receipt = backend.submit_prediction("TEST", prediction=0.5, stake=1.0)
    assert receipt.tx_hash == "mock_tx_hash"
