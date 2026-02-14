from pathlib import Path

import pytest

from predictoor_bot.config import ConfigError, load_config


def test_load_config_ok(tmp_path: Path) -> None:
    p = tmp_path / "config.toml"
    p.write_text(
        """
[bot]
enabled = true

[rpc]
url = "http://127.0.0.1:8545"
chain_id = 1

[wallet]
private_key = "deadbeef"

[predictoor]
markets = ["market-1"]
stake = 1.0
cadence_seconds = 60
""".lstrip(),
        encoding="utf-8",
    )
    cfg = load_config(p)
    assert cfg.bot.enabled is True
    assert cfg.rpc.chain_id == 1
    assert cfg.predictoor.markets == ["market-1"]


def test_load_config_missing_section(tmp_path: Path) -> None:
    p = tmp_path / "config.toml"
    p.write_text("x = 1\n", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_config(p)


def test_load_config_enabled_wrong_type(tmp_path: Path) -> None:
    p = tmp_path / "config.toml"
    p.write_text("[bot]\nenabled = 'yes'\n", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_config(p)
