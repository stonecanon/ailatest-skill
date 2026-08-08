#!/usr/bin/env python3
"""Render a configurable process-flowchart template.

The script is deliberately content-agnostic. Pass a JSON file containing a
list of stage objects or edit DEFAULT_STAGES. Each stage may contain:

    {"title": "阶段", "icon": "evidence",
     "groups": [{"label": "输入", "body": "说明"}],
     "note": "可选注释"}

Use --orientation horizontal (default) or vertical. The default content is a
small generic example and should be replaced for a real figure.
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
from matplotlib.patches import Circle, FancyBboxPatch, Polygon

# Keep text as text in the editable SVG export.  This also makes it possible
# to verify the selected Microsoft YaHei face after the figure is embedded.
matplotlib.rcParams["svg.fonttype"] = "none"


HEADER = ["#34495E", "#2B7F97", "#4E8667", "#6E9655", "#6C7FA5", "#8D6C88"]
BLACK = "#20262D"
MUTED = "#66717C"
BORDER = "#59636C"
RULE = "#AEB6BD"
LIGHT_RULE = "#D7DCE0"

DEFAULT_STAGES = [
    {"title": "输入与观察", "icon": "evidence", "groups": [
        {"label": "对象", "body": "确定研究对象与资料来源"},
        {"label": "问题", "body": "提取需要解释的现象"},
        {"label": "范围", "body": "明确样本与边界"},
    ]},
    {"title": "分析与核验", "icon": "structure", "groups": [
        {"label": "分类", "body": "按共同属性组织证据"},
        {"label": "核验", "body": "检查定义、层次与关联"},
        {"label": "结果", "body": "形成可比较的判断"},
    ]},
    {"title": "方案与行动", "icon": "path", "groups": [
        {"label": "选项", "body": "列出可执行的处理路径"},
        {"label": "取舍", "body": "比较目标、资源与风险"},
        {"label": "行动", "body": "确定下一步实施方案"},
    ]},
    {"title": "实施与反馈", "icon": "feedback", "groups": [
        {"label": "边界", "body": "明确责任、资源与程序"},
        {"label": "交付", "body": "完成实施并记录结果"},
        {"label": "复核", "body": "用反馈修正后续决策"},
    ]},
]


def load_fonts(regular_path: str | None, bold_path: str | None) -> tuple[FontProperties, FontProperties]:
    regular = Path(regular_path).expanduser() if regular_path else Path.home() / "Library/Fonts/MicrosoftYaHei-v11.3.ttc"
    bold = Path(bold_path).expanduser() if bold_path else Path.home() / "Library/Fonts/MicrosoftYaHei-Bold-v11.3.ttc"
    font_family = None
    if regular.exists():
        font_manager.fontManager.addfont(str(regular))
        # Register the file first, then select the family by name.  This is
        # important for SVG: a direct `fname=` property can be serialized as
        # a generic DejaVu family even though the raster renderer found the
        # requested CJK face.  Family selection preserves the registered
        # Microsoft YaHei face and lets Matplotlib choose its real bold file.
        font_family = FontProperties(fname=str(regular)).get_name()
        regular_props = FontProperties(family=font_family, weight="normal")
    else:
        print(f"warning: regular font not found: {regular}")
        regular_props = FontProperties(family="DejaVu Sans")
    if bold.exists():
        font_manager.fontManager.addfont(str(bold))
        if font_family is None:
            font_family = FontProperties(fname=str(bold)).get_name()
        bold_props = FontProperties(family=font_family, weight="bold")
    else:
        print(f"warning: bold font not found: {bold}")
        bold_props = FontProperties(family="DejaVu Sans", weight="bold")
    return regular_props, bold_props


def draw_icon(ax, cx: float, cy: float, kind: str, color: str = "white") -> None:
    lw = 1.7
    if kind == "evidence":
        ax.add_patch(Circle((cx - 0.035, cy + 0.025), 0.085, fill=False,
                            edgecolor=color, linewidth=lw, zorder=4))
        ax.plot([cx + 0.030, cx + 0.125], [cy - 0.045, cy - 0.140],
                color=color, linewidth=lw, solid_capstyle="round", zorder=4)
    elif kind == "structure":
        for dy in (0.085, 0.0, -0.085):
            ax.plot([cx - 0.12, cx + 0.12], [cy + dy, cy + dy],
                    color=color, linewidth=lw, solid_capstyle="round", zorder=4)
        ax.plot([cx - 0.12, cx - 0.12], [cy - 0.085, cy + 0.085], color=color, linewidth=lw, zorder=4)
        ax.plot([cx + 0.12, cx + 0.12], [cy - 0.085, cy + 0.085], color=color, linewidth=lw, zorder=4)
    elif kind == "path":
        ax.plot([cx - 0.13, cx - 0.04, cx + 0.025, cx + 0.12],
                [cy - 0.08, cy - 0.08, cy + 0.08, cy + 0.08],
                color=color, linewidth=lw, solid_capstyle="round", solid_joinstyle="round", zorder=4)
        ax.add_patch(Polygon([(cx + 0.07, cy + 0.14), (cx + 0.16, cy + 0.08),
                              (cx + 0.07, cy + 0.02)], closed=True,
                             facecolor=color, edgecolor=color, zorder=4))
    elif kind == "analysis":
        ax.plot([cx - 0.13, cx + 0.13], [cy - 0.13, cy - 0.13],
                color=color, linewidth=lw, solid_capstyle="round", zorder=4)
        for dx, height in ((-0.09, 0.10), (0.0, 0.18), (0.09, 0.27)):
            ax.plot([cx + dx, cx + dx], [cy - 0.13, cy - 0.13 + height],
                    color=color, linewidth=lw, solid_capstyle="round", zorder=4)
    elif kind == "decision":
        ax.add_patch(Polygon([(cx, cy + 0.15), (cx + 0.15, cy),
                              (cx, cy - 0.15), (cx - 0.15, cy)], closed=True,
                             fill=False, edgecolor=color, linewidth=lw, zorder=4))
        ax.plot([cx - 0.23, cx - 0.14], [cy, cy], color=color, linewidth=lw,
                solid_capstyle="round", zorder=4)
        ax.plot([cx + 0.14, cx + 0.23], [cy, cy], color=color, linewidth=lw,
                solid_capstyle="round", zorder=4)
    elif kind == "database":
        ax.add_patch(FancyBboxPatch((cx - 0.12, cy - 0.10), 0.24, 0.20,
                                    boxstyle="round,pad=0.018,rounding_size=0.06",
                                    facecolor="none", edgecolor=color, linewidth=lw, zorder=4))
        ax.plot([cx - 0.12, cx + 0.12], [cy + 0.02, cy + 0.02],
                color=color, linewidth=lw, zorder=4)
        ax.plot([cx - 0.12, cx + 0.12], [cy - 0.06, cy - 0.06],
                color=color, linewidth=lw, zorder=4)
    elif kind == "delivery":
        ax.add_patch(plt.Rectangle((cx - 0.12, cy - 0.10), 0.20, 0.20,
                                   fill=False, edgecolor=color, linewidth=lw, zorder=4))
        ax.plot([cx - 0.02, cx + 0.17], [cy, cy], color=color, linewidth=lw,
                solid_capstyle="round", zorder=4)
        ax.add_patch(Polygon([(cx + 0.12, cy + 0.07), (cx + 0.20, cy),
                              (cx + 0.12, cy - 0.07)], closed=True,
                             facecolor=color, edgecolor=color, zorder=4))
    elif kind == "review":
        ax.add_patch(Circle((cx, cy), 0.13, fill=False, edgecolor=color,
                            linewidth=lw, zorder=4))
        ax.plot([cx - 0.06, cx - 0.01, cx + 0.08],
                [cy, cy - 0.05, cy + 0.07], color=color, linewidth=lw,
                solid_capstyle="round", solid_joinstyle="round", zorder=4)
    else:
        ax.add_patch(FancyBboxPatch((cx - 0.11, cy - 0.14), 0.22, 0.27,
                                    boxstyle="round,pad=0.018,rounding_size=0.025",
                                    facecolor="none", edgecolor=color, linewidth=lw, zorder=4))
        ax.plot([cx - 0.06, cx - 0.015, cx + 0.075],
                [cy - 0.015, cy - 0.065, cy + 0.055], color=color,
                linewidth=lw, solid_capstyle="round", solid_joinstyle="round", zorder=4)


def filled_arrow(ax, x0: float, x1: float, y: float, color: str, *, vertical: bool = False) -> None:
    if vertical:
        # In vertical mode x0/x1 are the source/target y coordinates and y is
        # the horizontal centre line.  The target may be above or below the
        # source, so construct the same filled arrow in either direction.
        start, end = x0, x1
        length = max(abs(end - start), 0.05)
        head = min(0.18, length * 0.48)
        tail = min(0.14, 0.34 * 0.55)
        direction = 1 if end >= start else -1
        shaft_end = end - direction * head
        vertices = [(y - tail / 2, start), (y - tail / 2, shaft_end),
                    (y - 0.34 / 2, shaft_end), (y, end),
                    (y + 0.34 / 2, shaft_end), (y + tail / 2, shaft_end),
                    (y + tail / 2, start)]
        ax.add_patch(Polygon(vertices, closed=True, facecolor=color,
                              edgecolor=color, linewidth=0, zorder=4))
        return

    length = max(x1 - x0, 0.05)
    head = min(0.18, length * 0.48)
    tail = min(0.14, 0.34 * 0.55)
    vertices = [(x0, y - tail / 2), (x1 - head, y - tail / 2),
                (x1 - head, y - 0.34 / 2), (x1, y),
                (x1 - head, y + 0.34 / 2), (x1 - head, y + tail / 2),
                (x0, y + tail / 2)]
    ax.add_patch(Polygon(vertices, closed=True, facecolor=color, edgecolor=color, linewidth=0, zorder=4))


def draw_horizontal(stages: list[dict], regular: FontProperties, bold: FontProperties,
                    bottom_labels: list[str] | None = None) -> plt.Figure:
    n = len(stages)
    fig_w, fig_h = (15.8, 6.9) if n <= 4 else (max(15.8, 3.7 * n + 1.4), 6.9)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.axis("off")
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    outer_left, outer_right = 0.42, fig_w - 0.42
    gap = min(0.56, max(0.30, (outer_right - outer_left) * 0.035))
    panel_w = (outer_right - outer_left - gap * (n - 1)) / n
    panel_y, panel_h, header_h = 1.30, 5.03, 0.63
    xs = [outer_left + i * (panel_w + gap) for i in range(n)]

    def rule(x0: float, x1: float, y: float) -> None:
        ax.plot([x0, x1], [y, y], color=RULE, lw=0.9,
                linestyle=(0, (4, 3)), dash_capstyle="butt", zorder=2)

    for i, (x, stage) in enumerate(zip(xs, stages)):
        color = HEADER[i % len(HEADER)]
        ax.add_patch(plt.Rectangle((x, panel_y), panel_w, panel_h, facecolor="white",
                                   edgecolor=BORDER, linewidth=1.0, zorder=1))
        ax.add_patch(plt.Rectangle((x, panel_y + panel_h - header_h), panel_w, header_h,
                                   facecolor=color, edgecolor=color, linewidth=1.0, zorder=2))
        header_y = panel_y + panel_h - header_h / 2
        draw_icon(ax, x + 0.34, header_y, stage.get("icon", "path"))
        ax.text(x + panel_w / 2 + 0.10, header_y, stage["title"], ha="center", va="center",
                fontsize=18, fontproperties=bold, color="white", zorder=3)

        groups = stage.get("groups", [])[:4]
        if not groups:
            continue
        content_top, content_bottom = 5.34, 2.12
        step = (content_top - content_bottom) / max(len(groups), 1)
        for j, group in enumerate(groups):
            y = content_top - j * step
            ax.text(x + 0.23, y, group.get("label", ""), ha="left", va="center",
                    fontsize=15, fontproperties=bold, color=color, zorder=3)
            ax.text(x + 0.23, y - 0.34, group.get("body", ""), ha="left", va="center",
                    fontsize=12, fontproperties=bold, color=BLACK, zorder=3)
            if j < len(groups) - 1:
                rule(x + 0.20, x + panel_w - 0.20, y - step + 0.12)
        if stage.get("note"):
            ax.text(x + 0.23, panel_y + 0.24, stage["note"], ha="left", va="center",
                    fontsize=10.6, fontproperties=regular, color=MUTED, zorder=3)

    arrow_y = panel_y + panel_h / 2
    for left, right in zip(xs[:-1], xs[1:]):
        filled_arrow(ax, left + panel_w + 0.08, right - 0.08, arrow_y, HEADER[0])

    if bottom_labels:
        bottom_y, bottom_h = 0.70, 0.72
        ax.add_patch(plt.Rectangle((outer_left, bottom_y - bottom_h / 2), outer_right - outer_left,
                                   bottom_h, facecolor="#F7F8F9", edgecolor=LIGHT_RULE,
                                   linewidth=1.0, zorder=1))
        centers = [x + panel_w / 2 for x in xs]
        for center, label in zip(centers, bottom_labels[:n]):
            ax.text(center, bottom_y, label, ha="center", va="center", fontsize=14.6,
                    fontproperties=bold, color=BLACK, zorder=3)
        for left, right in zip(xs[:-1], xs[1:]):
            filled_arrow(ax, left + panel_w + 0.10, right - 0.10, bottom_y, HEADER[0])
    return fig


def draw_vertical(stages: list[dict], regular: FontProperties, bold: FontProperties) -> plt.Figure:
    n = len(stages)
    max_groups = max(2, min(4, max((len(stage.get("groups", [])) for stage in stages), default=2)))
    box_h = max(1.05, 0.63 + max_groups * 0.32 + 0.20)
    gap = 0.55
    fig_w = 8.0
    fig_h = max(8.0, 0.65 + n * box_h + max(n - 1, 0) * gap + 0.70)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.axis("off")
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    x, box_w = 0.75, fig_w - 1.50
    ys = [fig_h - 0.65 - i * (box_h + gap) - box_h for i in range(n)]
    for i, (y, stage) in enumerate(zip(ys, stages)):
        color = HEADER[i % len(HEADER)]
        ax.add_patch(plt.Rectangle((x, y), box_w, box_h, facecolor="white",
                                   edgecolor=BORDER, linewidth=1.0, zorder=1))
        header_h = 0.32
        ax.add_patch(plt.Rectangle((x, y + box_h - header_h), box_w, header_h,
                                   facecolor=color, edgecolor=color, linewidth=1.0, zorder=2))
        draw_icon(ax, x + 0.32, y + box_h - header_h / 2, stage.get("icon", "path"))
        ax.text(x + box_w / 2 + 0.08, y + box_h - header_h / 2, stage["title"],
                ha="center", va="center", fontsize=15, fontproperties=bold, color="white", zorder=3)
        groups = stage.get("groups", [])[:4]
        for j, group in enumerate(groups):
            yy = y + box_h - header_h - 0.25 - j * 0.32
            ax.text(x + 0.22, yy, group.get("label", ""), ha="left", va="center",
                    fontsize=11.5, fontproperties=bold, color=color, zorder=3)
            ax.text(x + 1.45, yy, group.get("body", ""), ha="left", va="center",
                    fontsize=10.5, fontproperties=bold, color=BLACK, zorder=3)
        if i < n - 1:
            filled_arrow(ax, ys[i] - 0.06, ys[i + 1] + box_h + 0.06,
                         x + box_w / 2, HEADER[0], vertical=True)
    return fig


def save_figure(fig: plt.Figure, output_dir: Path, stem: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "svg", "pdf"):
        fig.savefig(output_dir / f"{stem}.{ext}", dpi=300, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw a configurable process flowchart template")
    parser.add_argument("--stages-json", type=Path, help="JSON file containing a list of stage objects")
    parser.add_argument("--orientation", choices=("horizontal", "vertical"), default="horizontal")
    parser.add_argument("--output-dir", type=Path, default=Path("flowchart_output"))
    parser.add_argument("--stem", default="process_flowchart")
    parser.add_argument("--bottom-labels", nargs="*", help="Optional labels for the horizontal lifecycle band")
    parser.add_argument("--regular-font")
    parser.add_argument("--bold-font")
    args = parser.parse_args()

    stages = DEFAULT_STAGES
    if args.stages_json:
        stages = json.loads(args.stages_json.read_text(encoding="utf-8"))
    if not 2 <= len(stages) <= 6:
        raise SystemExit("stages-json must contain between 2 and 6 stages")
    regular, bold = load_fonts(args.regular_font, args.bold_font)
    if args.orientation == "horizontal":
        fig = draw_horizontal(stages, regular, bold, args.bottom_labels)
    else:
        fig = draw_vertical(stages, regular, bold)
    save_figure(fig, args.output_dir, args.stem)
    print({"stages": len(stages), "orientation": args.orientation, "output_dir": str(args.output_dir)})


if __name__ == "__main__":
    main()
