#!/usr/bin/env python3
"""Audit grant-proposal SVG files against the user's figure style contract."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


SVG_NS = {"svg": "http://www.w3.org/2000/svg"}
ALLOWED_TEXT_FILLS = {"#000000", "#FFFFFF"}
PRIMARY_BLUE = "#4C689B"


def number(value: str | None, default: float = 0.0) -> float:
    if value is None:
        return default
    match = re.search(r"-?\d+(?:\.\d+)?", value)
    return float(match.group(0)) if match else default


def style_value(node: ET.Element, name: str) -> str:
    """Read an SVG presentation attribute or its inline style equivalent."""
    direct = node.get(name)
    if direct:
        return direct
    style = node.get("style") or ""
    for declaration in style.split(";"):
        if ":" not in declaration:
            continue
        key, value = declaration.split(":", 1)
        if key.strip().lower() == name.lower():
            return value.strip()
    return ""


def audit(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        return [f"cannot parse SVG: {exc}"], warnings

    raw = path.read_text(encoding="utf-8").upper()
    if PRIMARY_BLUE not in raw:
        errors.append(f"missing primary blue {PRIMARY_BLUE}")

    texts = root.findall(".//svg:text", SVG_NS)
    if not texts:
        warnings.append("contains no SVG text elements")
    for index, node in enumerate(texts, start=1):
        # SVG's default text paint is black; Matplotlib omits an explicit
        # fill for black text, so treat a missing presentation value as the
        # contract's #000000 rather than reporting a false error.
        fill = (style_value(node, "fill") or "#000000").upper()
        if fill not in ALLOWED_TEXT_FILLS:
            errors.append(f"text {index} uses disallowed fill {fill or '[missing]'}")
        family = style_value(node, "font-family")
        if "MICROSOFT YAHEI" not in family.upper() and "微软雅黑" not in family:
            errors.append(f"text {index} is missing Microsoft YaHei font stack")

    gaussian = root.findall(".//svg:feGaussianBlur", SVG_NS)
    if gaussian:
        errors.append("uses feGaussianBlur; broad soft shadows are not allowed")

    drops = root.findall(".//svg:feDropShadow", SVG_NS)
    if len(drops) > 1:
        errors.append(f"uses {len(drops)} drop-shadow definitions; use one shared short shadow")
    for node in drops:
        dx = number(node.get("dx"))
        dy = number(node.get("dy"))
        std = number(node.get("stdDeviation"))
        opacity = number(node.get("flood-opacity"), 1.0)
        if not 0 <= dx <= 6 or not 0 <= dy <= 6:
            errors.append(f"shadow offset is too large or not lower-right: dx={dx}, dy={dy}")
        if std > 2:
            errors.append(f"shadow is too soft: stdDeviation={std}")
        if opacity > 0.35:
            errors.append(f"shadow is too dark: flood-opacity={opacity}")

    for index, node in enumerate(root.findall(".//svg:rect", SVG_NS), start=1):
        rx = number(node.get("rx"))
        if rx > 12:
            warnings.append(f"rect {index} has large corner radius rx={rx}")

    if "VIEWBOX" not in raw:
        errors.append("missing viewBox")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("svg", nargs="+", type=Path)
    args = parser.parse_args()

    failed = False
    for path in args.svg:
        errors, warnings = audit(path)
        status = "FAIL" if errors else "PASS"
        print(f"[{status}] {path}")
        for warning in warnings:
            print(f"  warning: {warning}")
        for error in errors:
            print(f"  error: {error}")
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
