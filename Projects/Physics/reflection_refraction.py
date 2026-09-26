"""
REFLECTION & REFRACTION — a 3Blue1Brown-style Manim explainer
================================================================
Built for Manim Community Edition (pip install manim).

HOW TO RENDER
-------------
Render one scene at a time (each is a full "chapter"):

    manim -pqh reflection_refraction.py Scene00_Title
    manim -pqh reflection_refraction.py Scene01_WhyLightBends
    manim -pqh reflection_refraction.py Scene02_LawsOfReflection
    manim -pqh reflection_refraction.py Scene03_AngleOfInclination
    manim -pqh reflection_refraction.py Scene04_MultipleImages
    manim -pqh reflection_refraction.py Scene05_RefractionIntro
    manim -pqh reflection_refraction.py Scene06_RefractiveIndex
    manim -pqh reflection_refraction.py Scene07_SnellsLaw
    manim -pqh reflection_refraction.py Scene08_CriticalAngleTIR
    manim -pqh reflection_refraction.py Scene09_MirrorEquation
    manim -pqh reflection_refraction.py Scene10_ThinLensEquation
    manim -pqh reflection_refraction.py Scene11_ImageCharacteristics
    manim -pqh reflection_refraction.py Scene12_Outro

Or render the whole film in order with the tiny helper at the
bottom of this file:  python render_all.py  (see comment there).

    -p   preview when done       -q  quality (l/m/h/k)

STYLE NOTES
-----------
- Dark background, thin glowing rays, dashed construction lines,
  color-coded angles (incidence = YELLOW, reflection/refraction = ORANGE),
  captions live in a strip at the bottom so diagrams keep the top 2/3.
- Every derivation is built term-by-term with TransformMatchingTex so
  equations visibly grow rather than jump-cutting.
- ValueTrackers + always_redraw are used everywhere a picture should
  react live to a changing angle/position (the "interactive proof" feel).
"""

from manim import *
import numpy as np

# ----------------------------------------------------------------------
#  PALETTE
# ----------------------------------------------------------------------
BG        = "#0e1116"
INK       = "#ececec"
DIM       = "#8a8f98"
RAY_IN    = "#FFD966"   # incident ray
RAY_OUT   = "#FF9F1C"   # reflected / refracted ray
RAY_ALT   = "#58C4DD"   # secondary ray / normal-adjacent
NORMAL_C  = "#8a8f98"
MIRROR_C  = "#d8d8d8"
GLASS_C   = "#58C4DD"
WATER_C   = "#3A8FB7"
ANGLE_IN  = "#FFD966"
ANGLE_OUT = "#FC6255"
GOOD      = "#83C167"
HILITE    = "#B48EAD"

config.background_color = BG


# ----------------------------------------------------------------------
#  SMALL VISUAL HELPERS  (reused across every scene)
# ----------------------------------------------------------------------

def caption(text, scale=0.62, color=INK):
    """Bottom-strip narration caption, 3b1b style."""
    cap = Text(text, font="sans-serif", color=color).scale(scale)
    cap.to_edge(DOWN, buff=0.35)
    return cap


def swap_caption(scene, old_caption, new_text, run_time=0.8, **kwargs):
    """Cross-fade the bottom caption to new text; returns the new mobject."""
    new_caption = caption(new_text, **kwargs)
    scene.play(FadeOut(old_caption, shift=UP * 0.15),
               FadeIn(new_caption, shift=UP * 0.15), run_time=run_time)
    return new_caption


def unit(v):
    n = np.linalg.norm(v)
    return v / n if n > 1e-9 else v


def make_ray(start, end, color=RAY_IN, width=5, tip_length=0.16):
    """An arrowed light ray."""
    ln = Line(start, end, color=color, stroke_width=width)
    ln.add_tip(tip_length=tip_length)
    return ln


def mirror_hatch(p1, p2, n_hatch=None, color=DIM, back_side=None):
    """A silvered mirror: solid front line + hatch marks on the back."""
    p1, p2 = np.array(p1), np.array(p2)
    d = unit(p2 - p1)
    normal = np.array([-d[1], d[0], 0.0])
    if back_side is not None and np.dot(normal, back_side) > 0:
        normal = -normal
    length = np.linalg.norm(p2 - p1)
    if n_hatch is None:
        n_hatch = max(int(length / 0.22), 4)
    face = Line(p1, p2, stroke_width=8, color=MIRROR_C)
    hatches = VGroup()
    for i in range(n_hatch + 1):
        base = p1 + d * (i * length / n_hatch)
        hatches.add(Line(base, base - normal * 0.22 - d * 0.09,
                          stroke_width=2, color=color))
    return VGroup(hatches, face)


def dashed_normal(point, direction, half_len=1.6, color=NORMAL_C):
    d = unit(direction)
    return DashedLine(point - d * half_len, point + d * half_len,
                       color=color, stroke_width=2, dash_length=0.1)


def angle_arc(vertex, arm1_point, arm2_point, radius=0.55, color=WHITE,
              label=None, label_buff=0.34, label_scale=0.65, other_angle=False):
    """Angle arc at `vertex` spanned by rays toward arm1_point / arm2_point."""
    a = Angle(Line(vertex, arm1_point), Line(vertex, arm2_point),
              radius=radius, color=color, other_angle=other_angle)
    grp = VGroup(a)
    if label is not None:
        tex = MathTex(label, color=color).scale(label_scale)
        mid = a.point_from_proportion(0.5)
        dirn = unit(mid - vertex)
        tex.move_to(vertex + dirn * (radius + label_buff))
        grp.add(tex)
    return grp


def title_card(main, sub=None, main_scale=1.15, sub_scale=0.55):
    grp = VGroup()
    t = Text(main, weight=BOLD, color=INK).scale(main_scale)
    grp.add(t)
    if sub:
        s = Text(sub, color=DIM).scale(sub_scale)
        s.next_to(t, DOWN, buff=0.35)
        grp.add(s)
    return grp


def chapter_header(number, title, color=RAY_OUT):
    tag = Text(f"CHAPTER {number}", color=color, weight=BOLD).scale(0.42)
    head = Text(title, color=INK, weight=BOLD).scale(0.85)
    head.next_to(tag, DOWN, buff=0.18)
    grp = VGroup(tag, head).to_edge(UP, buff=0.6)
    return grp


# ----------------------------------------------------------------------
#  CHAPTER 0 — TITLE
# ----------------------------------------------------------------------
class Scene00_Title(Scene):
    def construct(self):
        self.camera.background_color = BG

        # A slab of "glass" with a ray bending through it, built purely
        # from primitives, sitting behind the title as a quiet hero shot.
        glass = Rectangle(width=5.5, height=2.4, color=GLASS_C,
                           fill_color=GLASS_C, fill_opacity=0.12,
                           stroke_width=2).shift(DOWN * 0.3)
        top, bot = glass.get_top(), glass.get_bottom()

        entry = np.array([-2.6, 1.9, 0])
        hit1 = np.array([-1.0, glass.get_top()[1], 0])
        hit2 = np.array([0.4, glass.get_bottom()[1], 0])
        exitp = np.array([2.6, -1.9, 0])

        r1 = make_ray(entry, hit1, color=RAY_IN, width=4)
        r2 = make_ray(hit1, hit2, color=RAY_OUT, width=4)
        r3 = make_ray(hit2, exitp, color=RAY_IN, width=4)

        bg_group = VGroup(glass, r1, r2, r3).set_opacity(0.55)

        title = title_card("Reflection & Refraction",
                            "how light bounces, bends, and builds images")
        title.move_to(ORIGIN)

        self.play(FadeIn(bg_group, run_time=1.6))
        self.play(Write(title[0]), run_time=1.8)
        if len(title) > 1:
            self.play(FadeIn(title[1], shift=UP * 0.2), run_time=0.9)
        self.wait(1.2)

        roadmap = VGroup(*[
            Text(t, color=DIM).scale(0.4) for t in [
                "laws of reflection  ·  images in tilted mirrors",
                "Snell's law  ·  refractive index  ·  critical angle",
                "mirror & lens equations  ·  image characteristics",
            ]
        ]).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(title, DOWN, buff=0.9)

        self.play(FadeIn(roadmap, shift=UP * 0.2), run_time=1.2)
        self.wait(2)
        self.play(FadeOut(VGroup(bg_group, title, roadmap)))


