"""
ShieldLab Logo Intro
=====================
A minimal, precise, construction-style logo animation for the ShieldLab
Manim project intro. Built entirely from primitive vector shapes
(VMobject / Polygon / Circle) -- no SVG or raster assets are imported.

Render:
    manim -pqh shieldlab_intro.py ShieldLabIntro
"""

import math
import numpy as np
from manim import *
from manim.utils.rate_functions import ease_in_out_sine

# --------------------------------------------------------------------------
# CONSTANTS -- colors, sizing, timing
# --------------------------------------------------------------------------

# Brand colors (sampled from reference artwork)
ORANGE_LIGHT = "#F08A2E"
ORANGE_DARK = "#9C3A14"

BLUE_LIGHT = "#3E84B5"
BLUE_DARK = "#0E2C45"

SPINE_WHITE = "#FBFAF7"
SPINE_EDGE_ORANGE = "#F0A93E"
SPINE_EDGE_BLUE = "#BFE0EE"
DOT_CREAM = "#E8D5A8"
DOT_EDGE = "#C9AD72"

TEXT_CREAM = "#E7DCC4"
TEXT_ORANGE = "#D14A1F"

BG_BLACK = "#000000"

# Geometry sizing (logo "design units" before any group scaling).
# Ratios below were measured directly from the reference artwork:
#   half-width : half-height  ~= 0.67
#   spine half-width at center : shield half-width ~= 0.24
#   spine narrows to a hairline at the top/bottom tips
SHIELD_HALF_WIDTH = 1.40      # widest horizontal extent of one half
SHIELD_HEIGHT = 4.2           # full vertical span, tip to tip
SPINE_WIDTH_TOP = 0.05        # spine gap width near the top/bottom tips
SPINE_WIDTH_MID = 0.68        # spine gap width at the vertical center

# Timing (seconds) -- tuned to match the requested sequence durations
T_LEFT_DRAW = 0.8
T_RIGHT_DRAW = 0.8
T_OVERLAP_LR = 0.35           # right half starts before left half finishes
T_SPINE_DRAW = 0.5
T_SPINE_OVERLAP = 0.25
T_DOTS_LAG = 0.1
T_DOT_ANIM = 0.3

T_BREATH_HOLD = 0.4
T_BREATH = 0.9

T_TEXT_WRITE = 1.0
T_HOLD = 1.0

T_SHRINK = 1.1


# --------------------------------------------------------------------------
# GEOMETRY HELPERS
# --------------------------------------------------------------------------

def _vesica_half_points(side: int, n: int = 80):
    """
    Returns the outer-edge sample points for one half (left=-1, right=+1)
    of a vertically oriented vesica (pointed-leaf) shape, traced from the
    top tip down to the bottom tip along the OUTER curve only.

    Rather than a true circular vesica piscis (which bulges into an
    egg-like profile when the half-width is large relative to height),
    this uses a power-law profile x(y) = w * (1 - |y/half_h|^p)^q.
    Tuning p/q gives the sharp, deliberate tip points and gently
    rounded shoulders seen in the reference artwork while staying
    perfectly smooth (C1) everywhere except the two tips, which is
    exactly where the reference logo also has its only corners.
    """
    half_h = SHIELD_HEIGHT / 2
    w = SHIELD_HALF_WIDTH
    p = 1.35   # controls how quickly the curve departs from the tip
    q = 0.62   # controls how full/rounded the shoulder bulge is

    pts = []
    for i in range(n + 1):
        t = i / n
        y = half_h - t * SHIELD_HEIGHT  # top tip -> bottom tip
        u = abs(y) / half_h             # 0 at center, 1 at tips
        x_mag = w * (1.0 - u**p) ** q
        x_mag = max(x_mag, 0.0)
        x = side * x_mag
        pts.append(np.array([x, y, 0.0]))
    return pts


def _spine_edge_points(side: int, n: int = 80):
    """
    Returns sample points for the inner spine edge on the given side
    (left=-1, right=+1). The spine stays a near-hairline for most of
    its length and only bulges outward in the middle third, matching
    the reference artwork's organic "stem" shape. A higher exponent
    than the outer shield curve keeps it narrow longer before the
    bulge, then widens quickly near the center.
    """
    half_h = SHIELD_HEIGHT / 2
    p = 2.6  # higher power = stays thin longer, bulges late near center
    pts = []
    for i in range(n + 1):
        t = i / n
        y = half_h - t * SHIELD_HEIGHT
        u = abs(y) / half_h  # 0 at center, 1 at tips
        width = SPINE_WIDTH_TOP + (SPINE_WIDTH_MID - SPINE_WIDTH_TOP) * (
            1.0 - u**p
        )
        x = side * (width / 2)
        pts.append(np.array([x, y, 0.0]))
    return pts


