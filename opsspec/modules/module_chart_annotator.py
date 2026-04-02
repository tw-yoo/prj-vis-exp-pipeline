"""PIL-based chart image annotator.

Draws visual annotations (reference lines, text labels, bands, bar highlights,
circles) on top of an existing chart image programmatically using Pillow.

Coordinate mapping:
  - chart_area defines the plot area bounding box in image pixels.
  - y-axis: y_min (bottom) → y_max (top) mapped to pixel range.
  - x-axis (categorical): evenly-spaced categories mapped to bar centers.

Entry point: annotate_chart_steps()
"""
from __future__ import annotations

import base64
import io
import logging
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

# ── Colour helpers ─────────────────────────────────────────────────────────────

def _parse_hex_color(hex_color: str) -> Tuple[int, int, int]:
    """Parse a #RRGGBB string into an (R, G, B) tuple."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        return (228, 87, 86)  # fallback red
    try:
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except ValueError:
        return (228, 87, 86)


def _rgba(hex_color: str, alpha: int = 255) -> Tuple[int, int, int, int]:
    r, g, b = _parse_hex_color(hex_color)
    return (r, g, b, alpha)


# ── Coordinate helpers ─────────────────────────────────────────────────────────

class ChartCoords:
    """Translates data-space values to image pixel coordinates."""

    def __init__(
        self,
        *,
        chart_x: int,
        chart_y: int,
        chart_width: int,
        chart_height: int,
        y_min: float,
        y_max: float,
        x_categories: List[str],
    ) -> None:
        self.chart_x = chart_x
        self.chart_y = chart_y
        self.chart_width = chart_width
        self.chart_height = chart_height
        self.y_min = y_min
        self.y_max = y_max
        self.x_categories = x_categories

    def data_y_to_px(self, value: float) -> int:
        """Map a y data value to the pixel y coordinate (top-down PIL convention)."""
        y_range = self.y_max - self.y_min
        if y_range == 0:
            return self.chart_y + self.chart_height // 2
        frac = (value - self.y_min) / y_range
        # frac=0 → bottom (chart_y + chart_height), frac=1 → top (chart_y)
        return int(self.chart_y + self.chart_height * (1.0 - frac))

    def category_to_px(self, category: str) -> Optional[int]:
        """Map a categorical x label to the pixel x-center of its bar."""
        n = len(self.x_categories)
        if n == 0:
            return None
        try:
            idx = self.x_categories.index(category)
        except ValueError:
            return None
        bar_width = self.chart_width / n
        return int(self.chart_x + bar_width * (idx + 0.5))

    def category_bar_bounds(self, category: str) -> Optional[Tuple[int, int, int, int]]:
        """Return (x0, y0_data_zero, x1, chart_bottom) pixel rect for a bar."""
        n = len(self.x_categories)
        if n == 0:
            return None
        try:
            idx = self.x_categories.index(category)
        except ValueError:
            return None
        bar_width = self.chart_width / n
        x0 = int(self.chart_x + bar_width * idx)
        x1 = int(self.chart_x + bar_width * (idx + 1))
        y_top = self.chart_y                          # chart area top
        y_bot = self.chart_y + self.chart_height      # chart area bottom
        return (x0, y_top, x1, y_bot)


# ── Drawing primitives ─────────────────────────────────────────────────────────

def _draw_reference_line(
    draw: ImageDraw.ImageDraw,
    coords: ChartCoords,
    value: float,
    label: Optional[str],
    color: str = "#e45756",
    line_width: int = 2,
) -> None:
    """Draw a dashed horizontal reference line at the given y data value."""
    py = coords.data_y_to_px(value)
    x0 = coords.chart_x
    x1 = coords.chart_x + coords.chart_width
    rgb = _parse_hex_color(color)

    # Draw dashed line (4 px on / 4 px off)
    dash_on, dash_off = 8, 6
    x = x0
    while x < x1:
        x_end = min(x + dash_on, x1)
        draw.line([(x, py), (x_end, py)], fill=rgb, width=line_width)
        x += dash_on + dash_off

    if label:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 13)
        except OSError:
            font = ImageFont.load_default()
        tx = x0 + 4
        ty = py - 16
        draw.text((tx, ty), label, fill=rgb, font=font)


def _draw_text_label(
    draw: ImageDraw.ImageDraw,
    coords: ChartCoords,
    label: str,
    x_px: Optional[int],
    y_px: Optional[int],
    color: str = "#e45756",
    dx: int = 5,
    dy: int = -12,
) -> None:
    """Draw a text label at the given pixel position."""
    if x_px is None or y_px is None:
        return
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 13)
    except OSError:
        font = ImageFont.load_default()
    rgb = _parse_hex_color(color)
    draw.text((x_px + dx, y_px + dy), label, fill=rgb, font=font)


def _draw_band(
    overlay: Image.Image,
    coords: ChartCoords,
    y_lower: float,
    y_upper: float,
    color: str = "#4c78a8",
    opacity: float = 0.15,
) -> None:
    """Draw a shaded horizontal band between two y data values."""
    alpha = int(opacity * 255)
    py_lower = coords.data_y_to_px(y_lower)
    py_upper = coords.data_y_to_px(y_upper)
    x0 = coords.chart_x
    x1 = coords.chart_x + coords.chart_width
    y0 = min(py_lower, py_upper)
    y1 = max(py_lower, py_upper)
    r, g, b = _parse_hex_color(color)
    band_draw = ImageDraw.Draw(overlay)
    band_draw.rectangle([x0, y0, x1, y1], fill=(r, g, b, alpha))


def _draw_highlight_bars(
    overlay: Image.Image,
    coords: ChartCoords,
    highlight_categories: List[str],
    all_categories: List[str],
    highlight_color: str = "#e45756",
    dim_color: str = "#d3d3d3",
    highlight_alpha: int = 0,   # 0 = no overlay (already highlighted in chart)
    dim_alpha: int = 160,       # dim non-highlighted bars
) -> None:
    """Overlay a semi-transparent tint on non-highlighted bars to dim them."""
    draw = ImageDraw.Draw(overlay)
    highlight_set = set(highlight_categories)
    r, g, b = _parse_hex_color(dim_color)

    for cat in all_categories:
        if cat in highlight_set:
            continue
        bounds = coords.category_bar_bounds(cat)
        if bounds is None:
            continue
        x0, y0, x1, y1 = bounds
        draw.rectangle([x0, y0, x1, y1], fill=(r, g, b, dim_alpha))


def _draw_circle_emphasis(
    draw: ImageDraw.ImageDraw,
    coords: ChartCoords,
    x_category: Optional[str],
    y_value: Optional[float],
    radius: int = 14,
    color: str = "#e45756",
    line_width: int = 2,
) -> None:
    """Draw a circle around a specific data point."""
    if x_category is not None:
        px = coords.category_to_px(x_category)
    else:
        px = coords.chart_x + coords.chart_width // 2
    if y_value is not None:
        py = coords.data_y_to_px(y_value)
    else:
        py = coords.chart_y + coords.chart_height // 2
    if px is None:
        return
    rgb = _parse_hex_color(color)
    draw.ellipse(
        [(px - radius, py - radius), (px + radius, py + radius)],
        outline=rgb,
        width=line_width,
    )


# ── Per-annotation dispatcher ──────────────────────────────────────────────────

def _apply_annotation(
    base_img: Image.Image,
    overlay: Image.Image,
    draw: ImageDraw.ImageDraw,
    coords: ChartCoords,
    ann: Dict[str, Any],
) -> List[str]:
    """Apply a single annotation dict. Returns a list of warning strings."""
    warnings: List[str] = []
    ann_type = (ann.get("type") or "").strip()

    if ann_type == "reference_line":
        value = ann.get("value")
        if value is None:
            warnings.append("reference_line: missing 'value'")
            return warnings
        _draw_reference_line(
            draw=draw,
            coords=coords,
            value=float(value),
            label=ann.get("label"),
            color=ann.get("color", "#e45756"),
            line_width=ann.get("line_width", 2),
        )

    elif ann_type == "text_label":
        label = ann.get("label")
        if not label:
            warnings.append("text_label: missing 'label'")
            return warnings
        x_cat = ann.get("x_category")
        y_val = ann.get("y_value")
        x_px: Optional[int] = ann.get("x_px")
        y_px: Optional[int] = ann.get("y_px")
        # Resolve pixel positions from data coords if px not given directly
        if x_px is None and x_cat is not None:
            x_px = coords.category_to_px(str(x_cat))
        if y_px is None and y_val is not None:
            y_px = coords.data_y_to_px(float(y_val))
        _draw_text_label(
            draw=draw,
            coords=coords,
            label=str(label),
            x_px=x_px,
            y_px=y_px,
            color=ann.get("color", "#e45756"),
            dx=ann.get("dx", 5),
            dy=ann.get("dy", -12),
        )

    elif ann_type == "band":
        y_lower = ann.get("y_lower")
        y_upper = ann.get("y_upper")
        if y_lower is None or y_upper is None:
            warnings.append("band: missing 'y_lower' or 'y_upper'")
            return warnings
        _draw_band(
            overlay=overlay,
            coords=coords,
            y_lower=float(y_lower),
            y_upper=float(y_upper),
            color=ann.get("color", "#4c78a8"),
            opacity=ann.get("opacity", 0.15),
        )

    elif ann_type == "highlight_bar":
        targets = ann.get("categories") or []
        if not targets:
            warnings.append("highlight_bar: 'categories' list is empty")
            return warnings
        _draw_highlight_bars(
            overlay=overlay,
            coords=coords,
            highlight_categories=[str(c) for c in targets],
            all_categories=coords.x_categories,
            highlight_color=ann.get("highlight_color", "#e45756"),
            dim_color=ann.get("dim_color", "#d3d3d3"),
            dim_alpha=int(ann.get("dim_opacity", 0.55) * 255),
        )

    elif ann_type == "circle":
        _draw_circle_emphasis(
            draw=draw,
            coords=coords,
            x_category=ann.get("x_category"),
            y_value=ann.get("y_value"),
            radius=int(ann.get("radius", 14)),
            color=ann.get("color", "#e45756"),
            line_width=ann.get("line_width", 2),
        )

    else:
        warnings.append(f"Unknown annotation type: {ann_type!r}")

    return warnings


# ── Main entry point ───────────────────────────────────────────────────────────

def annotate_chart_steps(
    *,
    image_base64: str,
    chart_area: Dict[str, Any],
    steps: List[Dict[str, Any]],
    return_each_step: bool = True,
) -> Dict[str, Any]:
    """Apply step-wise annotations to a chart image using PIL.

    Args:
        image_base64: Base64-encoded PNG of the base chart.
        chart_area: Dict with plot area bounds and axis info:
            x, y, width, height  — pixel coordinates of the plot area
            y_min, y_max         — data range of the y-axis
            x_categories         — ordered list of x-axis category labels
        steps: List of annotation step dicts, each with:
            sentence  (str)
            annotations: list of annotation item dicts (see _apply_annotation)
        return_each_step: If True, return an image per step. If False, return only final.

    Returns:
        {
          "steps": [{"sentenceIndex": int, "sentence": str, "image_base64": str}],
          "warnings": [str]
        }
    """
    # Decode base image
    try:
        raw = base64.b64decode(image_base64)
        base_img = Image.open(io.BytesIO(raw)).convert("RGBA")
    except Exception as exc:
        return {"steps": [], "warnings": [f"Failed to decode image_base64: {exc}"]}

    # Build coordinate helper
    ca = chart_area
    coords = ChartCoords(
        chart_x=int(ca.get("x", 0)),
        chart_y=int(ca.get("y", 0)),
        chart_width=int(ca.get("width", base_img.width)),
        chart_height=int(ca.get("height", base_img.height)),
        y_min=float(ca.get("y_min", 0)),
        y_max=float(ca.get("y_max", 100)),
        x_categories=[str(c) for c in (ca.get("x_categories") or [])],
    )

    all_warnings: List[str] = []
    result_steps: List[Dict[str, Any]] = []

    # Cumulative: each step builds on the previous annotated image
    current_img = base_img.copy()

    for step_idx, step in enumerate(steps, start=1):
        sentence = step.get("sentence", "")
        annotations = step.get("annotations") or []

        # Create a fresh RGBA overlay for transparent operations (band, highlight)
        overlay = Image.new("RGBA", current_img.size, (0, 0, 0, 0))
        # Draw on the composite (solid elements go on the combined image)
        combined = current_img.copy()
        draw = ImageDraw.Draw(combined)

        for ann in annotations:
            step_warnings = _apply_annotation(
                base_img=current_img,
                overlay=overlay,
                draw=draw,
                coords=coords,
                ann=ann,
            )
            all_warnings.extend(step_warnings)

        # Merge overlay (transparent bands/highlights) into combined
        combined_rgba = combined.convert("RGBA")
        merged = Image.alpha_composite(combined_rgba, overlay)

        # Update cumulative image for the next step
        current_img = merged

        if return_each_step or step_idx == len(steps):
            # Encode to base64 PNG
            buf = io.BytesIO()
            merged.convert("RGB").save(buf, format="PNG")
            encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
            result_steps.append({
                "sentenceIndex": step_idx,
                "sentence": sentence,
                "image_base64": encoded,
            })

        logger.debug(
            "[chart_annotator] step %d/%d | sentence=%r | annotations=%d",
            step_idx, len(steps), sentence[:60], len(annotations),
        )

    return {
        "steps": result_steps,
        "warnings": all_warnings,
    }
