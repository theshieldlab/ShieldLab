"""
NEWTON'S LAWS OF MOTION — a 3Blue1Brown-style educational video
=================================================================

Five scenes, meant to be watched/rendered in order, telling one
continuous story: intro -> Law 1 (inertia) -> Law 2 (F = ma) ->
Law 3 (action/reaction) -> summary.

RENDER
-------
Preview quality (fast, for editing):
    manim -pql newtons_laws_manim.py Introduction
    manim -pql newtons_laws_manim.py FirstLaw
    manim -pql newtons_laws_manim.py SecondLaw
    manim -pql newtons_laws_manim.py ThirdLaw
    manim -pql newtons_laws_manim.py Summary

Final 1080p60 render of everything, in story order:
    manim -qh newtons_laws_manim.py Introduction FirstLaw SecondLaw ThirdLaw Summary

Then concatenate the five mp4s in your editor (or with ffmpeg) in that order.

REQUIRES: Manim Community Edition >= 0.18
    pip install manim
(LaTeX distribution required for MathTex/Tex — e.g. TeX Live or MiKTeX.)
"""

from manim import *
import numpy as np

# ----------------------------------------------------------------------
# Shared palette / constants — keep every scene visually consistent
# ----------------------------------------------------------------------
config.background_color = "#0e0e17"

BLUE = "#58C4DD"       # velocity
YELLOW = "#FFD700"     # acceleration
RED = "#FC6255"        # force
GREEN = "#83C167"      # secondary / mass
GREY = "#888888"       # grid / faded elements
WHITE_T = "#ECECEC"

FORCE_COLOR = RED
VELOCITY_COLOR = BLUE
ACCEL_COLOR = YELLOW
MASS_COLOR = GREEN


def labeled_vector(start, vec, color, tex, direction=UP, scale=0.7):
    """An Arrow plus a MathTex label near its tip. Returns a VGroup."""
    arrow = Arrow(
        start, start + vec, buff=0, color=color,
        stroke_width=7, max_tip_length_to_length_ratio=0.22,
    )
    label = MathTex(tex, color=color).scale(scale)
    label.next_to(arrow.get_end(), direction, buff=0.15)
    return VGroup(arrow, label)


def faded_grid():
    grid = NumberPlane(
        x_range=(-8, 8, 1), y_range=(-5, 5, 1),
        background_line_style={"stroke_color": GREY, "stroke_width": 1, "stroke_opacity": 0.25},
        axis_config={"stroke_opacity": 0},
    )
    return grid


def title_block(main, sub=None):
    t = Text(main, weight=BOLD, font_size=48)
    group = VGroup(t)
    if sub:
        s = Text(sub, font_size=28, color=GREY)
        s.next_to(t, DOWN, buff=0.3)
        group.add(s)
    group.to_edge(UP, buff=0.6)
    return group


