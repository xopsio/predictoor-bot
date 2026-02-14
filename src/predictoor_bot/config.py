from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import tomllib


class ConfigError(ValueError):
    pass


def _require_dict(data: dict, key: str) -> dict:
    obj = data.get(key)
    if not isinstance(obj, dict):
        raise ConfigError(f"Missing [{key}] section")
    return obj


def _require_bool(section: dict, key: str, path: str) -> bool:
    val = section.get(key)
    if not isinstance(val, bool):
        raise ConfigError(f"{path}.{key} must be a boolean")
    return val


def _require_str(section: dict, key: str, path: str) -> str:
    val = section.get(key)
    if not isinstance(val, str) or not val.strip():
        raise ConfigError(f"{path}.{key} must be a non-empty string")
    return val


def _require_int(section: dict, key: str, path: str) -> int:
    val = section.get(key)
    if not isinstance(val, int):
        raise ConfigError(f"{path}.{key} must be an integer")
    return val


def _require_float(section: dict, key: str, path: str) -> float:
    val = section.get(key)
    if not isinstance(val, (int, float)):
        raise ConfigError(f"{path}.{key} must be a number")
    return float(val)


def _require_list_str(section: dict, key: str, path: str) -> list[str]:
    val = section.get(key)
    if not isinstance(val, list) or not all(isinstance(x, str) and x.strip() for x in val):
        raise ConfigError(f"{path}.{key} must be a list of non-empty strings")
    return [x.strip() for x in val]


@dataclass(frozen=True)
class BotConfig:
    enabled: bool


@dataclass(frozen=True)
class RpcConfig:
    url: str
    chain_id: int


@dataclass(frozen=True)
class WalletConfig:
    private_key: str | None  # recommended to set via ENV
    private_key_env: str | None  # e.g. "PREDICTOOR_PRIVATE_KEY"


@dataclass(frozen=True)
class PredictoorConfig:
    markets: list[str]
    stake: float
    cadence_seconds: int


@dataclass(frozen=True)
class AppConfig:
    bot: BotConfig
    rpc: RpcConfig
    wallet: WalletConfig
    predictoor: PredictoorConfig


def _load_wallet(section: dict) -> WalletConfig:
    pk = section.get("private_key")
    if pk is not None and (not isinstance(pk, str) or not pk.strip()):
        raise ConfigError("[wallet].private_key must be a non-empty string if set")

    pk_env = section.get("private_key_env")
    if pk_env is not None and (not isinstance(pk_env, str) or not pk_env.strip()):
        raise ConfigError("[wallet].private_key_env must be a non-empty string if set")

    if pk is None and pk_env is None:
        raise ConfigError("Provide either [wallet].private_key OR [wallet].private_key_env")

    return WalletConfig(
        private_key=pk.strip() if isinstance(pk, str) else None,
        private_key_env=pk_env.strip() if isinstance(pk_env, str) else None,
    )


def resolve_private_key(cfg: WalletConfig) -> str:
    if cfg.private_key:
        return cfg.private_key
    if cfg.private_key_env:
        val = os.getenv(cfg.private_key_env, "")
        if not val.strip():
            raise ConfigError(f"Environment variable not set: {cfg.private_key_env}")
        return val.strip()
    raise ConfigError("Wallet config invalid (no private key source)")


def load_config(path: Path) -> AppConfig:
    if not path.exists():
        raise ConfigError(f"Config not found: {path}")

    data = tomllib.loads(path.read_text(encoding="utf-8"))

    bot_s = _require_dict(data, "bot")
    rpc_s = _require_dict(data, "rpc")
    wallet_s = _require_dict(data, "wallet")
    pred_s = _require_dict(data, "predictoor")

    bot = BotConfig(enabled=_require_bool(bot_s, "enabled", "[bot]"))
    rpc = RpcConfig(
        url=_require_str(rpc_s, "url", "[rpc]"),
        chain_id=_require_int(rpc_s, "chain_id", "[rpc]"),
    )
    wallet = _load_wallet(wallet_s)

    stake = _require_float(pred_s, "stake", "[predictoor]")
    if stake <= 0:
        raise ConfigError("[predictoor].stake must be > 0")

    cadence_seconds = _require_int(pred_s, "cadence_seconds", "[predictoor]")
    if cadence_seconds < 5:
        raise ConfigError("[predictoor].cadence_seconds must be >= 5")

    pred = PredictoorConfig(
        markets=_require_list_str(pred_s, "markets", "[predictoor]"),
        stake=stake,
        cadence_seconds=cadence_seconds,
    )

    return AppConfig(bot=bot, rpc=rpc, wallet=wallet, predictoor=pred)
