from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .trainability_bridge import (
    METHODS,
    _build_readout_bases,
    _evaluate_basis,
    _family_instances,
    _prepare_fd_pairs,
    _simulate_visible_bundle,
    load_profile,
    paired_gains,
    summarize,
)


def build_jobs(cfg: dict) -> list[tuple[str, int, int, int]]:
    jobs: list[tuple[str, int, int, int]] = []
    for family in cfg["families"]:
        for n_raw in cfg["n_values"]:
            n = int(n_raw)
            depth = max(1, int(round(float(cfg["depth_factor"]) * n)))
            for instance in range(_family_instances(cfg, family)):
                jobs.append((family, n, depth, instance))
    return jobs


def run_shard(
    profile: str | Path,
    output: str | Path,
    shard_index: int,
    num_shards: int,
) -> pd.DataFrame:
    cfg = load_profile(profile)
    shard_index = int(shard_index)
    num_shards = int(num_shards)
    if num_shards < 1:
        raise ValueError("num_shards must be >= 1")
    if not 0 <= shard_index < num_shards:
        raise ValueError("shard_index must satisfy 0 <= shard_index < num_shards")

    jobs = build_jobs(cfg)
    selected = jobs[shard_index::num_shards]
    if not selected:
        raise RuntimeError(
            f"shard {shard_index}/{num_shards} has no jobs; total={len(jobs)}"
        )

    rows: list[dict] = []
    for family, n, depth, instance in selected:
        bundle = _simulate_visible_bundle(cfg, family, n, depth, instance)
        bases, rank = _build_readout_bases(
            cfg, bundle, family, n, depth, instance
        )
        fd_pairs = _prepare_fd_pairs(cfg, bundle, family, n, depth)

        for method, q in bases.items():
            metrics = _evaluate_basis(cfg, bundle, q, rank, fd_pairs)
            rows.append(
                {
                    "profile": cfg["name"],
                    "circuit_id": bundle["circuit_id"],
                    "family": family,
                    "n": n,
                    "depth": depth,
                    "depth_factor": float(cfg["depth_factor"]),
                    "instance": int(instance),
                    "method": method,
                    "parameter_count": int(bundle["pcount"]),
                    "score_dimension": int(len(bundle["p_support"]) - 1),
                    "readout_order": int(cfg["readout_order"]),
                    "readout_rank": int(rank),
                    "align_regular_tangents": int(len(bundle["U_train"])),
                    "eval_regular_tangents": int(len(bundle["U_eval"])),
                    "Ffull_eval_mean": float(np.mean(bundle["Ffull_eval"])),
                    "FQ_eval_mean": float(np.mean(bundle["FQ_eval"])),
                    "Ffull_over_FQ_eval_mean": float(
                        np.mean(bundle["Ffull_eval"] / bundle["FQ_eval"])
                    ),
                    "shots": int(cfg["shots"]),
                    "fd_epsilon": float(cfg["fd_epsilon"]),
                    "fd_directions": int(len(fd_pairs)),
                    **metrics,
                }
            )

        print(
            f"[bridge-full] shard={shard_index}/{num_shards} "
            f"{bundle['circuit_id']} rank={rank} "
            f"support={len(bundle['p_support'])} done",
            flush=True,
        )

    outdir = Path(output)
    outdir.mkdir(parents=True, exist_ok=True)
    raw = pd.DataFrame(rows)
    raw.to_csv(outdir / "raw.csv", index=False)
    (outdir / "shard.json").write_text(
        json.dumps(
            {
                "profile": cfg["name"],
                "shard_index": shard_index,
                "num_shards": num_shards,
                "scheduled_circuits": len(selected),
                "method_rows": len(raw),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return raw


def aggregate(
    profile: str | Path,
    input_dir: str | Path,
    output: str | Path,
) -> pd.DataFrame:
    cfg = load_profile(profile)
    paths = sorted(Path(input_dir).rglob("raw.csv"))
    if not paths:
        raise FileNotFoundError(f"no shard raw.csv files under {input_dir}")

    raw = pd.concat([pd.read_csv(path) for path in paths], ignore_index=True)
    raw = raw.drop_duplicates(subset=["circuit_id", "method"], keep="last")
    raw = raw.sort_values(["family", "n", "instance", "method"]).reset_index(
        drop=True
    )

    expected_circuits = len(build_jobs(cfg))
    observed_circuits = int(raw["circuit_id"].nunique())
    expected_rows = expected_circuits * len(METHODS)
    if observed_circuits != expected_circuits:
        raise RuntimeError(
            f"incomplete aggregate: observed {observed_circuits} circuits, "
            f"expected {expected_circuits}"
        )
    if len(raw) != expected_rows:
        raise RuntimeError(
            f"incomplete aggregate: observed {len(raw)} rows, expected {expected_rows}"
        )

    outdir = Path(output)
    outdir.mkdir(parents=True, exist_ok=True)
    raw.to_csv(outdir / "raw.csv", index=False)
    summarize(raw, cfg).to_csv(outdir / "summary.csv", index=False)
    paired_gains(raw, cfg).to_csv(outdir / "paired_gains.csv", index=False)

    manifest = {
        "profile": cfg,
        "expected_circuits": expected_circuits,
        "observed_circuits": observed_circuits,
        "method_rows": len(raw),
        "shard_files": [str(path) for path in paths],
        "outputs": ["raw.csv", "summary.csv", "paired_gains.csv"],
        "interpretation": {
            "primary_bridge_metric": "expected_scalar_directional_grad2",
            "primary_operational_metric": "finite_difference_snr_mean",
            "primary_contrast": "aligned_crossfit / physical on the same circuit",
            "warning": (
                "Controlled local linear-readout bridge; not a supervised "
                "barren-plateau claim."
            ),
        },
    }
    (outdir / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return raw


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run")
    run.add_argument("--profile", required=True)
    run.add_argument("--output", required=True)
    run.add_argument("--shard-index", type=int, required=True)
    run.add_argument("--num-shards", type=int, required=True)

    agg = sub.add_parser("aggregate")
    agg.add_argument("--profile", required=True)
    agg.add_argument("--input-dir", required=True)
    agg.add_argument("--output", required=True)

    args = parser.parse_args()
    if args.cmd == "run":
        run_shard(
            args.profile,
            args.output,
            args.shard_index,
            args.num_shards,
        )
    else:
        aggregate(args.profile, args.input_dir, args.output)


if __name__ == "__main__":
    main()
