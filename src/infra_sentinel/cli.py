
import argparse
from .engine import run_engine

def main():
    ap = argparse.ArgumentParser(prog="infra-sentinel")
    sub = ap.add_subparsers(dest="cmd", required=True)

    runp = sub.add_parser("run", help="Run engine over an event stream")
    runp.add_argument("--config", required=True, help="Path to sentinel.yaml")
    runp.add_argument("--events", required=True, help="Path to events JSONL")
    runp.add_argument("--audit", default=None, help="Audit log path (JSONL)")
    runp.add_argument("--dry-run", action="store_true", help="Enable dry run (no side effects)")

    args = ap.parse_args()

    if args.cmd == "run":
        run_engine(args.config, args.events, args.audit, dry_run=args.dry_run or True)