# ----------------------------------------------------------------------
#  CHAPTER 1 — WHY LIGHT BENDS AND BOUNCES (intuition, no equations yet)
# ----------------------------------------------------------------------
class Scene01_WhyLightBends(Scene):
    def construct(self):
        head = chapter_header(1, "Two Things Light Does at a Boundary")
        self.play(FadeIn(head, shift=DOWN * 0.2))

        cap = caption("Every surface you can see is bouncing light into your eye.")
        self.play(FadeIn(cap))

        # A flat mirror-like boundary in the middle of the screen.
        boundary = Line(LEFT * 5.5, RIGHT * 5.5, color=MIRROR_C, stroke_width=3)
        boundary.shift(UP * 0.2)
        self.play(Create(boundary))

        # Fan of rays bouncing off, like light scattering off a surface.
        source = np.array([-3.5, 2.6, 0])
        dot_src = Dot(source, color=RAY_IN)
        self.play(FadeIn(dot_src))

        hit = np.array([-0.6, 0.2, 0])
        r_in = make_ray(source, hit, color=RAY_IN)
        self.play(Create(r_in), run_time=0.8)

        outs = []
        for dx in [-1.6, -0.4, 0.9, 2.1]:
            end = hit + np.array([dx, 2.2, 0])
            outs.append(make_ray(hit, end, color=RAY_OUT, width=3))
        self.play(*[Create(o) for o in outs], run_time=1.0)
        cap = swap_caption(self, cap,
                            "REFLECTION: light bounces back into the same medium.")
        self.wait(1.2)

        self.play(FadeOut(VGroup(r_in, *outs, dot_src)))

        # Now show refraction intuition: a rod dipping into water, bent look.
        water = Rectangle(width=11, height=2.6, color=WATER_C,
                           fill_color=WATER_C, fill_opacity=0.25, stroke_width=0)
        water.next_to(boundary, DOWN, buff=0)
        cap = swap_caption(self, cap,
                            "REFRACTION: light crosses into a new medium and bends.")
        self.play(FadeIn(water))

        rod_top = np.array([-2.0, 2.6, 0])
        bend_pt = np.array([-1.2, 0.2, 0])
        rod_bottom_straight = bend_pt + unit(bend_pt - rod_top) * 2.6
        rod_bottom_bent = bend_pt + np.array([-1.0, -2.2, 0])

        rod_air = Line(rod_top, bend_pt, color="#c9a877", stroke_width=8)
        rod_ghost = DashedLine(bend_pt, rod_bottom_straight, color=DIM, stroke_width=3)
        rod_water = Line(bend_pt, rod_bottom_bent, color="#c9a877", stroke_width=8)

        self.play(Create(rod_air))
        self.play(Create(rod_ghost))
        ghost_label = Text("looks like it should go here...", color=DIM).scale(0.35)
        ghost_label.next_to(rod_bottom_straight, RIGHT, buff=0.2)
        self.play(FadeIn(ghost_label))
        self.wait(0.5)
        self.play(Create(rod_water),
                   Transform(ghost_label,
                              Text("...but the light bent, so it looks broken.",
                                   color=DIM).scale(0.35).next_to(rod_bottom_bent, RIGHT, buff=0.2)))
        self.wait(1.5)

        take_away = Text(
            "Both effects come from one idea: light changes direction whenever\n"
            "it meets a new surface or a new material — the question is just how much.",
            color=INK).scale(0.45)
        self.play(FadeOut(VGroup(boundary, water, rod_air, rod_ghost, rod_water, ghost_label, cap)))
        self.play(Write(take_away))
        self.wait(2)
        self.play(FadeOut(VGroup(head, take_away)))


# ----------------------------------------------------------------------
#  CHAPTER 2 — LAWS OF REFLECTION  (angle of incidence, normal, i = r)
# ----------------------------------------------------------------------
class Scene02_LawsOfReflection(Scene):
    def construct(self):
        head = chapter_header(2, "The Laws of Reflection")
        self.play(FadeIn(head, shift=DOWN * 0.2))
        cap = caption("Drop a normal at the point of contact — everything is measured from it.")
        self.play(FadeIn(cap))

        mirror = mirror_hatch(LEFT * 4, RIGHT * 4, back_side=DOWN)
        mirror.shift(DOWN * 1.0)
        self.play(Create(mirror))

        P = np.array([0, -1.0, 0])         # point of incidence
        normal = dashed_normal(P, UP, half_len=2.2)
        self.play(Create(normal))
        n_label = MathTex("\\text{normal}", color=NORMAL_C).scale(0.5)
        n_label.next_to(P + UP * 2.2, UP, buff=0.1)
        self.play(FadeIn(n_label))

        # Angle tracker driving both incident & reflected rays symmetrically.
        theta = ValueTracker(35 * DEGREES)

        def incident_start():
            a = theta.get_value()
            return P + np.array([-np.sin(a), np.cos(a), 0]) * 3.2

        def reflected_end():
            a = theta.get_value()
            return P + np.array([np.sin(a), np.cos(a), 0]) * 3.2

        incident = always_redraw(lambda: make_ray(incident_start(), P, color=RAY_IN))
        reflected = always_redraw(lambda: make_ray(P, reflected_end(), color=RAY_OUT))

        angle_i = always_redraw(lambda: angle_arc(
            P, incident_start(), P + UP * 2.2, radius=0.5,
            color=ANGLE_IN, label="i", other_angle=True))
        angle_r = always_redraw(lambda: angle_arc(
            P, P + UP * 2.2, reflected_end(), radius=0.75,
            color=ANGLE_OUT, label="r"))

        self.play(Create(incident), Create(reflected))
        self.play(FadeIn(angle_i), FadeIn(angle_r))
        self.wait(0.5)

        cap = swap_caption(self, cap,
                            "Law 1: incident ray, normal, and reflected ray share one plane.")
        self.wait(1.2)
        cap = swap_caption(self, cap,
                            "Law 2: the angle of incidence equals the angle of reflection.")

        law2 = MathTex("i", "=", "r", color=INK).scale(1.0)
        law2.to_corner(UR, buff=0.6).shift(DOWN * 0.3)
        law2[0].set_color(ANGLE_IN)
        law2[2].set_color(ANGLE_OUT)
        self.play(Write(law2))
        self.wait(0.5)

        # Sweep the angle to prove i = r stays true for every tilt.
        self.play(theta.animate.set_value(65 * DEGREES), run_time=2, rate_func=there_and_back)
        self.play(theta.animate.set_value(15 * DEGREES), run_time=2, rate_func=there_and_back)
        self.wait(0.5)

        cap = swap_caption(self, cap,
                            "This holds at any tilt — reflection never plays favorites.")
        self.wait(1.5)

        self.play(FadeOut(VGroup(head, cap, mirror, normal, n_label,
                                  incident, reflected, angle_i, angle_r, law2)))