def _half_outline_points(side: int, n: int = 80):
    """
    Full closed outline (as a list of points, NOT yet split top/bottom)
    for one shield half: outer vesica edge down one side, inner spine
    edge back up the other side.
    """
    outer = _vesica_half_points(side=side, n=n)
    inner = list(reversed(_spine_edge_points(side=side, n=n)))
    return outer + inner


def _split_polygon_at_y(points, y_cut=0.0):
    """
    Given a closed outline (list of (x, y, 0) points), splits it into a
    "top" and "bottom" closed polygon at the horizontal line y = y_cut,
    by linearly interpolating new points wherever consecutive samples
    cross that line.

    This lets a single smooth silhouette be rendered as two flat-filled
    pieces (light top / dark bottom) that meet with a perfectly crisp,
    straight seam -- the "glossy badge" look of the reference artwork --
    while still tracing the exact same outer/inner curve.
    """
    top_pts, bottom_pts = [], []
    n = len(points)
    for i in range(n):
        p0 = points[i]
        p1 = points[(i + 1) % n]
        side0 = "top" if p0[1] >= y_cut else "bottom"
        (top_pts if side0 == "top" else bottom_pts).append(p0)

        y0, y1 = p0[1], p1[1]
        crosses = (y0 - y_cut) * (y1 - y_cut) < 0
        if crosses:
            t = (y_cut - y0) / (y1 - y0)
            cross_pt = p0 + t * (p1 - p0)
            top_pts.append(cross_pt)
            bottom_pts.append(cross_pt)
    return top_pts, bottom_pts


def _make_flat_piece(points, fill_color, stroke_color, stroke_width=2.5):
    piece = VMobject()
    piece.set_points_as_corners(list(points) + [points[0]])
    piece.set_stroke(color=stroke_color, width=stroke_width)
    piece.set_fill(color=fill_color, opacity=1)
    return piece


# --------------------------------------------------------------------------
# SCENE
# --------------------------------------------------------------------------