# ========================================================================
# SCENE 1 — INTRODUCTION
# ========================================================================
class Introduction(Scene):
    def construct(self):
        grid = faded_grid()
        self.play(FadeIn(grid), run_time=1.5)

        title = Text("THE LAWS OF MOTION", weight=BOLD, font_size=56)
        subtitle = Text("How three simple sentences describe the entire universe", font_size=26, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=1.8)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(subtitle))
        self.play(title.animate.to_edge(UP, buff=0.5))

        # --- The historical hook: Aristotle vs. Galileo/Newton ---
        aristotle = Text("Aristotle (~350 BCE):", font_size=30, color=GREY)
        aristotle_claim = Text('"Objects need a constant push to keep moving."', font_size=28, slant=ITALIC)
        arist_group = VGroup(aristotle, aristotle_claim).arrange(DOWN, aligned_edge=LEFT)
        arist_group.shift(UP * 0.8)

        self.play(FadeIn(arist_group, shift=UP * 0.2))
        self.wait(1.5)

        cross = Cross(aristotle_claim, stroke_color=RED, stroke_width=6)
        self.play(Create(cross))
        self.wait(0.5)

        newton = Text("Newton (1687), building on Galileo:", font_size=30, color=GREY)
        newton_claim = Text('"An object keeps its motion unless something changes it."', font_size=28, slant=ITALIC, color=BLUE)
        newton_group = VGroup(newton, newton_claim).arrange(DOWN, aligned_edge=LEFT)
        newton_group.next_to(arist_group, DOWN, buff=0.9, aligned_edge=LEFT)

        self.play(FadeIn(newton_group, shift=UP * 0.2))
        self.wait(2)

        self.play(FadeOut(arist_group), FadeOut(cross), FadeOut(newton_group))

        # --- Preview the three laws as a vertical menu ---
        laws = VGroup(
            self._law_row("I.", "Inertia", "An object at rest stays at rest;\nan object in motion stays in motion.", BLUE),
            self._law_row("II.", "F = ma", "Force causes acceleration,\nin proportion to mass.", YELLOW),
            self._law_row("III.", "Action–Reaction", "Every force is paired with an\nequal, opposite force.", RED),
        ).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        laws.move_to(ORIGIN).shift(DOWN * 0.3)

        for row in laws:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(0.3)

        self.wait(2)
        self.play(FadeOut(laws), FadeOut(title), FadeOut(grid))
        self.wait(0.5)

    def _law_row(self, numeral, name, desc, color):
        num = Text(numeral, font_size=40, color=color, weight=BOLD).set_width(0.9)
        name_txt = Text(name, font_size=34, color=color, weight=BOLD)
        desc_txt = Text(desc, font_size=22, color=WHITE_T, line_spacing=0.9)
        right = VGroup(name_txt, desc_txt).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        row = VGroup(num, right).arrange(RIGHT, buff=0.4, aligned_edge=UP)
        return row


# ========================================================================
# SCENE 2 — FIRST LAW (Inertia)
# ========================================================================
class FirstLaw(Scene):
    def construct(self):
        header = title_block("Newton's First Law", "The Law of Inertia")
        self.play(Write(header))
        self.wait(0.5)

        statement = Text(
            "An object's velocity does not change\nunless a net force acts on it.",
            font_size=30, line_spacing=1.2,
        )
        self.play(FadeIn(statement, shift=UP * 0.2))
        self.wait(2)
        self.play(statement.animate.scale(0.55).to_corner(UL, buff=0.4).shift(DOWN * 0.3))

        # ---------------- Demo 1: no force -> constant velocity ----------------
        ground = Line(LEFT * 6, RIGHT * 6, color=GREY).shift(DOWN * 1.5)
        self.play(Create(ground))

        ball = Dot(radius=0.22, color=BLUE).move_to(LEFT * 5 + DOWN * 1.1)
        trail = TracedPath(ball.get_center, stroke_color=BLUE, stroke_opacity=0.5, stroke_width=3)
        self.add(trail)

        v_label = MathTex(r"\vec{v} = \text{constant}", color=BLUE).scale(0.8)
        v_label.next_to(ground, UP, buff=2.0).to_edge(RIGHT, buff=1.0)

        self.play(FadeIn(ball))
        self.play(FadeIn(v_label))
        self.play(ball.animate.move_to(RIGHT * 5 + DOWN * 1.1), run_time=3, rate_func=linear)
        self.wait(0.5)

        caption1 = Text("No net force  ->  no change in velocity (this ball never had one to begin with)", font_size=22, color=GREY)
        caption1.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption1))
        self.wait(1.5)
        self.play(FadeOut(VGroup(ball, trail, v_label, caption1)))

        # ---------------- Demo 2: friction -> unbalanced force -> slows down ----------------
        ball2 = Dot(radius=0.22, color=BLUE).move_to(LEFT * 5 + DOWN * 1.1)
        trail2 = TracedPath(ball2.get_center, stroke_color=BLUE, stroke_opacity=0.5, stroke_width=3)
        self.add(trail2)

        friction_arrow = always_redraw(
            lambda: Arrow(
                ball2.get_center() + RIGHT * 0.3,
                ball2.get_center() + LEFT * 0.5,
                buff=0, color=RED, stroke_width=6, max_tip_length_to_length_ratio=0.3,
            ) if ball2.get_center()[0] < 4.5 else VMobject()
        )
        friction_label = Text("friction (unbalanced force)", font_size=22, color=RED)
        friction_label.next_to(ground, DOWN, buff=0.3).align_to(ground, LEFT)

        self.play(FadeIn(ball2), FadeIn(friction_label))
        self.add(friction_arrow)

        def decelerate(mob, alpha):
            # position from x0=-5 with v0=4, decelerating at a=-1.2 (arbitrary units), clipped at rest
            t = alpha * 4.5
            v0, a = 4.0, -1.2
            x = -5 + v0 * t + 0.5 * a * t**2
            x = min(x, 3.5)
            mob.move_to([x, -1.1, 0])

        self.play(UpdateFromAlphaFunc(ball2, decelerate), run_time=3.2, rate_func=linear)
        self.wait(0.3)
        caption2 = Text("An unbalanced force (friction) changes the velocity -> the ball decelerates", font_size=22, color=GREY)
        caption2.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption2))
        self.wait(2)

        self.play(FadeOut(VGroup(ball2, trail2, friction_label, caption2, friction_arrow, ground)))

        # ---------------- The math ----------------
        eq = MathTex(r"\sum \vec{F} = 0", r"\;\;\Longrightarrow\;\;", r"\vec{a} = 0", r"\;\;\Longrightarrow\;\;", r"\vec{v} = \text{constant}")
        eq.set_color_by_tex(r"\sum \vec{F}", RED)
        eq.set_color_by_tex(r"\vec{a}", YELLOW)
        eq.set_color_by_tex(r"\vec{v}", BLUE)
        eq.scale(1.1).move_to(UP * 0.3)

        self.play(FadeOut(statement))
        self.play(Write(eq))
        self.wait(2)

        galileo_note = Text(
            "Galileo first imagined a frictionless world to see this clearly —\n"
            "Newton turned the idea into a law.",
            font_size=24, color=GREY, line_spacing=1.2,
        )
        galileo_note.next_to(eq, DOWN, buff=1.0)
        self.play(FadeIn(galileo_note, shift=UP * 0.2))
        self.wait(2.5)

        self.play(FadeOut(VGroup(eq, galileo_note, header)))
        self.wait(0.5)