# ----------------------------------------------------------------------
#  CHAPTER 3 — ANGLE OF INCLINATION BETWEEN TWO MIRRORS
# ----------------------------------------------------------------------
class Scene03_AngleOfInclination(Scene):
    def construct(self):
        head = chapter_header(3, "Tilting a Second Mirror Into the Picture")
        self.play(FadeIn(head, shift=DOWN * 0.2))
        cap = caption("Hinge two mirrors together at a point — the hinge angle is theta.")
        self.play(FadeIn(cap))

        hinge = np.array([-1.0, -0.6, 0])
        theta = ValueTracker(70 * DEGREES)

        m1_end = hinge + RIGHT * 4.2
        m1 = Line(hinge, m1_end, color=MIRROR_C, stroke_width=6)

        m2 = always_redraw(lambda: Line(
            hinge, hinge + np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]) * 4.2,
            color=MIRROR_C, stroke_width=6))

        arc = always_redraw(lambda: angle_arc(
            hinge, m1_end, hinge + np.array(
                [np.cos(theta.get_value()), np.sin(theta.get_value()), 0]) * 4.2,
            radius=0.9, color=HILITE, label="\\theta"))

        self.play(Create(m1))
        self.play(Create(m2))
        self.play(FadeIn(arc))
        self.wait(0.5)

        cap = swap_caption(self, cap,
                            "theta is the angle of inclination — the wedge the mirrors open into.")
        self.wait(1)

        self.play(theta.animate.set_value(40 * DEGREES), run_time=2)
        self.wait(0.3)
        self.play(theta.animate.set_value(120 * DEGREES), run_time=2)
        self.wait(0.3)
        self.play(theta.animate.set_value(90 * DEGREES), run_time=1.5)

        note = Text("Small theta -> a narrow wedge, more room for light to keep\n"
                     "bouncing back and forth before it escapes.", color=DIM).scale(0.42)
        note.to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
        self.play(FadeIn(note, shift=LEFT * 0.2))
        self.wait(2)

        cap = swap_caption(self, cap,
                            "Next: an object placed in this wedge forms more than one image.")
        self.wait(1.5)
        self.play(FadeOut(VGroup(head, cap, m1, m2, arc, note)))


# ----------------------------------------------------------------------
#  CHAPTER 4 — HOW MANY IMAGES DO TWO INCLINED MIRRORS MAKE?
# ----------------------------------------------------------------------
def reflect_point_across_line(P, A, direction):
    """Reflect point P across the infinite line through A with given direction."""
    d = unit(direction)
    AP = P - A
    proj = np.dot(AP, d) * d
    perp = AP - proj
    return P - 2 * perp


def kaleidoscope_images(hinge, theta, object_angle, radius, max_bounces=14):
    """Generate the chain of images of a point object between two mirrors
    that meet at `hinge` with angle `theta`, by alternately reflecting
    across mirror-1 (angle 0) and mirror-2 (angle theta)."""
    m1_dir = np.array([1.0, 0.0, 0.0])
    m2_dir = np.array([np.cos(theta), np.sin(theta), 0.0])

    obj = hinge + radius * np.array([np.cos(object_angle), np.sin(object_angle), 0.0])
    images = []
    current = obj
    use_m1 = True
    for _ in range(max_bounces):
        line_dir = m1_dir if use_m1 else m2_dir
        nxt = reflect_point_across_line(current, hinge, line_dir)
        if any(np.linalg.norm(nxt - im) < 1e-3 for im in images) or np.linalg.norm(nxt - obj) < 1e-3:
            break
        images.append(nxt)
        current = nxt
        use_m1 = not use_m1
    return obj, images


class Scene04_MultipleImages(Scene):
    def construct(self):
        head = chapter_header(4, "Images in Two Inclined Mirrors")
        self.play(FadeIn(head, shift=DOWN * 0.2))
        cap = caption("Put an object in the wedge between two mirrors set at angle theta.")
        self.play(FadeIn(cap))

        hinge = np.array([0.0, -0.4, 0.0])
        theta_deg = 60
        theta = theta_deg * DEGREES
        R = 3.4

        m1 = Line(hinge, hinge + np.array([np.cos(0), np.sin(0), 0]) * R,
                  color=MIRROR_C, stroke_width=6)
        m2 = Line(hinge, hinge + np.array([np.cos(theta), np.sin(theta), 0]) * R,
                  color=MIRROR_C, stroke_width=6)
        self.play(Create(m1), Create(m2))

        object_angle = theta / 2
        obj, images = kaleidoscope_images(hinge, theta, object_angle, radius=1.6)

        obj_dot = Dot(obj, color=RAY_IN, radius=0.09)
        obj_label = Text("object", color=RAY_IN).scale(0.35).next_to(obj_dot, UP, buff=0.15)
        self.play(FadeIn(obj_dot), FadeIn(obj_label))
        self.wait(0.3)

        cap = swap_caption(self, cap,
                            "Each mirror reflects the object AND reflects every other image.")

        image_dots = VGroup()
        image_labels = VGroup()
        for i, im in enumerate(images):
            d = Dot(im, color=RAY_OUT, radius=0.08)
            l = Text(f"I{i+1}", color=RAY_OUT).scale(0.32).next_to(d, UP, buff=0.12)
            image_dots.add(d)
            image_labels.add(l)
            self.play(FadeIn(d, scale=1.4), FadeIn(l), run_time=0.45)

        self.wait(0.5)
        cap = swap_caption(self, cap,
                            f"With theta = {theta_deg}\N{DEGREE SIGN}, that's {len(images)} images in total.")
        self.wait(1.2)

        formula = MathTex("n", "=", "\\dfrac{360^\\circ}{\\theta}", "-", "1").scale(0.95)
        formula.to_corner(UR, buff=0.5)
        formula[0].set_color(RAY_OUT)
        self.play(Write(formula))
        self.wait(0.3)

        check = MathTex(f"= \\dfrac{{360}}{{{theta_deg}}} - 1 = {len(images)}").scale(0.8)
        check.next_to(formula, DOWN, buff=0.25).align_to(formula, RIGHT)
        self.play(Write(check))
        self.wait(1.5)

        cap = swap_caption(self, cap,
                            "This exact formula only works when 360/theta is a whole number.")
        self.wait(1.2)

        # Quick montage: shrink theta -> more images; widen theta -> fewer.
        self.play(FadeOut(VGroup(obj_dot, obj_label, image_dots, image_labels, check)))

        for new_deg in [90, 45, 36]:
            new_theta = new_deg * DEGREES
            new_m2_end = hinge + np.array([np.cos(new_theta), np.sin(new_theta), 0]) * R
            obj2, images2 = kaleidoscope_images(hinge, new_theta, new_theta / 2, radius=1.6)
            new_obj_dot = Dot(obj2, color=RAY_IN, radius=0.09)
            new_images = VGroup(*[Dot(p, color=RAY_OUT, radius=0.08) for p in images2])
            new_formula_check = MathTex(
                f"\\theta={new_deg}^\\circ \\Rightarrow n = \\dfrac{{360}}{{{new_deg}}}-1 = {len(images2)}"
            ).scale(0.7).next_to(formula, DOWN, buff=0.3)

            self.play(
                Transform(m2, Line(hinge, new_m2_end, color=MIRROR_C, stroke_width=6)),
                FadeIn(new_obj_dot), FadeIn(new_images), FadeIn(new_formula_check),
                run_time=1.3,
            )
            self.wait(1.0)
            self.play(FadeOut(VGroup(new_obj_dot, new_images, new_formula_check)))

        cap = swap_caption(self, cap,
                            "Two parallel mirrors are the limit: theta -> 0, images -> infinite.")
        self.wait(1.8)

        self.play(FadeOut(VGroup(head, cap, m1, m2, formula)))


