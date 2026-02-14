import argparse
from pathlib import Path

from predictoor_bot.config import ConfigError, load_config, resolve_private_key

APP_NAME = "predictoor-bot"
DEFAULT_CONFIG_PATH = Path.home() / ".config" / APP_NAME / "config.toml"


def main() -> int:
    parser = argparse.ArgumentParser(prog=APP_NAME)
    sub = parser.add_subparsers(dest="cmd", required=False)

    parser.add_argument("--version", action="store_true", help="Show version and exit")

    run_p = sub.add_parser("run", help="Run the bot")
    run_p.add_argument("--dry-run", action="store_true", help="Validate config and print planned actions")
    run_p.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help=f"Path to config file (default: {DEFAULT_CONFIG_PATH})",
    )

    args = parser.parse_args()

    if args.version:
        print(f"{APP_NAME} 0.0.0")
        return 0

    if args.cmd == "run":
        try:
            cfg = load_config(args.config)
        except ConfigError as e:
            print(f"[ERROR] {e}")
            print(f"Create it at: {DEFAULT_CONFIG_PATH}")
            print("Example:\n  [bot]\n  enabled = true\n")
            return 2

        if args.dry_run:
            try:
                _ = resolve_private_key(cfg.wallet)
                pk_status = "OK"
            except ConfigError as e:
                pk_status = f"ERROR: {e}"

            print("[DRY-RUN] Config OK")
            print(f"[DRY-RUN] Using config: {args.config}")
            print(f"[DRY-RUN] bot.enabled = {cfg.bot.enabled}")
            print(f"[DRY-RUN] rpc.url = {cfg.rpc.url}")
            print(f"[DRY-RUN] rpc.chain_id = {cfg.rpc.chain_id}")
            print(f"[DRY-RUN] wallet.private_key = {pk_status}")
            print(f"[DRY-RUN] predictoor.markets = {cfg.predictoor.markets}")
            print(f"[DRY-RUN] predictoor.stake = {cfg.predictoor.stake}")
            print(f"[DRY-RUN] predictoor.cadence_seconds = {cfg.predictoor.cadence_seconds}")
            print("[DRY-RUN] Next steps: connect RPC, load markets, fetch data, score, submit predictions.")
            return 0

        if not cfg.bot.enabled:
            print("[INFO] bot is disabled in config. Exiting.")
            return 0

        # Minimal run: validate config + private key presence, then exit 0.
        try:
            _ = resolve_private_key(cfg.wallet)
        except ConfigError as e:
            print(f"[ERROR] {e}")
            return 2

        print("[INFO] Run mode: config + wallet OK (stub).")
        print("[INFO] Non-dry-run stub exits successfully for now.")
        return 0

    print(f"{APP_NAME}: ok")
    return 0
