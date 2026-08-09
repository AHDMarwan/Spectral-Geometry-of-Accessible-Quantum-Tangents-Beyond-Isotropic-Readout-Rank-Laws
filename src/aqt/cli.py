from __future__ import annotations

import argparse

from .controls import run_isotropic_controls
from .runner import analyze, run_profile


def main():
    p = argparse.ArgumentParser(prog="aqt")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="run one experiment profile or shard")
    r.add_argument("--profile", required=True)
    r.add_argument("--output", required=True)
    r.add_argument("--shard-index", type=int, default=0)
    r.add_argument("--num-shards", type=int, default=1)

    a = sub.add_parser("analyze", help="merge shards and bootstrap at circuit level")
    a.add_argument("--input", action="append", required=True, help="glob pattern; repeatable")
    a.add_argument("--output", required=True)
    a.add_argument("--master-seed", type=int, default=20260809)

    c = sub.add_parser("controls", help="run exact isotropic Beta-law controls")
    c.add_argument("--output", required=True)
    c.add_argument("--seed", type=int, default=20260809)
    c.add_argument("--samples", type=int, default=30000)

    args = p.parse_args()
    if args.cmd == "run":
        run_profile(args.profile, args.output, args.shard_index, args.num_shards)
    elif args.cmd == "analyze":
        analyze(args.input, args.output, args.master_seed)
    else:
        run_isotropic_controls(args.output, args.seed, args.samples)


if __name__ == "__main__":
    main()