# ----------------------------------------------------------------------
#  CHAPTER 5 — REFRACTION: LIGHT CROSSING A BOUNDARY
# ----------------------------------------------------------------------
class Scene05_RefractionIntro(Scene):
    def construct(self):
        head = chapter_header(5, "Refraction: Bending at a Boundary", color=GLASS_C)
        self.play(FadeIn(head, shift=DOWN * 0.2))
        cap = caption("Same idea as before: draw the normal where the ray meets the surface.")
        self.play(FadeIn(cap))

        boundary_y = -0.4
        boundary = Line(LEFT * 5.5, RIGHT * 5.5, color=WHITE, stroke_width=2).shift(UP * boundary_y)
        air_label = Text("air  (less dense)", color=DIM).scale(0.4).to_corner(UL, buff=0.7).shift(DOWN*0.3)
        water = Rectangle(width=11, height=3.2, color=WATER_C, fill_color=WATER_C,
                           fill_opacity=0.22, stroke_width=0).next_to(boundary, DOWN, buff=0)
        water_label = Text("water  (denser)", color=DIM).scale(0.4)
        water_label.next_to(water.get_corner(UL), DOWN, buff=0.25).shift(RIGHT*0.3)

        self.play(FadeIn(water), Create(boundary), FadeIn(air_label), FadeIn(water_label))

        P = np.array([0, boundary_y, 0])
        normal = dashed_normal(P, UP, half_len=2.6)
        self.play(Create(normal))

        theta_i = ValueTracker(40 * DEGREES)
        theta_t = ValueTracker(27 * DEGREES)   # will be tied to Snell's law later

        def in_start():
            a = theta_i.get_value()
            return P + np.array([-np.sin(a), np.cos(a), 0]) * 3.0

        def out_end():
            a = theta_t.get_value()
            return P + np.array([np.sin(a), -np.cos(a), 0]) * 3.0

        r_in = always_redraw(lambda: make_ray(in_start(), P, color=RAY_IN))
        r_out = always_redraw(lambda: make_ray(P, out_end(), color=RAY_OUT))
        self.play(Create(r_in))
        self.wait(0.2)
        self.play(Create(r_out))

        ang_i = always_redraw(lambda: angle_arc(P, in_start(), P + UP * 2.6,
                                                 radius=0.55, color=ANGLE_IN,
                                                 label="\\theta_1", other_angle=True))
        ang_t = always_redraw(lambda: angle_arc(P, P + DOWN * 2.6, out_end(),
                                                 radius=0.7, color=ANGLE_OUT,
                                                 label="\\theta_2", other_angle=True))
        self.play(FadeIn(ang_i), FadeIn(ang_t))
        self.wait(0.5)

        cap = swap_caption(self, cap,
                            "Going into a denser medium, the ray bends TOWARD the normal.")
        self.wait(1.3)

        cap = swap_caption(self, cap,
                            "Leaving into a lighter medium, it would bend AWAY from the normal.")
        self.play(theta_i.animate.set_value(25 * DEGREES),
                   theta_t.animate.set_value(38 * DEGREES), run_time=1.6)
        self.wait(1)
        self.play(theta_i.animate.set_value(40 * DEGREES),
                   theta_t.animate.set_value(27 * DEGREES), run_time=1.2)

        cap = swap_caption(self, cap,
                            "How much it bends depends on a number attached to each material.")
        self.wait(1.5)

        self.play(FadeOut(VGroup(head, cap, water, boundary, air_label, water_label,
                                  normal, r_in, r_out, ang_i, ang_t)))


# ----------------------------------------------------------------------
#  CHAPTER 6 — REFRACTIVE INDEX
# ----------------------------------------------------------------------
class Scene06_RefractiveIndex(Scene):
    def construct(self):
        head = chapter_header(6, "The Refractive Index", color=GLASS_C)
        self.play(FadeIn(head, shift=DOWN * 0.2))
        cap = caption("Light always travels slower inside a material than in vacuum.")
        self.play(FadeIn(cap))

        c_line = MathTex("c", "=", "3.0\\times10^{8}\\ \\text{m/s}", "\\quad\\text{(vacuum, top speed)}")
        c_line.scale(0.8).shift(UP * 1.6)
        self.play(Write(c_line))
        self.wait(0.8)

        n_def = MathTex("n", "=", "\\dfrac{c}{v}").scale(1.2)
        n_def.next_to(c_line, DOWN, buff=0.7)
        n_def[0].set_color(GLASS_C)
        self.play(Write(n_def))
        cap = swap_caption(self, cap,
                            "n is how many times SLOWER light travels in that medium.")
        self.wait(1.3)

        table_data = [
            ("vacuum / air", "1.00"),
            ("water", "1.33"),
            ("crown glass", "1.52"),
            ("diamond", "2.42"),
        ]
        rows = VGroup()
        for name, val in table_data:
            row = VGroup(
                Text(name, color=INK).scale(0.45),
                MathTex(f"n = {val}", color=GLASS_C).scale(0.5),
            ).arrange(RIGHT, buff=0.6)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        rows.next_to(n_def, DOWN, buff=0.8).align_to(n_def, LEFT).shift(LEFT*0.6)

        self.play(FadeIn(rows, shift=UP * 0.2), run_time=1.2)
        self.wait(1.5)

        cap = swap_caption(self, cap,
                            "Higher n -> light slows more there -> it bends more crossing in.")
        self.wait(1.2)

        rel = MathTex("_1n_2", "=", "\\dfrac{v_1}{v_2}", "=", "\\dfrac{n_2}{n_1}").scale(0.85)
        rel.next_to(rows, DOWN, buff=0.6)
        self.play(Write(rel))
        cap = swap_caption(self, cap,
                            "That ratio, medium 1 relative to medium 2, is what Snell's law uses.")
        self.wait(1.8)

        self.play(FadeOut(VGroup(head, cap, c_line, n_def, rows, rel)))