class ShieldLabIntro(Scene):
    """Constructs and reveals the ShieldLab logo, then docks it top-left."""

    def construct(self):
        self.camera.background_color = BG_BLACK

        # ---- Build all logo pieces (not yet added to the scene) ----
        left_half = self._build_left_half()
        right_half = self._build_right_half()
        spine = self._build_spine()
        dots = self._build_dots()
        wordmark = self._build_wordmark()

        logo_shield = VGroup(left_half, right_half, spine, dots)
        logo_full = VGroup(logo_shield, wordmark)

        # Wordmark sits centered beneath the shield with breathing room.
        wordmark.next_to(logo_shield, DOWN, buff=0.55)

        # Recenter the whole lockup in frame.
        logo_full.move_to(ORIGIN)

        # ---- 1. Shield construction ----
        self._animate_construction(left_half, right_half, spine, dots)

        # ---- 2. Micro pause / breathing ----
        # Hold briefly, then an almost imperceptible scale breathe:
        # 1.00 -> 1.015 -> 1.00, smooth the whole way, no overshoot.
        self.wait(T_BREATH_HOLD)
        self.play(
            logo_shield.animate.scale(1.015),
            run_time=T_BREATH,
            rate_func=there_and_back_with_pause,
        )

        # ---- 3. ShieldLab text ----
        self.play(Write(wordmark, run_time=T_TEXT_WRITE, rate_func=smooth))

        # ---- 4. Hold ----
        self.wait(T_HOLD)

        # ---- 5. Transition into lesson: shrink + dock top-left ----
        self._dock_top_left(logo_full)

        self.wait(0.3)

    # ------------------------------------------------------------------
    # CONSTRUCTION HELPERS
    # ------------------------------------------------------------------

    def _build_left_half(self) -> VGroup:
        """
        Left orange shield half, built as two flat-filled pieces (light
        top, dark bottom) that share a crisp horizontal seam at the
        vertical center -- matching the "glossy badge" look of the
        reference artwork far better than a smooth gradient would.
        """
        outline = _half_outline_points(side=-1)
        top_pts, bottom_pts = _split_polygon_at_y(outline, y_cut=0.0)
        top_piece = _make_flat_piece(top_pts, ORANGE_LIGHT, SPINE_EDGE_ORANGE)
        bottom_piece = _make_flat_piece(bottom_pts, ORANGE_DARK, SPINE_EDGE_ORANGE)
        return VGroup(top_piece, bottom_piece)

    def _build_right_half(self) -> VGroup:
        """Right blue shield half, same construction as the left half."""
        outline = _half_outline_points(side=1)
        top_pts, bottom_pts = _split_polygon_at_y(outline, y_cut=0.0)
        top_piece = _make_flat_piece(top_pts, BLUE_LIGHT, SPINE_EDGE_BLUE)
        bottom_piece = _make_flat_piece(bottom_pts, BLUE_DARK, SPINE_EDGE_BLUE)
        return VGroup(top_piece, bottom_piece)

    def _build_spine(self) -> VMobject:
        """
        The thin off-white spine channel running down the center.
        Drawn as a single closed band (left edge down, right edge up)
        so Create() reveals it as one continuous top-to-bottom stroke.
        """
        left_edge = _spine_edge_points(side=-1)
        right_edge = list(reversed(_spine_edge_points(side=1)))
        points = left_edge + right_edge

        spine = VMobject()
        spine.set_points_as_corners(points)
        spine.close_path()
        spine.set_stroke(color=SPINE_EDGE_BLUE, width=1.5)
        spine.set_fill(color=SPINE_WHITE, opacity=1)
        return spine

    def _build_dots(self) -> VGroup:
        """
        Three small circles centered within the spine channel. A thin
        warm-toned stroke keeps them legible against the near-white
        spine fill instead of visually melting into it.
        """
        half_h = SHIELD_HEIGHT / 2
        ys = [half_h * 0.155, 0.0, -half_h * 0.155]
        radius = 0.155
        dots = VGroup(
            *[
                Circle(
                    radius=radius,
                    color=DOT_EDGE,
                    fill_color=DOT_CREAM,
                    fill_opacity=1,
                    stroke_width=1.5,
                ).move_to([0, y, 0])
                for y in ys
            ]
        )
        return dots

    def _build_wordmark(self) -> VGroup:
        """'Shield' in off-white + 'Lab' in orange, as one text mobject pair."""
        shield_txt = Text(
            "Shield",
            font="DejaVu Sans",
            weight=NORMAL,
            color=TEXT_CREAM,
        )
        lab_txt = Text(
            "Lab",
            font="DejaVu Sans",
            weight=BOLD,
            color=TEXT_ORANGE,
        )
        lab_txt.next_to(shield_txt, RIGHT, buff=0.06)
        # Align baselines (Text() aligns by bounding box center by default,
        # which is close enough at matching font size; nudge for parity).
        lab_txt.align_to(shield_txt, DOWN)

        wordmark = VGroup(shield_txt, lab_txt)
        wordmark.scale(1.15)
        return wordmark

    # ------------------------------------------------------------------
    # ANIMATION HELPERS
    # ------------------------------------------------------------------

    def _animate_construction(self, left_half, right_half, spine, dots):
        """
        Sequence 1: the shield is built, not faded in.

        Left half draws -> right half starts while the left half is
        still finishing (true overlap via AnimationGroup lag_ratio,
        not just back-to-back plays) -> spine draws, overlapping the
        tail of the halves -> three dots appear in a gentle LaggedStart.
        Total duration ~1.8-2.2s, smooth easing throughout, no bounce.
        """
        # Left half draws fully; right half begins before it finishes.
        # lag_ratio < 1 means anim_right starts at lag_ratio * T_LEFT_DRAW.
        lag_lr = (T_LEFT_DRAW - T_OVERLAP_LR) / T_LEFT_DRAW
        halves_group = AnimationGroup(
            DrawBorderThenFill(left_half, run_time=T_LEFT_DRAW, rate_func=smooth),
            DrawBorderThenFill(right_half, run_time=T_RIGHT_DRAW, rate_func=smooth),
            lag_ratio=lag_lr,
        )

        # Spine begins while the halves are still settling into place.
        lag_spine = (T_LEFT_DRAW + T_OVERLAP_LR - T_SPINE_OVERLAP) / (
            T_LEFT_DRAW + T_OVERLAP_LR
        )
        full_shield_group = AnimationGroup(
            halves_group,
            Create(spine, run_time=T_SPINE_DRAW, rate_func=smooth),
            lag_ratio=max(lag_spine, 0.0),
        )

        self.play(full_shield_group)

        # Three dots settle in one after another, calm and deliberate.
        self.play(
            LaggedStart(
                *[GrowFromCenter(dot) for dot in dots],
                lag_ratio=T_DOTS_LAG / T_DOT_ANIM,
                run_time=T_DOT_ANIM * 1.8,
                rate_func=smooth,
            )
        )

    def _dock_top_left(self, logo_full: VGroup):
        """
        Sequence 5: shrink the full lockup to ~32% and ease it toward the
        upper-left corner, where it remains as persistent branding for
        the lesson content that follows.
        """
        target_scale = 0.32
        target_corner = UP * 3.1 + LEFT * 5.7  # safely inside frame edges

        self.play(
            logo_full.animate.scale(target_scale).move_to(target_corner),
            run_time=T_SHRINK,
            rate_func=ease_in_out_sine,
        )