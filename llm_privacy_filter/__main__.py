import argparse
import json
import sys
from pathlib import Path

from .core.pipeline import run
from .utils.logger import get_logger


def _parse_args(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(
        prog="llm_privacy_filter", description="Baseline privacy‑filter CLI (Phase 1)."
    )
    parser.add_argument(
        "--mode",
        choices=["presidio", "regex", "hydrox"],
        default="regex",
        help="Detector to use (default: regex).",
    )
    parser.add_argument(
        "--input", required=True, help="Path to input CSV or JSONL dataset."
    )
    parser.add_argument(
        "--output", required=True, help="Path where the masked CSV will be written."
    )
    parser.add_argument(
        "--sensitivity",
        type=float,
        default=1.0,
        help="Sensitivity threshold (currently unused for regex).",
    )
    parser.add_argument(
        "--gold", help="Optional path to gold‑standard annotations for evaluation."
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None):
    args = _parse_args(argv)
    logger = get_logger()
    logger.info("Starting baseline masking pipeline (mode=%s)", args.mode)

    try:
        result = run(
            dataset_path=args.input,
            output_path=args.output,
            detector=args.mode,
            sensitivity=args.sensitivity,
            gold_path=args.gold,
        )
    except Exception as exc:
        logger.error("Pipeline failed: %s", exc)
        sys.exit(1)

    metrics = result.get("metrics", {})
    logger.info(
        "Pipeline completed. Metrics – precision: %.3f, recall: %.3f, f1: %.3f, leakage: %.3f",
        metrics.get("precision", 0.0),
        metrics.get("recall", 0.0),
        metrics.get("f1", 0.0),
        metrics.get("leakage_rate", 0.0),
    )
    logger.info("Masked output written to %s", args.output)


if __name__ == "__main__":
    main()