# ----------------------------------------------------------------------
#  CHAPTER 7 — SNELL'S LAW, DERIVED FROM HUYGENS' WAVEFRONTS
# ----------------------------------------------------------------------
class Scene07_SnellsLaw(Scene):
    def construct(self):
        head = chapter_header(7, "Deriving Snell's Law", color=GLASS_C)
        self.play(FadeIn(head, shift=DOWN * 0.2))
        cap = caption("Picture light as a wavefront, not a single ray — a marching straight line.")
        self.play(FadeIn(cap))

        boundary_y = -0.2
        boundary = Line(LEFT * 5.5, RIGHT * 5.5, color=WHITE, stroke_width=2).shift(UP * boundary_y)
        water = Rectangle(width=11, height=3.4, color=WATER_C, fill_color=WATER_C,
                           fill_opacity=0.2, stroke_width=0).next_to(boundary, DOWN, buff=0)
        self.play(FadeIn(water), Create(boundary))

        theta1 = 40 * DEGREES
        theta2 = 27 * DEGREES

        # Two parallel rays of the same wavefront, hitting the boundary
        # at two different points A (first) and B (arrives later).
        A = np.array([-0.9, boundary_y, 0])
        B = np.array([1.1, boundary_y, 0])

        rayA_dir = np.array([-np.sin(theta1), np.cos(theta1), 0])
        rayB_dir = np.array([-np.sin(theta1), np.cos(theta1), 0])
        A_start = A - rayA_dir * 2.6
        B_start = B - rayB_dir * 2.6 - np.array([0, 0.9, 0])  # B is behind, wavefront tilted

        # Build a genuine common wavefront: a line perpendicular to the ray
        # direction, passing through both starting points at t=0.
        wave_dir = np.array([rayA_dir[1], -rayA_dir[0], 0])  # perpendicular to ray
        # Place B_start so that A_start and B_start lie on one perpendicular line
        B_start = A_start + wave_dir * 2.0

        rA = make_ray(A_start, A, color=RAY_IN, width=3.5)
        rB = make_ray(B_start, B, color=RAY_IN, width=3.5)
        wavefront_0 = DashedLine(A_start, B_start, color=DIM, stroke_width=2)

        self.play(Create(wavefront_0))
        self.play(Create(rA), Create(rB))
        cap = swap_caption(self, cap,
                            "Ray A reaches the boundary first; ray B is still travelling in air.")
        self.wait(1)

        dotA = Dot(A, color=RAY_IN, radius=0.06)
        self.play(FadeIn(dotA))

        # While A refracts and travels through water at v2 for time T,
        # B (still in air) covers AB*sin(theta1) at speed v1 in the same time.
        # Geometrically: BB' = AB*sin(theta1) (distance B still has to go to reach boundary along its direction)
        AB = np.linalg.norm(B - A)
        BB_prime_len = AB * np.sin(theta1)
        # A_prime: where the refracted wavelet from A has reached in water,
        # travelling at angle theta2 from the normal, distance = AB*sin(theta2)*k
        AAprime_len = AB * np.sin(theta2)

        # Show the two little "wavelet" distances as the key triangle legs.
        B_travel_dir = rayB_dir
        B_prime = B  # B reaches boundary at time T
        A_prime = A + np.array([np.sin(theta2), -np.cos(theta2), 0]) * AAprime_len

        brace_air = BraceBetweenPoints(B_start + (B - B_start) * 0.0, B, color=RAY_IN)
        self.play(Create(rayB_dir_line := Line(B_start, B, color=RAY_IN, stroke_width=3.5)))
        self.wait(0.2)

        seg_air = Line(A, B, color=DIM, stroke_width=1.5)
        self.play(Create(seg_air))
        ab_label = MathTex("AB", color=DIM).scale(0.5).next_to(seg_air, UP, buff=0.1)
        self.play(FadeIn(ab_label))

        wavelet_air = Line(B, B, color=RAY_IN)  # placeholder to keep structure simple
        # distance B still must travel in air along its ray to reach the boundary line's
        # "wavefront" through A is AB*sin(theta1); we visualise it as a small tick.
        B_perp_foot = A + unit(B - A) * (np.dot(B - A, unit(B - A)))
        self.wait(0.3)

        seg_water_wavelet = Line(A, A_prime, color=RAY_OUT, stroke_width=4)
        dotAp = Dot(A_prime, color=RAY_OUT, radius=0.06)
        self.play(Create(seg_water_wavelet), FadeIn(dotAp))
        wavelet_label = MathTex("v_2 T", color=RAY_OUT).scale(0.5)
        wavelet_label.next_to(seg_water_wavelet.get_center(), LEFT, buff=0.15)
        self.play(FadeIn(wavelet_label))

        b_tick = MathTex("v_1 T", color=RAY_IN).scale(0.5)
        b_tick.next_to(Line(A,B).get_center(), UP+RIGHT, buff=0.55)
        self.play(FadeIn(b_tick))

        cap = swap_caption(self, cap,
                            "In the same time T, wavelet from A covers v2*T; ray B covers v1*T.")
        self.wait(1.5)

        # Right triangles ABAp and AB Bp share hypotenuse AB, giving:
        # sin(theta1) = v1*T / AB   and   sin(theta2) = v2*T / AB
        eq1 = MathTex("\\sin\\theta_1", "=", "\\dfrac{v_1 T}{AB}").scale(0.75)
        eq2 = MathTex("\\sin\\theta_2", "=", "\\dfrac{v_2 T}{AB}").scale(0.75)
        eqs = VGroup(eq1, eq2).arrange(DOWN, buff=0.35)
        eqs.to_corner(UR, buff=0.5)
        self.play(Write(eq1))
        self.wait(0.4)
        self.play(Write(eq2))
        self.wait(0.8)

        divide = MathTex(
            "\\dfrac{\\sin\\theta_1}{\\sin\\theta_2}", "=", "\\dfrac{v_1}{v_2}"
        ).scale(0.8)
        divide.next_to(eqs, DOWN, buff=0.4)
        self.play(Write(divide))
        self.wait(0.8)

        cap = swap_caption(self, cap,
                            "Swap speeds for refractive indices, since n = c/v ...")
        final = MathTex("n_1", "\\sin\\theta_1", "=", "n_2", "\\sin\\theta_2").scale(1.15)
        final.set_color_by_tex("n_1", RAY_IN)
        final.set_color_by_tex("n_2", RAY_OUT)
        final.to_edge(DOWN, buff=1.1)

        box = SurroundingRectangle(final, color=GOOD, buff=0.3)
        self.play(TransformFromCopy(divide, final))
        self.play(Create(box))
        cap = swap_caption(self, cap, "This is Snell's Law.")
        self.wait(2)

        self.play(FadeOut(VGroup(
            head, cap, boundary, water, wavefront_0, rA, rB, dotA, rayB_dir_line,
            seg_air, ab_label, seg_water_wavelet, dotAp, wavelet_label, b_tick,
            eqs, divide, final, box
        )))


