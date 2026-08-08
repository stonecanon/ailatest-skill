#!/usr/bin/env python3
"""Render a synthetic, publication-oriented natural-science-fund figure.

The content is deliberately generic. It demonstrates how a grant figure can
connect two scientific questions to three research-content blocks, their
method/evidence layers, and three expected contributions.
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


PRIMARY_BLUE = "#4C689B"
DEEP_BLUE = "#1A4175"
BLUE_BORDER = "#7E95B7"
PALE_BLUE = "#E2E8F0"
OFF_WHITE = "#F7F8FA"
BORDER_GRAY = "#AAB6C6"
SCIENTIFIC_RED = "#D34545"
PALE_RED = "#FBE7E7"
METHOD_ORANGE = "#E88925"
PALE_ORANGE = "#FCEBD7"
EVALUATION_GREEN = "#5A9D77"
BLACK = "#000000"
MUTED = "#566273"
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
        regular = FontProperties(family="DejaVu Sans")
        family = "DejaVu Sans"
    if bold_path.exists():
        font_manager.fontManager.addfont(str(bold_path))
        bold = FontProperties(family=family, weight="bold")
    else:
        bold = FontProperties(family=family, weight="bold")
    return regular, bold


def rounded_box(ax, x: float, y: float, w: float, h: float, *, face: str,
                edge: str = BORDER_GRAY, lw: float = 1.2, radius: float = 0.08,
                zorder: int = 1) -> None:
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.012,rounding_size={radius}",
        facecolor=face, edgecolor=edge, linewidth=lw, zorder=zorder,
    ))


def icon(ax, kind: str, cx: float, cy: float, color: str = WHITE) -> None:
    lw = 1.9
    if kind == "question":
        ax.add_patch(Circle((cx, cy), 0.14, fill=False, edgecolor=color, linewidth=lw, zorder=4))
        ax.text(cx, cy - 0.005, "?", ha="center", va="center", color=color,
                fontsize=14, fontweight="bold", fontfamily="Microsoft YaHei", zorder=5)
    elif kind == "content":
        for dy in (0.10, 0.0, -0.10):
            ax.plot([cx - 0.14, cx + 0.14], [cy + dy, cy + dy], color=color,
                    linewidth=lw, solid_capstyle="round", zorder=4)
        ax.plot([cx - 0.14, cx - 0.14], [cy - 0.10, cy + 0.10], color=color, linewidth=lw, zorder=4)
        ax.plot([cx + 0.14, cx + 0.14], [cy - 0.10, cy + 0.10], color=color, linewidth=lw, zorder=4)
    elif kind == "method":
        ax.plot([cx - 0.15, cx - 0.05, cx + 0.03, cx + 0.15],
                [cy - 0.08, cy - 0.08, cy + 0.08, cy + 0.08],
                color=color, linewidth=lw, solid_capstyle="round", zorder=4)
        ax.add_patch(Polygon([(cx + 0.10, cy + 0.14), (cx + 0.19, cy + 0.08),
                              (cx + 0.10, cy + 0.02)], closed=True,
                             facecolor=color, edgecolor=color, zorder=4))
    elif kind == "outcome":
        ax.add_patch(Circle((cx, cy), 0.14, fill=False, edgecolor=color, linewidth=lw, zorder=4))
        ax.plot([cx - 0.07, cx - 0.01, cx + 0.09], [cy, cy - 0.06, cy + 0.07],
                color=color, linewidth=lw, solid_capstyle="round", zorder=4)


def header(ax, x: float, y: float, w: float, h: float, title: str, color: str,
           kind: str, bold: FontProperties, fontsize: float = 16) -> None:
    rounded_box(ax, x, y, w, h, face=color, edge=color, lw=1.0, radius=0.08, zorder=2)
    icon(ax, kind, x + 0.32, y + h / 2, WHITE)
    ax.text(x + w / 2 + 0.12, y + h / 2, title, ha="center", va="center",
            color=WHITE, fontsize=fontsize, fontproperties=bold, zorder=4)


def arrow(ax, x0: float, y0: float, x1: float, y1: float, *, color: str = DEEP_BLUE,
          lw: float = 2.0, scale: float = 16) -> None:
    ax.add_patch(FancyArrowPatch(
        (x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=scale,
        linewidth=lw, color=color, shrinkA=2, shrinkB=4, zorder=3,
    ))


def divider(ax, x0: float, x1: float, y: float) -> None:
    ax.plot([x0, x1], [y, y], color=BORDER_GRAY, linewidth=0.9,
            linestyle=(0, (4, 3)), zorder=2)


def draw_question_panel(ax, x: float, y: float, w: float, h: float,
                        questions: list[dict], regular: FontProperties,
                        bold: FontProperties) -> None:
    rounded_box(ax, x, y, w, h, face=WHITE, edge=BLUE_BORDER, lw=1.3, radius=0.08)
    header(ax, x, y + h - 0.72, w, 0.72, "科学问题", SCIENTIFIC_RED, "question", bold)
    positions = [y + h - 1.55, y + h - 3.30]
    for i, (question, yy) in enumerate(zip(questions[:2], positions)):
        ax.text(x + 0.25, yy, question["label"], ha="left", va="center",
                color=BLACK, fontsize=13.2, fontproperties=bold, zorder=4)
        ax.text(x + 0.25, yy - 0.36, question["body"], ha="left", va="center",
                color=BLACK, fontsize=10.6, fontproperties=bold, zorder=4)
        if i == 0:
            divider(ax, x + 0.22, x + w - 0.22, yy - 0.88)
    ax.text(x + 0.25, y + 0.44, "问题决定内容边界与验证路径", ha="left", va="center",
            color=BLACK, fontsize=9.7, fontproperties=regular, zorder=4)


def draw_content_panel(ax, x: float, y: float, w: float, h: float,
                       item: dict, number: int, regular: FontProperties,
                       bold: FontProperties) -> None:
    rounded_box(ax, x, y, w, h, face=WHITE, edge=BLUE_BORDER, lw=1.3, radius=0.08)
    header(ax, x, y + h - 0.72, w, 0.72, item["title"], PRIMARY_BLUE, "content", bold, fontsize=14.2)
    ax.text(x + 0.22, y + h - 1.37, item["label"], ha="left", va="center",
            color=BLACK, fontsize=13.2, fontproperties=bold, zorder=4)
    ax.text(x + 0.22, y + h - 1.73, item["body"], ha="left", va="center",
            color=BLACK, fontsize=10.3, fontproperties=bold, zorder=4)
    divider(ax, x + 0.20, x + w - 0.20, y + 2.35)
    rounded_box(ax, x + 0.16, y + 0.30, w - 0.32, 1.56, face=PALE_ORANGE,
                edge=PALE_ORANGE, lw=0.8, radius=0.05, zorder=2)
    icon(ax, "method", x + 0.38, y + 1.52, METHOD_ORANGE)
    ax.text(x + 0.66, y + 1.52, item["method_label"], ha="left", va="center",
            color=BLACK, fontsize=11.2, fontproperties=bold, zorder=4)
    ax.text(x + 0.22, y + 0.83, item["method"], ha="left", va="center",
            color=BLACK, fontsize=9.7, fontproperties=bold, zorder=4)


def draw_outcome_panel(ax, x: float, y: float, w: float, h: float,
                       outcomes: list[dict], regular: FontProperties,
                       bold: FontProperties) -> None:
    rounded_box(ax, x, y, w, h, face=WHITE, edge=EVALUATION_GREEN, lw=1.3, radius=0.08)
    header(ax, x, y + h - 0.72, w, 0.72, "预期贡献", EVALUATION_GREEN, "outcome", bold)
    positions = [y + h - 1.55, y + h - 3.02, y + h - 4.49]
    for i, (outcome, yy) in enumerate(zip(outcomes[:3], positions)):
        ax.text(x + 0.23, yy, outcome["label"], ha="left", va="center",
                color=BLACK, fontsize=12.6, fontproperties=bold, zorder=4)
        ax.text(x + 0.23, yy - 0.36, outcome["body"], ha="left", va="center",
                color=BLACK, fontsize=9.8, fontproperties=bold, zorder=4)
        if i < 2:
            divider(ax, x + 0.20, x + w - 0.20, yy - 0.75)
    # Keep the third outcome's two-line explanation clear of the panel edge;
    # the global principle band already carries the closing note.


def draw(config: dict, output_dir: Path, stem: str) -> None:
    regular, bold = load_fonts()
    fig, ax = plt.subplots(figsize=(14.8, 8.6))
    ax.axis("off")
    ax.set_xlim(0, 14.8)
    ax.set_ylim(0, 8.6)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    ax.text(0.55, 8.12, config["title"], ha="left", va="center", color=BLACK,
            fontsize=22, fontproperties=bold, zorder=5)
    ax.text(0.55, 7.72, config["subtitle"], ha="left", va="center", color=BLACK,
            fontsize=11.2, fontproperties=regular, zorder=5)
    ax.plot([0.55, 14.25], [7.47, 7.47], color=PALE_BLUE, linewidth=1.1, zorder=1)

    panel_y, panel_h = 1.52, 5.32
    qx, qw = 0.55, 2.72
    content_x, content_w, gap = 3.82, 2.34, 0.36
    outcome_x, outcome_w = 12.02, 2.23

    draw_question_panel(ax, qx, panel_y, qw, panel_h, config["questions"], regular, bold)
    for i, item in enumerate(config["contents"][:3]):
        draw_content_panel(ax, content_x + i * (content_w + gap), panel_y,
                           content_w, panel_h, item, i + 1, regular, bold)
    draw_outcome_panel(ax, outcome_x, panel_y, outcome_w, panel_h,
                       config["outcomes"], regular, bold)

    # Keep the connectors in the gaps between panels.  The three research
    # contents form one readable argument, while the methods remain inside
    # their corresponding content blocks instead of being crossed by lines.
    route_y = 4.22
    arrow(ax, qx + qw + 0.05, route_y, content_x - 0.08, route_y,
          color=SCIENTIFIC_RED, scale=13)
    for i in range(2):
        left = content_x + i * (content_w + gap) + content_w + 0.05
        right = content_x + (i + 1) * (content_w + gap) - 0.08
        arrow(ax, left, route_y, right, route_y, color=PRIMARY_BLUE, scale=12)
    third_right = content_x + 2 * (content_w + gap) + content_w + 0.05
    arrow(ax, third_right, route_y, outcome_x - 0.08, route_y,
          color=EVALUATION_GREEN, scale=13)

    rounded_box(ax, 0.55, 0.57, 13.70, 0.62, face=OFF_WHITE, edge=PALE_BLUE,
                lw=1.0, radius=0.05, zorder=1)
    ax.text(7.40, 0.88, config["principle"], ha="center", va="center", color=BLACK,
            fontsize=11.4, fontproperties=bold, zorder=4)

    output_dir.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "svg", "pdf"):
        fig.savefig(output_dir / f"{stem}.{ext}", dpi=300, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--stem", default="fund-figure-logic")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    draw(config, args.output_dir, args.stem)
    print({"output_dir": str(args.output_dir), "stem": args.stem})


if __name__ == "__main__":
    main()