# ========================================================================
# SCENE 3 — SECOND LAW (F = ma)
# ========================================================================
class SecondLaw(Scene):
    def construct(self):
        header = title_block("Newton's Second Law", "Quantifying the Push")
        self.play(Write(header))
        self.wait(0.5)

        # ---------------- Derivation from momentum ----------------
        p_def = MathTex(r"\vec{p} = m\vec{v}", font_size=44)
        p_label = Text("momentum := mass \u00d7 velocity", font_size=24, color=GREY)
        p_group = VGroup(p_def, p_label).arrange(DOWN, buff=0.3)
        self.play(FadeIn(p_group, shift=UP * 0.2))
        self.wait(1.5)

        step1 = MathTex(r"\vec{F}", r"=", r"\frac{d\vec{p}}{dt}", font_size=44)
        step1_label = Text("force := the rate momentum changes", font_size=24, color=GREY)
        step1_group = VGroup(step1, step1_label).arrange(DOWN, buff=0.3)
        self.play(ReplacementTransform(p_group[0].copy(), step1[2]), FadeIn(step1[0]), FadeIn(step1[1]))
        self.play(FadeIn(step1_label))
        self.wait(1.5)
        self.play(FadeOut(p_group))
        self.play(step1_group.animate.move_to(UP * 1.7))

        step2 = MathTex(r"\vec{F} = \frac{d(m\vec{v})}{dt} = m\frac{d\vec{v}}{dt}", font_size=44)
        step2.next_to(step1_group, DOWN, buff=0.7)
        note2 = Text("(mass constant, for now)", font_size=22, color=GREY)
        note2.next_to(step2, DOWN, buff=0.2)
        self.play(FadeIn(step2, shift=UP * 0.2))
        self.play(FadeIn(note2))
        self.wait(1.5)

        final_eq = MathTex(r"\vec{F} = m\vec{a}", font_size=64)
        final_eq.set_color_by_tex("F", RED)
        final_eq.next_to(step2, DOWN, buff=0.7)
        box = SurroundingRectangle(final_eq, color=YELLOW, buff=0.3)
        self.play(TransformFromCopy(step2, final_eq))
        self.play(Create(box))
        self.wait(2)

        self.play(FadeOut(VGroup(step1_group, step2, note2)))
        self.play(final_eq.animate.scale(0.7).to_corner(UR, buff=0.5), FadeOut(box))

        # ---------------- Visual demo: pushing a box, varying the force ----------------
        ground = Line(LEFT * 6, RIGHT * 6, color=GREY).shift(DOWN * 1.8)
        box_mob = Square(side_length=1.0, color=GREEN, fill_opacity=0.4).move_to(LEFT * 4.5 + DOWN * 1.3)
        mass_label = MathTex("m", color=GREEN).move_to(box_mob.get_center())

        force_tracker = ValueTracker(1.0)  # relative force magnitude

        f_arrow = always_redraw(lambda: labeled_vector(
            box_mob.get_left() + LEFT * 0.1,
            LEFT * force_tracker.get_value() * 1.0,
            RED, "F", direction=UP,
        ).next_to(box_mob, LEFT, buff=0.15))

        a_arrow = always_redraw(lambda: labeled_vector(
            box_mob.get_right() + RIGHT * 0.1,
            RIGHT * force_tracker.get_value() * 0.9,
            YELLOW, "a", direction=UP,
        ).next_to(box_mob, RIGHT, buff=0.15))

        self.play(Create(ground), FadeIn(box_mob), FadeIn(mass_label))
        self.wait(0.3)
        self.play(FadeIn(f_arrow), FadeIn(a_arrow))
        self.wait(0.5)

        weak_caption = Text("small F  ->  small a", font_size=24, color=GREY).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(weak_caption))
        self.play(force_tracker.animate.set_value(1.0), run_time=0.1)
        self.wait(1)

        strong_caption = Text("bigger F  ->  bigger a  (same mass)", font_size=24, color=GREY).to_edge(DOWN, buff=0.5)
        self.play(force_tracker.animate.set_value(3.0), run_time=1.5)
        self.play(ReplacementTransform(weak_caption, strong_caption))
        self.wait(1.5)

        self.play(FadeOut(VGroup(f_arrow, a_arrow, strong_caption, box_mob, mass_label, ground)))

        # ---------------- Graphs: a vs F, and a vs m ----------------
        axes1 = Axes(
            x_range=[0, 5, 1], y_range=[0, 5, 1], x_length=5, y_length=3.2,
            axis_config={"include_tip": True, "stroke_color": GREY},
        ).shift(LEFT * 3.3 + DOWN * 1.0)
        axes1_labels = axes1.get_axis_labels(x_label=MathTex("F").scale(0.7), y_label=MathTex("a").scale(0.7))
        graph1 = axes1.plot(lambda x: x, color=YELLOW, x_range=[0, 5])
        graph1_label = Text("fixed mass:\na is proportional to F", font_size=20, color=GREY)
        graph1_label.next_to(axes1, UP, buff=0.2)

        axes2 = Axes(
            x_range=[0.5, 5, 1], y_range=[0, 5, 1], x_length=5, y_length=3.2,
            axis_config={"include_tip": True, "stroke_color": GREY},
        ).shift(RIGHT * 3.3 + DOWN * 1.0)
        axes2_labels = axes2.get_axis_labels(x_label=MathTex("m").scale(0.7), y_label=MathTex("a").scale(0.7))
        graph2 = axes2.plot(lambda x: 3.0 / x, color=GREEN, x_range=[0.6, 5])
        graph2_label = Text("fixed force:\na shrinks as m grows", font_size=20, color=GREY)
        graph2_label.next_to(axes2, UP, buff=0.2)

        self.play(
            Create(axes1), FadeIn(axes1_labels), FadeIn(graph1_label),
            Create(axes2), FadeIn(axes2_labels), FadeIn(graph2_label),
        )
        self.play(Create(graph1), Create(graph2), run_time=2)
        self.wait(2.5)

        units_note = Text("1 Newton (N) = 1 kg\u00b7m/s\u00b2", font_size=24, color=WHITE_T)
        units_note.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(units_note))
        self.wait(2)

        self.play(FadeOut(VGroup(
            axes1, axes1_labels, graph1, graph1_label,
            axes2, axes2_labels, graph2, graph2_label,
            units_note, final_eq, header,
        )))
        self.wait(0.5)