# ----------------------------------------------------------------------
#  CHAPTER 8 — CRITICAL ANGLE & TOTAL INTERNAL REFLECTION
# ----------------------------------------------------------------------
class Scene08_CriticalAngleTIR(Scene):
    def construct(self):
        head = chapter_header(8, "Critical Angle & Total Internal Reflection", color=GLASS_C)
        self.play(FadeIn(head, shift=DOWN * 0.2))
        cap = caption("Now send light the OTHER way: from glass, out toward air.")
        self.play(FadeIn(cap))

        boundary_y = 0.6
        boundary = Line(LEFT * 5.5, RIGHT * 5.5, color=WHITE, stroke_width=2).shift(UP * boundary_y)
        glass = Rectangle(width=11, height=3.6, color=GLASS_C, fill_color=GLASS_C,
                           fill_opacity=0.18, stroke_width=0)
        glass.next_to(boundary, DOWN, buff=0)
        self.play(FadeIn(glass), Create(boundary))

        P = np.array([0, boundary_y, 0])
        normal = dashed_normal(P, UP, half_len=2.6)
        self.play(Create(normal))

        n1, n2 = 1.5, 1.0
        snell_title = MathTex("n_1 \\sin\\theta_1", "=", "n_2\\sin\\theta_2").scale(0.7)
        snell_title.to_corner(UL, buff=0.6).shift(DOWN*0.3)
        vals = MathTex(f"n_1={n1}\\ (\\text{{glass}}),\\ n_2={n2}\\ (\\text{{air}})").scale(0.55)
        vals.next_to(snell_title, DOWN, buff=0.2).align_to(snell_title, LEFT)
        self.play(Write(snell_title), FadeIn(vals))

        theta1 = ValueTracker(20 * DEGREES)

        def theta2_value():
            s2 = n1 * np.sin(theta1.get_value()) / n2
            return np.arcsin(min(s2, 1.0))

        def in_start():
            a = theta1.get_value()
            return P + np.array([-np.sin(a), -np.cos(a), 0]) * 2.6

        def refr_end():
            a = theta2_value()
            return P + np.array([np.sin(a), np.cos(a), 0]) * 2.6

        def reflect_end():
            a = theta1.get_value()
            return P + np.array([np.sin(a), -np.cos(a), 0]) * 2.6

        r_in = always_redraw(lambda: make_ray(in_start(), P, color=RAY_IN))
        r_refr = always_redraw(lambda: make_ray(P, refr_end(), color=RAY_OUT)
                                if n1 * np.sin(theta1.get_value()) <= n2 else VGroup())
        r_weak_reflect = always_redraw(lambda: make_ray(P, reflect_end(), color=DIM, width=2))

        self.play(Create(r_in))
        self.play(Create(r_refr), Create(r_weak_reflect))
        cap = swap_caption(self, cap,
                            "Leaving the denser medium, the ray bends AWAY from the normal.")
        self.wait(1)

        self.play(theta1.animate.set_value(35 * DEGREES), run_time=1.8)
        self.wait(0.5)

        crit = np.arcsin(n2 / n1)
        cap = swap_caption(self, cap,
                            "As theta1 grows, theta2 races ahead of it toward 90°.")
        self.play(theta1.animate.set_value(crit - 0.001), run_time=2.2)
        self.wait(0.3)

        crit_label = MathTex(
            "\\theta_c:\\ \\ \\theta_2 = 90^\\circ", color=HILITE
        ).scale(0.75).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
        self.play(FadeIn(crit_label))
        cap = swap_caption(self, cap,
                            "At the critical angle, the refracted ray skims flat along the surface.")
        self.wait(1.3)

        crit_formula = MathTex(
            "\\sin\\theta_c", "=", "\\dfrac{n_2}{n_1}"
        ).scale(0.85).next_to(crit_label, DOWN, buff=0.35)
        self.play(Write(crit_formula))
        self.wait(1)

        # Push past critical angle -> total internal reflection.
        cap = swap_caption(self, cap,
                            "Push past theta_c and refraction has nowhere to go — it all reflects.")
        strong_reflect = always_redraw(lambda: make_ray(P, reflect_end(), color=RAY_OUT, width=5))
        self.remove(r_refr)
        self.add(strong_reflect)
        self.play(theta1.animate.set_value(55 * DEGREES), run_time=2)
        self.wait(0.5)

        tir_label = Text("Total Internal Reflection", color=GOOD, weight=BOLD).scale(0.5)
        tir_label.next_to(crit_formula, DOWN, buff=0.5)
        self.play(FadeIn(tir_label, shift=UP * 0.2))
        self.wait(1.2)

        apps = Text("Applications: optical fibres, diamond sparkle, mirages, prisms in binoculars",
                     color=DIM).scale(0.4)
        apps.next_to(tir_label, DOWN, buff=0.35)
        self.play(FadeIn(apps))
        self.wait(2)

        self.play(FadeOut(VGroup(
            head, cap, boundary, glass, normal, snell_title, vals,
            r_in, r_weak_reflect, strong_reflect, crit_label, crit_formula,
            tir_label, apps
        )))


