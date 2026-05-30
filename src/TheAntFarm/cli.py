"""
TheAntFarm CLI – generate G-code from Gerber / Excellon files without a GUI.

This module demonstrates that ``app/services/`` is fully usable without Qt.
It is the primary proof-of-concept for the UI/CLI split architecture.

Usage
-----
Run from the ``src/TheAntFarm`` directory (or any directory once the
package is installed)::

    # Gerber → isolation-routing G-code (top copper layer)
    python cli.py generate gerber top path/to/board.gbr -o ./output

    # Excellon → drill G-code
    python cli.py generate drill drill path/to/board.drl -o ./output

    # Profile cut with custom depth
    python cli.py generate profile profile path/to/board.gbr \\
        --cut-depth -1.8 --travel-height 1.0 -o ./output

    # Bottom layer (mirrored)
    python cli.py generate gerber bottom path/to/bottom.gbr --mirror -o ./output
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# ------------------------------------------------------------------ #
#  Path setup – makes shape_core and app/ importable when running
#  directly as a script (before package installation).
# ------------------------------------------------------------------ #
_this_dir = Path(__file__).parent          # src/TheAntFarm/
_src_dir = _this_dir.parent               # src/
for _p in [str(_src_dir), str(_this_dir)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from app.services.pcb_service import PcbService  # noqa: E402 (after path setup)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------ #
#  Default machining configurations (mirrors the Qt UI defaults)
# ------------------------------------------------------------------ #

_DEFAULT_CFG: dict = {
    "gerber": {
        "cut": -0.07,
        "travel": 0.7,
        "xy_feedrate": 250.0,
        "z_feedrate": 40.0,
        "spindle": 1000.0,
        "mirror": False,
    },
    "profile": {
        "cut": -1.8,
        "travel": 0.7,
        "xy_feedrate": 250.0,
        "z_feedrate": 40.0,
        "spindle": 1000.0,
        "multi_depth": True,
        "depth_per_pass": 0.6,
        "mirror": False,
    },
    "drill": {
        "cut": -2.1,
        "travel": 0.7,
        "xy_feedrate": 250.0,
        "z_feedrate": 40.0,
        "spindle": 1000.0,
        "mirror": False,
    },
    "pocketing": {
        "cut": -0.07,
        "travel": 0.7,
        "xy_feedrate": 250.0,
        "z_feedrate": 40.0,
        "spindle": 1000.0,
        "mirror": False,
    },
}


# ------------------------------------------------------------------ #
#  Command implementation
# ------------------------------------------------------------------ #


def cmd_generate(args: argparse.Namespace) -> int:
    """Load a PCB layer, compute paths and write a G-code file."""

    service = PcbService()

    logger.info("Loading layer '%s' from: %s", args.layer_type, args.file)
    result = service.load_layer(args.layer_type, str(Path(args.file).resolve()))

    if not result.ok:
        logger.error("Failed to load layer '%s'. Check the file path and format.", args.layer_type)
        return 1

    # Build machining config, overriding defaults with any CLI flags provided.
    cfg = dict(_DEFAULT_CFG.get(args.machining_type, {}))
    overrides = {
        "cut":         args.cut_depth,
        "travel":      args.travel_height,
        "xy_feedrate": args.xy_feedrate,
        "z_feedrate":  args.z_feedrate,
        "spindle":     args.spindle,
    }
    cfg.update({k: v for k, v in overrides.items() if v is not None})
    if args.mirror:
        cfg["mirror"] = True

    logger.info("Computing tool paths (%s) …", args.machining_type)
    path_result = service.generate_path(args.layer_type, cfg, args.machining_type)

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Generating G-code …")
    gcode_result = service.generate_gcode(
        tag=args.layer_type,
        cfg=cfg,
        machining_type=args.machining_type,
        paths=path_result.paths,
        output_folder=str(output_dir),
        mirror_type=args.mirror_axis,
    )

    if not gcode_result.gcode_path:
        logger.error("G-code generation failed.")
        return 1

    print(f"Done → {gcode_result.gcode_path}")
    return 0


# ------------------------------------------------------------------ #
#  Argument parser
# ------------------------------------------------------------------ #


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="theantfarm",
        description="TheAntFarm CLI – PCB G-code generation without the Qt GUI.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # ---- generate / gen sub-command --------------------------------
    gen = sub.add_parser(
        "generate",
        aliases=["gen"],
        help="Generate G-code from a Gerber or Excellon file.",
    )
    gen.add_argument(
        "machining_type",
        choices=["gerber", "drill", "profile", "pocketing"],
        help="Type of machining operation.",
    )
    gen.add_argument(
        "layer_type",
        help="Layer tag: top | bottom | profile | drill | noncopper_top | noncopper_bottom",
    )
    gen.add_argument("file", help="Path to Gerber (.gbr) or Excellon (.drl / .xln) file.")
    gen.add_argument(
        "--output-dir", "-o",
        default=".",
        metavar="DIR",
        help="Output directory for G-code files (default: current dir).",
    )
    gen.add_argument("--cut-depth",      type=float, metavar="MM",
                     help="Z cut depth, negative (e.g. -0.07).")
    gen.add_argument("--travel-height",  type=float, metavar="MM",
                     help="Z travel height, positive (e.g. 0.7).")
    gen.add_argument("--xy-feedrate",    type=float, metavar="MM/MIN",
                     help="XY feed rate in mm/min.")
    gen.add_argument("--z-feedrate",     type=float, metavar="MM/MIN",
                     help="Z feed rate in mm/min.")
    gen.add_argument("--spindle",        type=float, metavar="RPM",
                     help="Spindle speed in RPM.")
    gen.add_argument("--mirror",         action="store_true",
                     help="Mirror output coordinates (e.g. for bottom layers).")
    gen.add_argument("--mirror-axis",    choices=["x", "y"], default="x",
                     help="Mirror axis: x = invert Y, y = invert X (default: x).")
    gen.set_defaults(func=cmd_generate)

    return parser


# ------------------------------------------------------------------ #
#  Entry point
# ------------------------------------------------------------------ #


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