# ========================================================================
# SCENE 4 — THIRD LAW (Action / Reaction)
# ========================================================================
class ThirdLaw(Scene):
    def construct(self):
        header = title_block("Newton's Third Law", "Action and Reaction")
        self.play(Write(header))
        self.wait(0.5)

        statement = Text(
            "If A pushes on B, then B pushes back on A\nwith equal magnitude and opposite direction.",
            font_size=28, line_spacing=1.2,
        )
        self.play(FadeIn(statement, shift=UP * 0.2))
        self.wait(2)
        self.play(statement.animate.scale(0.55).to_corner(UL, buff=0.4).shift(DOWN * 0.3))

        # ---------------- Demo: two skaters push apart ----------------
        skater_a = Square(side_length=0.9, color=BLUE, fill_opacity=0.5).move_to(LEFT * 1.0)
        skater_b = Square(side_length=0.9, color=RED, fill_opacity=0.5).move_to(RIGHT * 1.0)
        label_a = Text("A", font_size=26).move_to(skater_a)
        label_b = Text("B", font_size=26).move_to(skater_b)

        self.play(FadeIn(skater_a), FadeIn(skater_b), FadeIn(label_a), FadeIn(label_b))
        self.wait(0.5)

        force_ab = labeled_vector(skater_a.get_right() + RIGHT * 0.05, RIGHT * 1.3, RED, "F_{B\\,on\\,A}", direction=UP)
        force_ba = labeled_vector(skater_b.get_left() + LEFT * 0.05, LEFT * 1.3, BLUE, "F_{A\\,on\\,B}", direction=UP)
        force_ab.shift(LEFT * 1.3)
        force_ba.shift(RIGHT * 1.3)

        self.play(FadeIn(force_ab), FadeIn(force_ba))
        note = Text("equal size, opposite direction, acting on DIFFERENT objects", font_size=22, color=GREY)
        note.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(note))
        self.wait(1.5)

        self.play(FadeOut(force_ab), FadeOut(force_ba))
        self.play(
            skater_a.animate.shift(LEFT * 3.5), label_a.animate.shift(LEFT * 3.5),
            skater_b.animate.shift(RIGHT * 3.5), label_b.animate.shift(RIGHT * 3.5),
            run_time=2.2, rate_func=rush_from,
        )
        self.wait(1)
        self.play(FadeOut(VGroup(skater_a, skater_b, label_a, label_b, note)))

        # ---------------- Rocket example ----------------
        rocket_title = Text("The same idea launches rockets:", font_size=26, color=GREY)
        rocket_title.shift(UP * 1.8)
        self.play(FadeIn(rocket_title))

        rocket = Triangle(color=WHITE_T, fill_opacity=0.8).scale(0.5).rotate(0).move_to(DOWN * 0.5)
        rocket.set_color(WHITE_T)
        exhaust = Triangle(color=YELLOW, fill_opacity=0.9).scale(0.35).rotate(PI).next_to(rocket, DOWN, buff=0.0)

        thrust_arrow = labeled_vector(exhaust.get_bottom(), DOWN * 1.2, YELLOW, r"F_{\text{on gas}}", direction=DOWN)
        push_arrow = labeled_vector(rocket.get_top(), UP * 1.2, RED, r"F_{\text{on rocket}}", direction=UP)

        self.play(FadeIn(rocket), FadeIn(exhaust))
        self.play(FadeIn(thrust_arrow), FadeIn(push_arrow))
        self.wait(1)

        rocket_group = VGroup(rocket, exhaust, thrust_arrow, push_arrow)
        self.play(rocket_group.animate.shift(UP * 2.5), run_time=1.8, rate_func=rush_into)
        self.wait(1)
        self.play(FadeOut(rocket_group), FadeOut(rocket_title))

        # ---------------- Common misconception: book on table ----------------
        misconception_title = Text("A common mix-up:", font_size=28, color=YELLOW)
        misconception_title.shift(UP * 1.8)
        self.play(FadeIn(misconception_title))

        table = Line(LEFT * 2.5, RIGHT * 2.5, color=GREY, stroke_width=8).shift(DOWN * 0.5)
        book = Rectangle(width=1.6, height=0.5, color=GREEN, fill_opacity=0.5).next_to(table, UP, buff=0)

        gravity_arrow = labeled_vector(book.get_center(), DOWN * 1.2, RED, r"\vec{W}\ (\text{gravity on book})", direction=DOWN)
        normal_arrow = labeled_vector(book.get_center(), UP * 1.2, BLUE, r"\vec{N}\ (\text{table on book})", direction=UP)

        self.play(Create(table), FadeIn(book))
        self.play(FadeIn(gravity_arrow), FadeIn(normal_arrow))
        self.wait(1)

        wrong_note = Text("These look like an action/reaction pair — but they are NOT:", font_size=22, color=GREY)
        wrong_note2 = Text("both act on the SAME object (the book).", font_size=22, color=GREY)
        wrong_group = VGroup(wrong_note, wrong_note2).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=1.0)
        self.play(FadeIn(wrong_group))
        self.wait(2.5)

        right_note = Text(
            "The true 3rd-law pair to gravity-on-book is gravity-on-Earth (book pulls Earth up too);\n"
            "the pair to the table's push is the book pushing back down on the table.",
            font_size=20, color=WHITE_T, line_spacing=1.2,
        )
        right_note.to_edge(DOWN, buff=0.4)
        self.play(FadeOut(wrong_group), FadeIn(right_note, shift=UP * 0.2))
        self.wait(3)

        self.play(FadeOut(VGroup(
            table, book, gravity_arrow, normal_arrow, misconception_title, right_note, statement, header,
        )))
        self.wait(0.5)