# ----------------------------------------------------------------------
#  CHAPTER 9 — THE MIRROR EQUATION
# ----------------------------------------------------------------------
class Scene09_MirrorEquation(Scene):
    def construct(self):
        head = chapter_header(9, "The Mirror Equation", color=RAY_OUT)
        self.play(FadeIn(head, shift=DOWN * 0.2))
        cap = caption("A concave mirror: pole P, focus F, centre of curvature C.")
        self.play(FadeIn(cap))

        P = np.array([2.6, 0, 0])
        F = np.array([0.6, 0, 0])
        C = np.array([-1.4, 0, 0])
        axis = Line(LEFT * 5.3, RIGHT * 4.0, color=DIM, stroke_width=1.5)

        mirror_arc = ArcBetweenPoints(np.array([2.6, 1.6, 0]), np.array([2.6, -1.6, 0]),
                                      angle=-40 * DEGREES, color=MIRROR_C, stroke_width=6)
        self.play(Create(axis))
        self.play(Create(mirror_arc))

        labels = VGroup()
        for pt, name, col in [(P, "P", INK), (F, "F", ANGLE_OUT), (C, "C", ANGLE_IN)]:
            d = Dot(pt, radius=0.05, color=col)
            t = Text(name, color=col).scale(0.4).next_to(d, DOWN, buff=0.12)
            labels.add(d, t)
        self.play(FadeIn(labels))

        obj_base = np.array([-3.4, 0, 0])
        obj_h = 1.3
        obj = Arrow(obj_base, obj_base + UP * obj_h, buff=0, color=RAY_IN, stroke_width=5)
        self.play(GrowArrow(obj))
        obj_label = Text("object", color=RAY_IN).scale(0.35).next_to(obj, LEFT, buff=0.1)
        self.play(FadeIn(obj_label))

        top = obj_base + UP * obj_h

        # Ray 1: parallel to axis -> reflects through F
        hit1 = np.array([P[0], top[1], 0])
        ray1a = make_ray(top, hit1, color=RAY_OUT, width=3)
        ray1b_end = F + unit(F - hit1) * 6.5
        ray1b = make_ray(hit1, ray1b_end, color=RAY_OUT, width=3)

        # Ray 2: through C -> reflects straight back along itself, so we draw
        # it going to the mirror and back out through the image point.
        dir2 = unit(C - top)
        t_hit = (P[0] - top[0]) / dir2[0]
        hit2 = top + dir2 * t_hit
        ray2a = make_ray(top, hit2, color=RAY_ALT, width=3)
        ray2b = make_ray(hit2, C - unit(C - hit2) * 6.5, color=RAY_ALT, width=3)

        self.play(Create(ray1a))
        self.play(Create(ray1b))
        self.wait(0.3)
        self.play(Create(ray2a))
        self.play(Create(ray2b))
        self.wait(0.3)

        # Where ray1b and ray2b cross gives the (inverted, real) image tip.
        def line_intersection(p1, d1, p2, d2):
            A = np.array([[d1[0], -d2[0]], [d1[1], -d2[1]]])
            b = p2[:2] - p1[:2]
            t = np.linalg.solve(A, b)
            return p1 + d1 * t[0]

        img_tip = line_intersection(hit1, unit(ray1b_end - hit1), hit2, unit((C - unit(C - hit2) * 6.5) - hit2))
        img_base = np.array([img_tip[0], 0, 0])
        image_arrow = Arrow(img_base, img_tip, buff=0, color=GOOD, stroke_width=5)
        self.play(GrowArrow(image_arrow))
        img_label = Text("image (real, inverted)", color=GOOD).scale(0.35)
        img_label.next_to(image_arrow, DOWN, buff=0.15)
        self.play(FadeIn(img_label))
        self.wait(1)

        cap = swap_caption(self, cap,
                            "Two similar triangles connect object height, image height, u, v, f.")

        u_brace = BraceBetweenPoints(P, obj_base, color=RAY_IN, direction=DOWN)
        v_brace = BraceBetweenPoints(P, img_base, color=GOOD, direction=UP).shift(UP*1.9)
        u_txt = MathTex("u", color=RAY_IN).scale(0.6).next_to(u_brace, DOWN, buff=0.1)
        v_txt = MathTex("v", color=GOOD).scale(0.6).next_to(v_brace, UP, buff=0.1)
        self.play(FadeIn(u_brace), FadeIn(u_txt))
        self.play(FadeIn(v_brace), FadeIn(v_txt))
        self.wait(1.2)

        deriv = VGroup(
            MathTex("\\triangle ABP \\sim \\triangle A'B'P", "\\Rightarrow",
                    "\\dfrac{h'}{h} = -\\dfrac{v}{u}").scale(0.6),
            MathTex("\\triangle FB'A' \\sim \\triangle FPO", "\\Rightarrow",
                    "\\dfrac{h'}{h} = \\dfrac{v - f}{f}").scale(0.6),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        deriv.to_corner(UR, buff=0.4)
        self.play(Write(deriv[0]))
        self.wait(0.6)
        self.play(Write(deriv[1]))
        self.wait(0.8)

        combine = MathTex("-\\dfrac{v}{u}", "=", "\\dfrac{v-f}{f}").scale(0.7)
        combine.next_to(deriv, DOWN, buff=0.35).align_to(deriv, LEFT)
        self.play(Write(combine))
        self.wait(0.6)

        final = MathTex("\\dfrac{1}{v}", "+", "\\dfrac{1}{u}", "=", "\\dfrac{1}{f}").scale(1.1)
        final.next_to(combine, DOWN, buff=0.4)
        box = SurroundingRectangle(final, color=GOOD, buff=0.25)
        self.play(TransformFromCopy(combine, final))
        self.play(Create(box))
        self.wait(1)

        mag = MathTex("m", "=", "\\dfrac{h'}{h}", "=", "-\\dfrac{v}{u}").scale(0.75)
        mag.next_to(final, DOWN, buff=0.4)
        self.play(Write(mag))
        cap = swap_caption(self, cap,
                            "Same equation, same sign convention, for concave AND convex mirrors.")
        self.wait(2)

        self.play(FadeOut(VGroup(
            head, cap, axis, mirror_arc, labels, obj, obj_label,
            ray1a, ray1b, ray2a, ray2b, image_arrow, img_label,
            u_brace, v_brace, u_txt, v_txt, deriv, combine, final, box, mag
        )))


# ----------------------------------------------------------------------
#  CHAPTER 10 — THE THIN LENS EQUATION
# ----------------------------------------------------------------------
class Scene10_ThinLensEquation(Scene):
    def construct(self):
        head = chapter_header(10, "The Thin Lens Equation", color=GLASS_C)
        self.play(FadeIn(head, shift=DOWN * 0.2))
        cap = caption("A convex lens: optical centre O, focal points F1 and F2.")
        self.play(FadeIn(cap))

        O = np.array([0, 0, 0])
        F2 = np.array([1.6, 0, 0])
        F1 = np.array([-1.6, 0, 0])
        axis = Line(LEFT * 5.3, RIGHT * 4.6, color=DIM, stroke_width=1.5)

        lens = VGroup(
            Line(np.array([0, 1.7, 0]), np.array([0, -1.7, 0]), color=GLASS_C, stroke_width=2),
            ArcBetweenPoints(np.array([0, 1.7, 0]), np.array([0, -1.7, 0]), angle=60*DEGREES,
                             color=GLASS_C, stroke_width=5),
            ArcBetweenPoints(np.array([0, 1.7, 0]), np.array([0, -1.7, 0]), angle=-60*DEGREES,
                             color=GLASS_C, stroke_width=5),
        )
        self.play(Create(axis))
        self.play(Create(lens))

        labels = VGroup()
        for pt, name, col in [(O, "O", INK), (F2, "F2", ANGLE_OUT), (F1, "F1", ANGLE_IN)]:
            d = Dot(pt, radius=0.05, color=col)
            t = Text(name, color=col).scale(0.4).next_to(d, DOWN, buff=0.12)
            labels.add(d, t)
        self.play(FadeIn(labels))

        obj_base = np.array([-3.6, 0, 0])
        obj_h = 1.2
        obj = Arrow(obj_base, obj_base + UP * obj_h, buff=0, color=RAY_IN, stroke_width=5)
        obj_label = Text("object", color=RAY_IN).scale(0.35).next_to(obj, LEFT, buff=0.1)
        self.play(GrowArrow(obj), FadeIn(obj_label))
        top = obj_base + UP * obj_h

        # Ray 1: parallel to axis, refracts through F2 on the far side.
        hit1 = np.array([0, top[1], 0])
        ray1a = make_ray(top, hit1, color=RAY_OUT, width=3)
        ray1b_end = F2 + unit(F2 - hit1) * 6.0
        ray1b = make_ray(hit1, ray1b_end, color=RAY_OUT, width=3)

        # Ray 2: through the optical centre, undeviated.
        ray2_end = O + unit(O - top) * 8.5
        ray2 = make_ray(top, ray2_end, color=RAY_ALT, width=3)

        self.play(Create(ray1a))
        self.play(Create(ray1b))
        self.wait(0.2)
        self.play(Create(ray2))

        def line_intersection(p1, d1, p2, d2):
            A = np.array([[d1[0], -d2[0]], [d1[1], -d2[1]]])
            b = p2[:2] - p1[:2]
            t = np.linalg.solve(A, b)
            return p1 + d1 * t[0]

        img_tip = line_intersection(hit1, unit(ray1b_end - hit1), top, unit(ray2_end - top))
        img_base = np.array([img_tip[0], 0, 0])
        image_arrow = Arrow(img_base, img_tip, buff=0, color=GOOD, stroke_width=5)
        img_label = Text("image (real, inverted)", color=GOOD).scale(0.35)
        img_label.next_to(image_arrow, DOWN, buff=0.15)
        self.play(GrowArrow(image_arrow), FadeIn(img_label))
        self.wait(1)

        cap = swap_caption(self, cap,
                            "Same trick: similar triangles sharing the optical centre and F2.")

        u_brace = BraceBetweenPoints(O, obj_base, color=RAY_IN, direction=DOWN)
        v_brace = BraceBetweenPoints(O, img_base, color=GOOD, direction=DOWN).shift(DOWN*0.9)
        u_txt = MathTex("u", color=RAY_IN).scale(0.6).next_to(u_brace, DOWN, buff=0.1)
        v_txt = MathTex("v", color=GOOD).scale(0.6).next_to(v_brace, DOWN, buff=0.1)
        self.play(FadeIn(u_brace), FadeIn(u_txt), FadeIn(v_brace), FadeIn(v_txt))
        self.wait(1)

        deriv = VGroup(
            MathTex("\\triangle OAB \\sim \\triangle OA'B'", "\\Rightarrow",
                    "\\dfrac{h'}{h} = \\dfrac{v}{u}").scale(0.6),
            MathTex("\\triangle F_2OC \\sim \\triangle F_2A'B'", "\\Rightarrow",
                    "\\dfrac{h'}{h} = \\dfrac{v-f}{f}").scale(0.6),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        deriv.to_corner(UR, buff=0.4)
        self.play(Write(deriv[0]))
        self.wait(0.5)
        self.play(Write(deriv[1]))
        self.wait(0.8)

        final = MathTex("\\dfrac{1}{v}", "-", "\\dfrac{1}{u}", "=", "\\dfrac{1}{f}").scale(1.1)
        final.next_to(deriv, DOWN, buff=0.5)
        box = SurroundingRectangle(final, color=GOOD, buff=0.25)
        self.play(Write(final))
        self.play(Create(box))
        self.wait(1)

        lensmaker = MathTex(
            "\\dfrac{1}{f}", "=", "(n-1)\\left(\\dfrac{1}{R_1}-\\dfrac{1}{R_2}\\right)"
        ).scale(0.7)
        lensmaker.next_to(box, DOWN, buff=0.4)
        self.play(Write(lensmaker))
        cap = swap_caption(self, cap,
                            "f itself comes from the lens-maker's equation — glass curvature and n.")
        self.wait(2)

        self.play(FadeOut(VGroup(
            head, cap, axis, lens, labels, obj, obj_label, ray1a, ray1b, ray2,
            image_arrow, img_label, u_brace, v_brace, u_txt, v_txt,
            deriv, final, box, lensmaker
        )))


# ----------------------------------------------------------------------
#  CHAPTER 11 — READING AN IMAGE: REAL/VIRTUAL, ERECT/INVERTED, SIZE
# ----------------------------------------------------------------------
class Scene11_ImageCharacteristics(Scene):
    def construct(self):
        head = chapter_header(11, "Reading an Image Off the Numbers", color=HILITE)
        self.play(FadeIn(head, shift=DOWN * 0.2))
        cap = caption("v, u and m carry everything you need to know about the image.")
        self.play(FadeIn(cap))

        rules = VGroup(
            MathTex("v > 0", "\\Rightarrow", "\\text{real image (light actually meets there)}").scale(0.55),
            MathTex("v < 0", "\\Rightarrow", "\\text{virtual image (light only appears to meet)}").scale(0.55),
            MathTex("m > 0", "\\Rightarrow", "\\text{erect}", "\\qquad", "m < 0", "\\Rightarrow", "\\text{inverted}").scale(0.55),
            MathTex("|m| > 1", "\\Rightarrow", "\\text{magnified}", "\\qquad", "|m| < 1", "\\Rightarrow", "\\text{diminished}").scale(0.55),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rules.next_to(cap, UP, buff=0.6)
        for r in rules:
            self.play(Write(r), run_time=0.9)
        self.wait(1.5)
        self.play(FadeOut(rules))

        cap = swap_caption(self, cap, "Concave mirror: the image morphs as the object moves in.")

        headers = ["object position", "image"]
        rows_data = [
            ("beyond C", "real, inverted, diminished, between F & C"),
            ("at C", "real, inverted, same size, at C"),
            ("between C & F", "real, inverted, magnified, beyond C"),
            ("at F", "at infinity (rays leave parallel)"),
            ("between F & P", "virtual, erect, magnified, behind mirror"),
        ]
        table = VGroup()
        for pos, img in rows_data:
            row = VGroup(
                Text(pos, color=RAY_IN).scale(0.4),
                Text(img, color=GOOD).scale(0.36),
            ).arrange(RIGHT, buff=0.5, aligned_edge=LEFT)
            table.add(row)
        table.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        table.scale(0.95).move_to(ORIGIN).shift(UP * 0.2)

        for row in table:
            self.play(FadeIn(row, shift=UP * 0.1), run_time=0.6)
        self.wait(1.5)

        cap = swap_caption(self, cap,
                            "A convex mirror never gets a chance: always virtual, erect, diminished.")
        self.wait(1.2)
        self.play(FadeOut(table))

        cap = swap_caption(self, cap,
                            "A convex lens runs the same story as a concave mirror, object-side out.")
        lens_rows = [
            ("beyond 2F", "real, inverted, diminished, between F & 2F (other side)"),
            ("at 2F", "real, inverted, same size, at 2F"),
            ("between F & 2F", "real, inverted, magnified, beyond 2F"),
            ("at F", "at infinity"),
            ("between F & lens", "virtual, erect, magnified, same side as object"),
        ]
        table2 = VGroup()
        for pos, img in lens_rows:
            row = VGroup(
                Text(pos, color=GLASS_C).scale(0.4),
                Text(img, color=GOOD).scale(0.34),
            ).arrange(RIGHT, buff=0.5, aligned_edge=LEFT)
            table2.add(row)
        table2.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        table2.scale(0.95).move_to(ORIGIN).shift(UP * 0.2)

        for row in table2:
            self.play(FadeIn(row, shift=UP * 0.1), run_time=0.6)
        self.wait(1.5)

        cap = swap_caption(self, cap,
                            "A concave lens, like a convex mirror, always makes a virtual, diminished, erect image.")
        self.wait(1.5)

        self.play(FadeOut(VGroup(head, cap, table2)))


# ----------------------------------------------------------------------
#  CHAPTER 12 — OUTRO / RECAP
# ----------------------------------------------------------------------
class Scene12_Outro(Scene):
    def construct(self):
        title = Text("The Whole Story", weight=BOLD, color=INK).scale(1.0).to_edge(UP, buff=0.8)
        self.play(Write(title))

        pillars = VGroup(
            MathTex("i", "=", "r", color=ANGLE_OUT).scale(0.9),
            MathTex("n_1\\sin\\theta_1 = n_2\\sin\\theta_2", color=GLASS_C).scale(0.9),
            MathTex("\\sin\\theta_c = \\dfrac{n_2}{n_1}", color=HILITE).scale(0.9),
            MathTex("\\dfrac{1}{v}+\\dfrac{1}{u}=\\dfrac{1}{f}", color=RAY_OUT).scale(0.9),
            MathTex("\\dfrac{1}{v}-\\dfrac{1}{u}=\\dfrac{1}{f}", color=GOOD).scale(0.9),
        )
        tags = VGroup(
            Text("reflection", color=DIM).scale(0.35),
            Text("refraction (Snell)", color=DIM).scale(0.35),
            Text("critical angle / TIR", color=DIM).scale(0.35),
            Text("mirror equation", color=DIM).scale(0.35),
            Text("thin lens equation", color=DIM).scale(0.35),
        )
        rows = VGroup(*[
            VGroup(p, t).arrange(RIGHT, buff=0.8) for p, t in zip(pillars, tags)
        ]).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        rows.next_to(title, DOWN, buff=0.7)

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.7)
        self.wait(1.5)

        closer = Text(
            "Every one of these came from the same two questions:\n"
            "where does the normal point, and how fast does light travel here?",
            color=INK
        ).scale(0.45)
        closer.next_to(rows, DOWN, buff=0.8)
        self.play(Write(closer))
        self.wait(2.5)

        self.play(FadeOut(VGroup(title, rows, closer)))
        thanks = Text("Thanks for watching.", weight=BOLD, color=INK).scale(1.0)
        self.play(Write(thanks))
        self.wait(2)
        self.play(FadeOut(thanks))