#!/usr/bin/env python3
"""Render a synthetic proposal-argument map for the writing skill.

The figure is intentionally a scientific-argument architecture rather than a
generic four-step workflow: basis and gap lead to two questions, three
research-content blocks carry their methods/evidence, and the chain closes at
contribution and application boundary.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon


DEEP_BLUE = "#1A4175"
PRIMARY_BLUE = "#4C689B"
BLUE_BORDER = "#7E95B7"
PALE_BLUE = "#E2E8F0"
OFF_WHITE = "#F7F8FA"
BORDER_GRAY = "#AAB6C6"
SCIENTIFIC_RED = "#D34545"
PALE_RED = "#FBE7E7"
METHOD_ORANGE = "#E88925"
PALE_ORANGE = "#FCEBD7"
EVALUATION_GREEN = "#5A9D77"
PALE_GREEN = "#E7F2EC"
BLACK = "#000000"
WHITE = "#FFFFFF"

matplotlib.rcParams["svg.fonttype"] = "none"


def load_fonts() -> tuple[FontProperties, FontProperties]:
    regular_path = Path.home() / "Library/Fonts/MicrosoftYaHei-v11.3.ttc"
    bold_path = Path.home() / "Library/Fonts/MicrosoftYaHei-Bold-v11.3.ttc"
    if regular_path.exists():
        font_manager.fontManager.addfont(str(regular_path))
        family = FontProperties(fname=str(regular_path)).get_name()
        regular = FontProperties(family=family, weight="normal")
    else:
        family = "DejaVu Sans"
        regular = FontProperties(family=family)
    if bold_path.exists():
        font_manager.fontManager.addfont(str(bold_path))
    bold = FontProperties(family=family, weight="bold")
    return regular, bold


def box(ax, x: float, y: float, w: float, h: float, *, face: str,
        edge: str = BORDER_GRAY, lw: float = 1.2, radius: float = 0.07,
        zorder: int = 1) -> None:
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.012,rounding_size={radius}",
        facecolor=face, edgecolor=edge, linewidth=lw, zorder=zorder,
    ))


def icon(ax, kind: str, cx: float, cy: float, color: str = WHITE) -> None:
    lw = 1.8
    if kind == "basis":
        ax.add_patch(Circle((cx - 0.03, cy + 0.03), 0.10, fill=False,
                            edgecolor=color, linewidth=lw, zorder=4))
        ax.plot([cx + 0.04, cx + 0.14], [cy - 0.05, cy - 0.15], color=color,
                linewidth=lw, solid_capstyle="round", zorder=4)
    elif kind == "content":
        ax.plot([cx - 0.14, cx + 0.14], [cy + 0.10, cy + 0.10], color=color,
                linewidth=lw, zorder=4)
        ax.plot([cx - 0.14, cx + 0.14], [cy, cy], color=color, linewidth=lw, zorder=4)
        ax.plot([cx - 0.14, cx + 0.14], [cy - 0.10, cy - 0.10], color=color,
                linewidth=lw, zorder=4)
    elif kind == "method":
        ax.plot([cx - 0.14, cx - 0.05, cx + 0.03, cx + 0.13],
                [cy - 0.08, cy - 0.08, cy + 0.08, cy + 0.08], color=color,
                linewidth=lw, solid_capstyle="round", zorder=4)
        ax.add_patch(Polygon([(cx + 0.08, cy + 0.14), (cx + 0.18, cy + 0.08),
                              (cx + 0.08, cy + 0.02)], closed=True,
                             facecolor=color, edgecolor=color, zorder=4))
    elif kind == "outcome":
        ax.add_patch(Circle((cx, cy), 0.13, fill=False, edgecolor=color,
                            linewidth=lw, zorder=4))
        ax.plot([cx - 0.07, cx - 0.01, cx + 0.08],
                [cy, cy - 0.05, cy + 0.07], color=color, linewidth=lw,
                solid_capstyle="round", zorder=4)


def header(ax, x: float, y: float, w: float, h: float, title: str,
           color: str, kind: str, bold: FontProperties, fontsize: float = 15) -> None:
    box(ax, x, y, w, h, face=color, edge=color, lw=1.0, radius=0.07, zorder=2)
    icon(ax, kind, x + 0.30, y + h / 2, WHITE)
    ax.text(x + w / 2 + 0.09, y + h / 2, title, ha="center", va="center",
            color=WHITE, fontsize=fontsize, fontproperties=bold, zorder=4)


def arrow(ax, x0: float, y0: float, x1: float, y1: float, *, color: str = DEEP_BLUE,
          scale: float = 15, lw: float = 2.0) -> None:
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>",
                                 mutation_scale=scale, linewidth=lw, color=color,
                                 shrinkA=2, shrinkB=4, zorder=3))


def dashed(ax, x0: float, x1: float, y: float) -> None:
    ax.plot([x0, x1], [y, y], color=BORDER_GRAY, linewidth=0.9,
            linestyle=(0, (4, 3)), zorder=2)


def draw_basis(ax, x: float, y: float, w: float, h: float, basis: dict,
               regular: FontProperties, bold: FontProperties) -> None:
    box(ax, x, y, w, h, face=WHITE, edge=SCIENTIFIC_RED, lw=1.3, radius=0.07)
    header(ax, x, y + h - 0.40, w, 0.40, "立项依据", SCIENTIFIC_RED, "basis", bold, 13.5)
    body_y = y + 0.20
    col_w = (w - 0.48) / 3
    parts = [basis["object"], basis["gap"]]
    for i, part in enumerate(parts):
        xx = x + 0.20 + i * col_w
        ax.text(xx, body_y + 0.50, part["label"], ha="left", va="center", color=BLACK,
                fontsize=9.4, fontproperties=bold, zorder=4)
        ax.text(xx, body_y + 0.23, part["body"], ha="left", va="center",
                color=BLACK, fontsize=8.0, fontproperties=regular, zorder=4)
    for i in (1, 2):
        xx = x + 0.20 + i * col_w - 0.12
        ax.plot([xx, xx], [body_y + 0.10, body_y + 0.65], color=PALE_BLUE,
                linewidth=1.0, zorder=2)
    qx = x + 0.20 + 2 * col_w
    ax.text(qx, body_y + 0.50, "科学问题", ha="left", va="center", color=BLACK,
            fontsize=9.4, fontproperties=bold, zorder=4)
    ax.text(qx, body_y + 0.28, basis["questions"][0], ha="left", va="center",
            color=BLACK, fontsize=8.1, fontproperties=regular, zorder=4)
    ax.text(qx, body_y + 0.08, basis["questions"][1], ha="left", va="center",
            color=BLACK, fontsize=8.1, fontproperties=regular, zorder=4)


def draw_content(ax, x: float, y: float, w: float, h: float, item: dict,
                 number: int, regular: FontProperties, bold: FontProperties) -> None:
    content_h = 1.58
    method_h = 1.35
    box(ax, x, y + h - content_h, w, content_h, face=WHITE, edge=BLUE_BORDER,
        lw=1.3, radius=0.07)
    header(ax, x, y + h - 0.48, w, 0.48, item["title"], PRIMARY_BLUE, "content", bold, 12.1)
    ax.text(x + 0.25, y + h - 0.91, item["content"], ha="left", va="center",
            color=BLACK, fontsize=9.8, linespacing=1.35, fontproperties=bold, zorder=4)
    ax.text(x + 0.25, y + h - 1.39, item["detail"], ha="left", va="center",
            color=BLACK, fontsize=8.1, linespacing=1.35, fontproperties=regular, zorder=4)
    arrow(ax, x + w / 2, y + h - content_h - 0.05, x + w / 2,
          y + h - content_h - 0.28, color=METHOD_ORANGE, scale=11, lw=1.5)
    box(ax, x, y, w, method_h, face=PALE_ORANGE, edge=METHOD_ORANGE,
        lw=1.0, radius=0.07)
    icon(ax, "method", x + 0.27, y + method_h - 0.27, METHOD_ORANGE)
    ax.text(x + 0.65, y + method_h - 0.27, "研究方案与证据",
            ha="left", va="center", color=BLACK, fontsize=9.2,
            fontproperties=bold, zorder=4)
    ax.text(x + 0.25, y + 0.47, item["method"], ha="left", va="center",
            color=BLACK, fontsize=8.2, linespacing=1.35, fontproperties=regular, zorder=4)


def draw_outcomes(ax, x: float, y: float, w: float, h: float, outcomes: list[dict],
                  regular: FontProperties, bold: FontProperties) -> None:
    box(ax, x, y, w, h, face=WHITE, edge=EVALUATION_GREEN, lw=1.3, radius=0.07)
    header(ax, x, y + h - 0.55, w, 0.55, "科学贡献", EVALUATION_GREEN, "outcome", bold, 14.5)
    cols = [x + 0.20, x + w / 3 + 0.04, x + 2 * w / 3 - 0.10]
    for i, (outcome, xx) in enumerate(zip(outcomes[:3], cols)):
        ax.text(xx, y + h - 0.92, outcome["label"], ha="left", va="center", color=BLACK,
                fontsize=9.9, fontproperties=bold, zorder=4)
        ax.text(xx, y + h - 1.08, outcome["body"], ha="left", va="center", color=BLACK,
                fontsize=8.5, fontproperties=regular, zorder=4)
        if i < 2:
            ax.plot([xx + w / 3 - 0.22, xx + w / 3 - 0.22], [y + 0.22, y + h - 0.75],
                    color=PALE_BLUE, linewidth=1.0, zorder=2)


def draw(config: dict, output_dir: Path, stem: str) -> None:
    regular, bold = load_fonts()
    fig, ax = plt.subplots(figsize=(15.2, 9.0))
    ax.axis("off")
    ax.set_xlim(0, 15.2)
    ax.set_ylim(0, 9.0)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    ax.text(0.55, 8.55, config["title"], ha="left", va="center", color=BLACK,
            fontsize=21, fontproperties=bold, zorder=5)
    ax.text(0.55, 8.18, config["subtitle"], ha="left", va="center", color=BLACK,
            fontsize=10.5, fontproperties=regular, zorder=5)
    ax.plot([0.55, 14.65], [7.92, 7.92], color=PALE_BLUE, linewidth=1.1, zorder=1)

    basis_x, basis_y, basis_w, basis_h = 0.65, 6.27, 13.90, 1.22
    draw_basis(ax, basis_x, basis_y, basis_w, basis_h, config["basis"], regular, bold)
    arrow(ax, 7.60, 6.17, 7.60, 6.04, color=SCIENTIFIC_RED, scale=12, lw=1.6)

    content_y, content_h = 2.85, 3.20
    content_x, content_w, content_gap = 0.90, 3.66, 0.58
    for i, item in enumerate(config["contents"][:3]):
        draw_content(ax, content_x + i * (content_w + content_gap), content_y,
                     content_w, content_h, item, i + 1, regular, bold)
    for i in range(2):
        left = content_x + (i + 1) * content_w + i * content_gap + 0.06
        right = content_x + (i + 1) * (content_w + content_gap) - 0.06
        arrow(ax, left, content_y + 1.48, right, content_y + 1.48,
              color=PRIMARY_BLUE, scale=13, lw=1.8)

    outcome_x, outcome_y, outcome_w, outcome_h = 0.65, 1.37, 13.90, 1.15
    draw_outcomes(ax, outcome_x, outcome_y, outcome_w, outcome_h,
                  config["outcomes"], regular, bold)
    arrow(ax, 7.60, content_y - 0.08, 7.60, outcome_y + outcome_h + 0.10,
          color=EVALUATION_GREEN, scale=12, lw=1.6)

    box(ax, 0.65, 0.44, 13.90, 0.58, face=DEEP_BLUE, edge=DEEP_BLUE,
        lw=1.0, radius=0.05, zorder=1)
    ax.text(7.60, 0.73, config["application"], ha="center", va="center",
            color=WHITE, fontsize=10.0, fontproperties=bold, zorder=4)

    output_dir.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "svg", "pdf"):
        fig.savefig(output_dir / f"{stem}.{ext}", dpi=300, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--stem", default="proposal-core-logic")
    args = parser.parse_args()
    draw(json.loads(args.config.read_text(encoding="utf-8")), args.output_dir, args.stem)
    print({"output_dir": str(args.output_dir), "stem": args.stem})


if __name__ == "__main__":
    main()