# ========================================================================
# SCENE 5 — SUMMARY
# ========================================================================
class Summary(Scene):
    def construct(self):
        title = Text("Putting It All Together", weight=BOLD, font_size=48)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP, buff=0.6))
        self.wait(0.5)

        law1 = self._law_card("I", "Inertia", r"\sum \vec{F} = 0 \;\Rightarrow\; \vec{v} = \text{const}", BLUE)
        law2 = self._law_card("II", "F = ma", r"\vec{F} = m\vec{a}", YELLOW)
        law3 = self._law_card("III", "Action–Reaction", r"\vec{F}_{A\to B} = -\vec{F}_{B\to A}", RED)

        cards = VGroup(law1, law2, law3).arrange(RIGHT, buff=0.6)
        cards.move_to(ORIGIN).shift(UP * 0.2)

        for c in cards:
            self.play(FadeIn(c, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)

        unifying = Text(
            "Law I is really Law II with F = 0.\nLaw III is what lets forces come in consistent pairs\n"
            "so that momentum is conserved for a system as a whole.",
            font_size=24, color=GREY, line_spacing=1.2,
        )
        unifying.next_to(cards, DOWN, buff=0.9)
        self.play(FadeIn(unifying, shift=UP * 0.2))
        self.wait(3)

        self.play(FadeOut(unifying))

        closing = Text("Three sentences. The motion of everything.", font_size=32, color=WHITE_T)
        closing.move_to(DOWN * 2.2)
        self.play(Write(closing))
        self.wait(2)

        thanks = Text("Thanks for watching — see you in the next one.", font_size=26, color=GREY)
        thanks.next_to(closing, DOWN, buff=0.5)
        self.play(FadeIn(thanks))
        self.wait(2)

        self.play(FadeOut(VGroup(title, cards, closing, thanks)))
        self.wait(0.5)

    def _law_card(self, numeral, name, eq_tex, color):
        box = RoundedRectangle(corner_radius=0.15, width=3.6, height=3.0, color=color, fill_opacity=0.08)
        num = Text(numeral, font_size=40, color=color, weight=BOLD)
        name_txt = Text(name, font_size=26, color=WHITE_T)
        eq = MathTex(eq_tex, color=color).scale(0.75)
        content = VGroup(num, name_txt, eq).arrange(DOWN, buff=0.35)
        content.move_to(box.get_center())
        return VGroup(box, content)