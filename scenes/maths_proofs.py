import random

from random import uniform

from manim import *

from shieldlab.creatures.shield_creatures import (
    TeacherCreature, StudentCreature, CreatureScene,
    create_classroom, all_look_at_equation, all_look_at_teacher, creature_thinks,
    students_confused, teacher_teaches, student_raises_hand,
    teacher_points_to, blink_staggered, classroom_idle_blinks,
    SHIELD_BLACK, SHIELD_WHITE, TEACHER_COLOR,
    STUDENT_BLUE, STUDENT_GREEN, STUDENT_YELLOW,
)


#global style configs

config.background_color = "#000000"

PRIMARY   = "#58A6FF"   #blue
ACCENT    = "#F0C040"   #yellow
WARNING   = "#FF6B6B"   #red / question
SUCCESS   = "#3FB950"   #green
OFFWHITE  = "#E6EDF3"   #near-white text
DIMGRAY   = "#484F58"   #subtle outlines / shadows
PAPERBG   = "#F5F0E8"   #exam-paper cream


# ─────────────────────────────────────────────
# HELPER UTILITIES
# ─────────────────────────────────────────────


def styled_text(text: str, size: int = 36, color=OFFWHITE, **kwargs) -> Text:
    return Text(text, font_size=size, color=color, **kwargs)


def styled_math(tex: str, size: int = 42, color=OFFWHITE, **kwargs) -> MathTex:
    return MathTex(tex, font_size=size, color=color, **kwargs)


# ─────────────────────────────────────────────
# SCENE 1 – intro ----KCSE QUESTION
# ─────────────────────────────────────────────

class Scene1(Scene): #Intro
    """
    An exam paper on screen
    The question 'Prove that 1 + 1 = 2 (4 marks)' is written
    """

    def construct(self):
        # exam paper rectangle
        paper = Rectangle(
            width=7.2,
            height=4.5,
            fill_color=PAPERBG,
            fill_opacity=1,
            stroke_color=DIMGRAY,
            stroke_width=1.5,
        )

        # Header bar
        header_bar = Rectangle(
            width=7.2,
            height=0.6,
            fill_color="#D6CDBF",
            fill_opacity=1,
            stroke_width=0,
        ).align_to(paper, UP).align_to(paper, LEFT)

        exam_title = Text(
            "-- MATHEMATICS -- PAPER 1",
            font_size=11,
            color="#2A2A2A",
        ).move_to(header_bar.get_center())
        
        
        #Student
        Akinyi = StudentCreature("Akinyi").move_to(RIGHT * 5 + DOWN * 1.5)
        self.play(FadeIn(Akinyi))
        self.play(Akinyi.blink(), run_time=0.3)

        # Question text on paper
        q_number = Text("1.", font_size=22, color="#1A1A1A").move_to(
            paper.get_corner(UL) + RIGHT * 0.6 + DOWN * 1.0
        )
        q_text = Text(
            "Prove that  1 + 1 = 2",
            font_size=24,
            color="#1A1A1A",
        ).next_to(q_number, RIGHT, buff=0.2)
        q_marks = Text("(4 marks)", font_size=18, color="#555555").next_to(
            q_text, RIGHT, buff=1.25
        )

        paper_group = VGroup(paper, header_bar, exam_title, q_number, q_text, q_marks)

        self.play(FadeIn(paper, shift=UP * 0.4), run_time=0.9)
        self.play(FadeIn(header_bar), FadeIn(exam_title), run_time=0.5)
        self.play(
            Write(q_number),
            Write(q_text),
            Write(q_marks),
            run_time=1.4,
        )
        self.wait(0.5)

        self.play(Akinyi.look_at(q_text))

        self.play(Akinyi.be_thinking(), Akinyi.blink(), run_time=0.25)

        self.play(Akinyi.think("alaa..?"), side=1, hold_time=1.5)
        self.wait(1.3)
        self.play(
            Akinyi.stop_thinking(), run_time=0.3
        )
        self.play(Akinyi.think("mtego"), side=1, hold_time=1.5)
        self.wait(1.3)
        self.play(
            Akinyi.stop_thinking(), run_time=0.3
        )
        self.wait(1.3)
        student_raises_hand(self, Akinyi, run_time=0.6)
        self.play(Akinyi.think("nani hajui"), side=1, hold_time=1.5)
        self.play(Akinyi.blink(), run_time=0.25)
        self.wait(1.3)
        self.play(
            Akinyi.stop_thinking(), run_time=0.3
        )
        self.wait(1.3)
        self.play(FadeOut(paper_group), FadeOut(Akinyi), run_time=1.0)


         # ──THE QUESTION
        
        vtitle = styled_text(
            "Unaweza Prove That  1 + 1 = 2?",
            size=32,
            color=OFFWHITE,
        )

        self.play(Write(vtitle), run_time=1.6)
        self.wait(0.6)
        self.play(FadeOut(vtitle), run_time=0.8)

        

        # SCENE 2 – THE CHALLENGE

class Scene2(Scene):  #the challenge
    """
    Two 'chungwas' (labelled circles) combine then we show
    that observation ≠ proof.
    """

    def construct(self):
        # oranges (circles with label)
        def make_orange(label_text: str) -> VGroup:
            body = Circle(radius=0.55, fill_color=ORANGE, fill_opacity=1, stroke_width=0)
            stem = Line(
                start=body.get_top(),
                end=body.get_top() + UP * 0.3 + RIGHT * 0.12,
                stroke_color=SUCCESS,
                stroke_width=3,
            )
            leaf = Ellipse(
                width=0.28,
                height=0.14,
                fill_color=SUCCESS,
                fill_opacity=1,
                stroke_width=0,
            ).move_to(stem.get_end() + LEFT * 0.08)
            lbl = Text(label_text, font_size=20, color=OFFWHITE).move_to(body.get_center())
            return VGroup(body, stem, leaf, lbl)
        
        teacher = TeacherCreature().move_to(LEFT * 5 + DOWN * 1.5) #teacher on the left
        Akinyi = StudentCreature("curious").move_to(RIGHT * 4.2 + DOWN * 1.9) #Akinyi on the right
        Kamau = StudentCreature("calm").next_to(Akinyi, RIGHT, buff=0.2) #Kamau on the right of Akinyi
        students = VGroup(Akinyi, Kamau)

        orange1 = make_orange("🍊").shift(LEFT * 3)
        orange2 = make_orange("🍊").shift(RIGHT * 3)

        self.play(FadeIn(teacher), FadeIn(students), run_time=0.8)
        self.play(Akinyi.look_at(teacher), Kamau.look_at(teacher), teacher.look_at_student(Akinyi), run_time=0.5)
        
        self.wait(1.3)

        heading = styled_text("tuhesabu machungwa..", size=30, color=OFFWHITE).to_edge(UP, buff=1.1)
        

        self.play(Write(heading), run_time=0.8)
        self.play(teacher.blink(), run_time=0.3)
        self.wait(0.8)

        self.play(Kamau.blink(), run_time=0.5)

        self.play(FadeIn(orange1, shift=RIGHT * 0.4), run_time=0.7)
        self.play(Akinyi.blink(), run_time=0.3)
        self.wait(0.4)
        self.play(teacher.point_to(orange1), Akinyi.look_at(orange1), Kamau.look_at(orange1), run_time=0.6) #point at orange 1 & students look at it
        self.wait(0.3)
        self.play(Kamau.blink(), run_time=0.5)

        self.play(FadeIn(orange2, shift=LEFT * 0.4), run_time=0.7)
        self.wait(0.4)
        self.play(teacher.blink(), run_time=0.3)
        self.play(teacher.point_to(orange2), Akinyi.look_at(orange2), Kamau.look_at(orange2), run_time=0.6) #point at orange 2 & students look at it

        # ── combine ──
        plus_sign = styled_math("+", size=60, color=WHITE)
        self.play(FadeIn(plus_sign), run_time=0.4)
        self.play(Akinyi.blink(), run_time=0.5)

        result_oranges = VGroup(
            orange1, orange2,
        )

        self.play(
            orange1.animate.shift(RIGHT * 2.0),
            orange2.animate.shift(LEFT * 2.0),
            FadeOut(plus_sign),
            Akinyi.look_at(teacher),
            Kamau.look_at(teacher),
            run_time=1.0,
        )
        self.wait(0.3)
        self.play(teacher.blink(), run_time=0.5)

        count = styled_text("= 2 oranges", size=36, color=ACCENT).shift(DOWN * 1.5)

        box_oranges = SurroundingRectangle(result_oranges, color=ORANGE, buff=0.2, stroke_width=2)
        student_raises_hand(self, Akinyi, run_time=0.6)
        self.play(Create(box_oranges), Akinyi.think("2"), side=1, run_time=0.8)
        self.play(Kamau.blink(), run_time=0.3)
        self.play(Write(count), Akinyi.stop_thinking(), Akinyi.lower_hand(), run_time=0.9)
        self.play(teacher.look_at(count), Akinyi.look_at(count), Kamau.look_at(count), run_time=0.5)
        self.wait(0.7)

        self.play(
            FadeOut(orange1),
            FadeOut(orange2),
            FadeOut(count),
            FadeOut(heading),
            FadeOut(teacher),
            FadeOut(students),
            FadeOut(box_oranges),
            run_time=1.2,
        )

        # ── observation ≠ proof ──
        obs = styled_text("Observation", size=28, color=OFFWHITE)
        self.play(FadeIn(obs), run_time=0.7)
        self.wait(0.5)

        neq_line = MathTex(
            r"\text{Observation} \;\neq\; \text{Proof}",
            font_size=48,
        ).set_color_by_tex("Observation", OFFWHITE).set_color_by_tex("Proof", OFFWHITE)
        
        self.play(ReplacementTransform(obs, neq_line), run_time=1.0)


        box = SurroundingRectangle(neq_line, color=WARNING, buff=0.2, stroke_width=2)
        self.play(Create(box), run_time=0.8)
        self.wait(1.4)

        self.play(FadeOut(VGroup(neq_line, box)), run_time=0.8)


# ─────────────────────────────────────────────
# SCENE 3 – WHY PROOFS EXIST
# ─────────────────────────────────────────────

class Scene3(Scene):
    """
    A layered block tower, built bottom-to-top, illustrates
    how mathematics is constructed on rigorous foundations.
    """

    TOWER_LAYERS = [
        ("Definitions", PRIMARY, True),
        ("Axioms", PRIMARY, True),
        ("Proofs", PRIMARY, True),
        ("Algebra", OFFWHITE, False),
        ("Calculus", OFFWHITE, False),
        ("Physics", OFFWHITE, False),
        ("Engineering", OFFWHITE, False),
        ("AI", ACCENT, False),
    ]

    def construct(self):

        heading = styled_text(
            "Mathematics is built like a tower",
            size=30,
            color=OFFWHITE,
        ).to_edge(UP, buff=1)

        self.play(Write(heading), run_time=0.8)

        block_w = 3.4
        block_h = 0.52
        gap = 0.06

        total = len(self.TOWER_LAYERS)
        start_y = -total * (block_h + gap) / 2 + 0.3

        blocks = []

        for i, (text, color, foundation) in enumerate(self.TOWER_LAYERS):

            rect = Rectangle(
                width=block_w - i * 0.18,
                height=block_h,
                fill_color=color,
                fill_opacity=0.30 if foundation else 0.18,
                stroke_color=color,
                stroke_width=1.6,
            )

            rect.move_to(UP * (start_y + i * (block_h + gap)))

            label = Text(
                text,
                font_size=20,
                color=WHITE if foundation else color,
            ).move_to(rect)

            block = VGroup(rect, label)
            blocks.append(block)

        # Build tower
        for block in blocks:
            self.play(
                FadeIn(block, shift=UP * 0.15),
                run_time=0.32,
            )

        foundation = VGroup(*blocks[:3])
        upper = VGroup(*blocks[3:])

        highlight = SurroundingRectangle(
            foundation,
            color=PRIMARY,
            buff=0.12,
            stroke_width=2.5,
        )

        foundation_label = styled_text(
            "Foundation",
            size=22,
            color=PRIMARY,
        ).next_to(highlight, LEFT)

        self.play(
            Create(highlight),
            FadeIn(foundation_label),
            run_time=0.8,
        )

        caption = styled_text(
            "Ukitoa foundation → the tower collapses",
            size=24,
            color=WARNING,
        ).to_edge(DOWN)

        self.play(FadeIn(caption))
        self.wait(0.5)


        # REMOVE FOUNDATION

        self.play(
            FadeOut(foundation),
            FadeOut(highlight),
            FadeOut(foundation_label),
            run_time=0.45,
        )

        # SMALL WOBBLE
  
        pivot = blocks[3].get_corner(DL)

        self.play(
            Rotate(
                upper,
                angle=4 * DEGREES,
                about_point=pivot,
                rate_func=smooth,
            ),
            run_time=0.12,
        )

        self.play(
            Rotate(
                upper,
                angle=-8 * DEGREES,
                about_point=pivot,
                rate_func=smooth,
            ),
            run_time=0.18,
        )

        self.play(
            Rotate(
                upper,
                angle=4 * DEGREES,
                about_point=pivot,
                rate_func=smooth,
            ),
            run_time=0.10,
        )

        # BLOCKS SCATTER AFTER IMPACT

        scatter = [
            blocks[3].animate.shift(LEFT * 0.3 + DOWN * 0.2).rotate(-8 * DEGREES),
            blocks[4].animate.shift(RIGHT * 0.2 + DOWN * 0.15).rotate(6 * DEGREES),
            blocks[5].animate.shift(RIGHT * 0.7 + DOWN * 0.25).rotate(-12 * DEGREES),
            blocks[6].animate.shift(RIGHT * 1.2).rotate(10 * DEGREES),
            blocks[7].animate.shift(RIGHT * 1.8 + DOWN * 0.4).rotate(-18 * DEGREES),
        ]

        self.play(
            *scatter,
            run_time=0.45,
        )

        self.wait(1)

        self.play(
            FadeOut(
                VGroup(
                    upper,
                    heading,
                    caption,
                )
            ),
            run_time=0.8,
        )


# ─────────────────────────────────────────────
# SCENE 4 – BUILDING NUMBERS FROM SCRATCH
# ─────────────────────────────────────────────

class Scene4(Scene):
    """
    Building numbers from scratch.
    Part 1.
    """

    def construct(self):

        # --------------------------------------------------------
        # question
        # --------------------------------------------------------

        heading = styled_text(
            "What even is '1'?",
            size=36,
            color=OFFWHITE,
        ).to_edge(UP, buff=0.8)

        self.play(Write(heading), run_time=1)
        self.wait(0.6)

        subtitle = styled_text(
            "Before defining 1,\nwe need somewhere to begin",
            size=26,
            color=GREY_B,
        )

        self.play(FadeIn(subtitle, shift=UP*0.2))
        self.wait(2)

        self.play(FadeOut(subtitle))

        # --------------------------------------------------------
        # Reveal zero
        # --------------------------------------------------------

        zero = styled_math(
            "0",
            size=72,
            color=ACCENT,
        )

        self.play(
            GrowFromCenter(zero),
            run_time=1.2,
        )

        self.wait(0.5)

        meaning = styled_text(
            "The starting point",
            size=24,
            color=GREY_A,
        ).next_to(zero, DOWN, buff=0.5)

        self.play(
            FadeIn(meaning),
            run_time=0.7,
        )

        self.wait(2)

        self.play(
            FadeOut(meaning),
        )

        # --------------------------------------------------------
        # Shift left
        # --------------------------------------------------------

        self.play(
            zero.animate.shift(LEFT*4),
            run_time=1,
        )

        # --------------------------------------------------------
        # First successor
        # --------------------------------------------------------

        successor = MathTex(
            r"S(0)",
            font_size=58,
            color=PRIMARY,
        ).move_to(LEFT)

        arrow = Arrow(
            zero.get_right()+RIGHT*0.15,
            successor.get_left()+LEFT*0.15,
            color=PRIMARY,
            buff=0.05,
        )

        self.play(Create(arrow))

        # glowing successor particle

        dot = Dot(radius=0.07, color=YELLOW).move_to(arrow.get_start())

        self.add(dot)

        self.play(MoveAlongPath(dot, arrow), run_time=0.7, rate_func=linear)

        self.remove(dot)

        self.play(Write(successor), run_time=0.6)
        self.wait(1)

        # --------------------------------------------------------
        # Transformation
        # --------------------------------------------------------

        one = styled_math("1", size=72, color=OFFWHITE).move_to(successor)

        self.play(
            ReplacementTransform(successor, one),
            FadeOut(arrow),
            run_time=1,
        )

        self.wait(1.5)


        # --------------------------------------------------------
        # Build the number line by repeatedly applying successor  [part 2]
        # --------------------------------------------------------

        numbers = [zero, one]

        current_number = one
        current_value = 1

        spacing = 2.0

        for next_value in [2, 3, 4]:

            # Successor notation
            succ = MathTex(rf"S({current_value})", font_size=58, color=PRIMARY
                           ).move_to(current_number.get_center() + RIGHT * spacing)

            arrow = Arrow(
                current_number.get_right() + RIGHT * 0.15,
                succ.get_left() + LEFT * 0.15,
                buff=0.05,
                color=PRIMARY,
                stroke_width=2.5,
            )

            self.play(Create(arrow), run_time=0.35)

            # Glowing successor particle
            particle = Dot(radius=0.07, color=YELLOW).move_to(arrow.get_start())

            self.add(particle)

            self.play(MoveAlongPath(particle, arrow), rate_func=linear, run_time=0.55)
            self.remove(particle)

            self.play(Write(succ), run_time=0.45)

            self.wait(0.2)

            # Transform S(n) into the next number

            next_num = styled_math(
                str(next_value),
                size=72,
                color=OFFWHITE,
            ).move_to(succ)

            self.play(
                ReplacementTransform(succ, next_num),
                FadeOut(arrow),
                run_time=0.8,
            )

            numbers.append(next_num)

            current_number = next_num
            current_value = next_value

            self.wait(0.25)

        # --------------------------------------------------------
        # Continue forever...
        # --------------------------------------------------------

        dots = MathTex(r"\cdots", font_size=60, color=GREY_B).next_to(
            numbers[-1],
            RIGHT,
            buff=1
        )
        self.play(FadeIn(dots), run_time=0.8)
        self.wait(1)

        explanation = styled_text(
            "Every natural number\ncomes from repeatedly\napplying the successor operation",
            size=24,
            color=GREY_A,
        ).to_edge(DOWN)

        self.play(FadeIn(explanation, shift=UP * 0.2), run_time=1)

        self.wait(2)

        self.play(FadeOut(explanation))

        # Part 3

        # Every number has a hidden identity
        # --------------------------------------------------------

        self.wait(0.5)

        hidden = [
            MathTex(r"0", font_size=42, color=PRIMARY),
            MathTex(r"S(0)", font_size=40, color=PRIMARY),
            MathTex(r"S(S(0))", font_size=38, color=PRIMARY),
            MathTex(r"S(S(S(0)))", font_size=36, color=PRIMARY),
            MathTex(r"S(S(S(S(0))))", font_size=34, color=PRIMARY)
        ]

        for expr, num in zip(hidden, numbers):
            expr.next_to(num, UP, buff=0.45)

        reveal = styled_text(
            "Repeated successors",
            size=24,
            color=PRIMARY,
        ).to_edge(DOWN)

        self.play(FadeIn(reveal, shift=UP * 0.2))

        # reveal each expression one by one

        for expr in hidden:
            self.play(
                FadeIn(expr, shift=UP * 0.15),
                run_time=0.5,
            )
            self.wait(0.2)

        self.wait(1)

        flashes = []

        for expr in hidden:
            flashes.append(
                Indicate(
                    expr,
                    color=ACCENT,
                    scale_factor=1.15,
                )
            )

        self.play(
            LaggedStart(*flashes, lag_ratio=0.15), run_time=1.5)

        self.play(
            LaggedStart(
                *[
                    FadeOut(expr, shift=DOWN * 0.15)
                    for expr in hidden
                ],
                lag_ratio=0.08,
            ),
            run_time=1,
        )

        self.play(FadeOut(reveal), run_time=0.5)

        # --------------------------------------------------------
        # The Peano axiom
        # --------------------------------------------------------

        s = MathTex("S(n)", font_size=42, color=ACCENT)
        eq = MathTex("=", font_size=42, color=OFFWHITE)
        rhs = MathTex("n+1", font_size=42, color=ACCENT)

        equation = VGroup(s, eq, rhs)
        equation.arrange(RIGHT, buff=0.25)
        equation.to_edge(DOWN, buff=1.0)

        box = SurroundingRectangle(
            equation,
            color=ACCENT,
            buff=0.25,
        )

        title = styled_text(
            "Peano's Successor Axiom",
            size=24,
            color=GREY_A,
        ).next_to(equation, UP, buff=0.4)

        self.play(Write(title))

        self.play(Write(s))
        self.wait(0.2)

        self.play(Write(eq))
        self.wait(0.2)

        self.play(Write(rhs))

        self.play(Create(box))

        self.wait(2)

        highlight = SurroundingRectangle(
            VGroup(*numbers),
            color=PRIMARY,
            buff=0.2,
        )

        self.play(Create(highlight))

        caption = styled_text(
            "Every natural number\nis generated from zero",
            size=22,
            color=PRIMARY,
        ).next_to(highlight, DOWN, buff=0.45)

        self.play(FadeIn(caption))

        self.wait(2)

        self.play(
            FadeOut(
                VGroup(title, one, equation, box, highlight, caption, dots, zero, numbers[2], numbers[3], numbers[4])),
            run_time=1,
        )

        next_question = styled_text(
            "We've built the numbers\nBut hatujadefine addition bado",
            size=34,
            color=OFFWHITE,
        )

        self.play(
            FadeIn(next_question, shift=UP * 0.3),
            run_time=1.2,
        )

        self.wait(2)

# ─────────────────────────────────────────────
# SCENE 5 – DEFINING ADDITION
# ─────────────────────────────────────────────

class Scene5(Scene):
    """
    The proof begins.
    """

    def construct(self):

        heading = styled_text(
            "Proving that 1 + 1 = 2", size=30, color=OFFWHITE).to_edge(UP)

        self.play(Write(heading))
        self.wait(0.4)

        # ---------------------------------------------------------
        # Challenge the viewer
        # ---------------------------------------------------------

        assumption = VGroup(
            styled_text(
                "Hatuta-assume", size=28, color=WARNING),

            MathTex("1+1=2", font_size=60, color=OFFWHITE),
        ).arrange(DOWN, buff=.4)

        self.play(FadeIn(assumption, shift=UP*.3), run_time=1)

        self.wait(1.6)

        prove = styled_text(
            "We're going to prove it", size=30, color=SUCCESS).next_to( assumption, DOWN, buff=.7)

        self.play(FadeIn(prove),run_time=.8)

        self.wait(2)

        self.play(FadeOut(VGroup(assumption, prove)))

        # ---------------------------------------------------------
        # Proof title
        # ---------------------------------------------------------

        proof = Text("Proof", font_size=34, weight=BOLD, color=PRIMARY)

        proof.to_edge(LEFT, buff=.8)
        proof.to_edge(UP, buff=1.8)

        underline = Line(
            proof.get_left(),
            proof.get_right(),
            color=PRIMARY,
            stroke_width=2,
        ).next_to( proof, DOWN, buff=.08)

        self.play(Write(proof), Create(underline))
        # left margin

        x = -3.5

        line1 = MathTex("1","+","1", font_size=60)
        line1.move_to(np.array([x,.8,0]))
        self.play(Write(line1))

        self.wait(.8)

        reason_title = styled_text("Reason", size=22, color=PRIMARY)
        reason_line = Line(LEFT*.8, RIGHT*.8, color=PRIMARY)
        reason = styled_text("Definition of 1", size=20, color=DIMGRAY)
        reason_group = VGroup(reason_title, reason_line, reason)
        reason_group.arrange(DOWN, buff=.15)
        reason_group.to_corner(UR, buff=.6)
        self.play(FadeIn(reason_group))


        # ==========================================================
        # PROOF STEP 1
        # 1 + 1
        # = 1 + S(0)
        # ==========================================================

        # Update reason panel
        new_reason = styled_text(
            "Definition of 1\n(1 := S(0))",
            size=20,
            color=DIMGRAY,
        ).move_to(reason)

        self.play(Transform(reason, new_reason),run_time=0.5)

        # New proof line
        line2 = MathTex("=", "1", "+", "S(0)", font_size=60)

        line2.next_to(line1, DOWN, aligned_edge=LEFT, buff=0.45)

        # First reveal the equals sign
        self.play(FadeIn(line2[0], shift=RIGHT * 0.2), run_time=0.3)

        # Highlight the second "1" in the previous line
        highlight = SurroundingRectangle(line1[2], color=ACCENT, buff=0.08)

        self.play(Create(highlight), run_time=0.4)

        # Copy the first "1"
        first_one = line1[0].copy()

        self.play(TransformFromCopy(first_one, line2[1]), run_time=0.5)

        # Copy the plus sign
        plus = line1[1].copy()

        self.play( TransformFromCopy(plus, line2[2]), run_time=0.35)

        # Transform the SECOND 1 into S(0)
        self.play(
            ReplacementTransform(line1[2].copy(), line2[3]),
            FadeOut(highlight),
            run_time=0.9,
        )

        self.wait(1)


        # ==========================================================
        # PROOF STEP 2
        #
        # = S(1+0)
        # ==========================================================

        new_reason = styled_text(
            "Addition axiom\n"
            "a + S(b) = S(a+b)",
            size=20,
            color=DIMGRAY,
        ).move_to(reason)

        self.play(Transform(reason, new_reason), run_time=0.5)

        line3 = MathTex("=", "S(", "1", "+", "0", ")", font_size=60)

        line3.next_to( line2, DOWN, aligned_edge=LEFT, buff=0.45)

        self.play(FadeIn(line3[0]), run_time=0.3)

        # Highlight the expression being rewritten
        rewrite_box = SurroundingRectangle(VGroup(line2[1], line2[2], line2[3]),
            color=PRIMARY,
            buff=0.08
        )

        self.play(Create(rewrite_box))

        self.play(
            FadeIn(line3[1]),
            TransformFromCopy(line2[1], line3[2]),
            TransformFromCopy(line2[2], line3[3]),
            FadeIn(line3[4]),
            FadeIn(line3[5]),
            FadeOut(rewrite_box),
            run_time=1.3,
        )

        self.wait(1)

        # ==========================================================
        # PROOF STEP 3
        #
        # = S(1)
        # ==========================================================

        new_reason = styled_text("Identity axiom\n" "a + 0 = a", size=20, color=DIMGRAY).move_to(reason)

        self.play(Transform(reason, new_reason))

        line4 = MathTex("=", "S(", "1", ")", font_size=60)

        line4.next_to(line3, DOWN, aligned_edge=LEFT, buff=0.45)

        self.play(FadeIn(line4[0]),run_time=0.3)

        target = SurroundingRectangle(VGroup(line3[2], line3[3], line3[4]),
            color=ACCENT,
            buff=0.08
        )

        self.play(Create(target))

        self.play(TransformFromCopy( line3[1], line4[1]), TransformFromCopy(line3[2], line4[2]),TransformFromCopy(line3[5],line4[3]),
            FadeOut(target), run_time=1.0
                )

        self.wait(1)

        # ==========================================================
        # PROOF STEP 4
        #
        # = 2
        # ==========================================================

        new_reason = styled_text("Definition of 2\n(2 := S(1))", size=20, color=DIMGRAY).move_to(reason)

        self.play( Transform(reason, new_reason), run_time=0.5)

        line5 = MathTex("=", "2", font_size=60, color=SUCCESS)

        line5.next_to(line4, DOWN, aligned_edge=LEFT, buff=0.45)

        self.play(FadeIn(line5[0]),run_time=0.25)

        # Highlight S(1)

        final_box = SurroundingRectangle(VGroup(line4[1], line4[2], line4[3]), color=SUCCESS, buff=0.08)

        self.play(Create(final_box), run_time=0.45)

        self.wait(0.3)

        self.play(
            ReplacementTransform(VGroup(line4[1], line4[2], line4[3]).copy(), line5[1]),
            FadeOut(final_box),
            run_time=1.0
        )

        self.wait(1)

        proof_box = SurroundingRectangle(VGroup(line1, line2, line3, line4, line5), color=PRIMARY, buff=0.25)

        self.play(Create(proof_box), run_time=.8)

        self.wait(.8)
        self.play(FadeOut(line2), FadeOut(line3), FadeOut(line4), FadeOut(reason_group), FadeOut(proof_box), run_time=.8)

        self.play(line1.animate.move_to(UP*.6), line5.animate.move_to(DOWN*.2), run_time=1)

        theorem = MathTex("1", "+", "1", "=", "2", font_size=90)

        theorem.set_color_by_tex("2", SUCCESS)
        theorem.move_to(ORIGIN)

        self.play(ReplacementTransform(VGroup(line1.copy(), line5.copy()),
                theorem),
                FadeOut(heading),
                run_time=1.4
        )

        glow = SurroundingRectangle( theorem, color=SUCCESS, buff=.35, corner_radius=.18)

        self.play(Create(glow),run_time=.5)

        self.play( glow.animate.scale(1.08).set_stroke(width=6), rate_func=there_and_back, run_time=.8)

        self.play(glow.animate.scale(1.05).set_stroke(width=4), rate_func=there_and_back, run_time=.8)

        qed = MathTex(r"\blacksquare", font_size=42, color=PRIMARY)

        qed.next_to(theorem, RIGHT, buff=0.45)
        self.play(DrawBorderThenFill(qed), run_time=0.7)

        conclusion = styled_text("Not assumed.\nProven from the axioms.", size=24, color=DIMGRAY)
        conclusion.next_to(theorem, DOWN, buff=0.7)
        self.play(FadeIn(conclusion, shift=UP*0.15))

        self.wait(2.5)

        
# ─────────────────────────────────────────────
# SCENE 6 – THE SURPRISING TRUTH / HISTORY
# ─────────────────────────────────────────────

class Scene6(Scene):
    """
    A stack of 'books' builds up with timeline markers,
    conveying how long formalising foundations took.
    """

    BOOKS = [
        ("Euclid's Elements",      "~300 BC",  "#4A90D9"),
        ("Leibniz & Newton",       "1660s",    "#7B5EA7"),
        ("Boole's Logic",          "1847",     "#3E8E6A"),
        ("Frege's Begriffschrift", "1879",     "#C0832E"),
        ("Peano Axioms",           "1889",     PRIMARY),
        ("Principia Mathematica",  "1910",     WARNING),
    ]

    def construct(self):

        heading = styled_text(
            "mathematicians wali spend centuries on this",
            size=30,
            color=OFFWHITE,
        ).to_edge(UP, buff=1.0)
        self.play(Write(heading), run_time=0.9)

        spine_w, spine_h = 2.6, 0.55
        gap = 0.06
        total = len(self.BOOKS)
        base_y = -(total * (spine_h + gap)) / 2 + 0.25

        book_mobs = []
        for i, (title, year, color) in enumerate(self.BOOKS):
            spine = Rectangle(
                width=spine_w,
                height=spine_h,
                fill_color=color,
                fill_opacity=0.22,
                stroke_color=color,
                stroke_width=1.8,
            ).move_to(LEFT * 1.0 + UP * (base_y + i * (spine_h + gap)))

            title_txt = Text(title, font_size=16, color=OFFWHITE).move_to(
                spine.get_center() + LEFT * 0.2
            )
            year_txt = Text(year, font_size=15, color=color).next_to(spine, RIGHT, buff=0.25)
            tick = Line(
                start=year_txt.get_left() + LEFT * 0.08,
                end=year_txt.get_left() + LEFT * 0.25,
                stroke_color=color,
                stroke_width=1.5,
            )
            book = VGroup(spine, title_txt, year_txt, tick)
            book_mobs.append(book)

        # Stagger in bottom-to-top
        for book in book_mobs:
            self.play(FadeIn(book, shift=UP * 0.18), run_time=0.45)

        self.wait(0.5)

        # ── "Rigorous Foundations" callout ──
        callout = styled_text(
            "Rigorous Foundations",
            size=32,
            color=ACCENT,
        ).shift(RIGHT * 3.8)
        callout_line = Line(
            start=book_mobs[-1][0].get_right() + RIGHT * 0.1,
            end=callout.get_left() + LEFT * 0.15,
            stroke_color=ACCENT,
            stroke_width=1.5,
        )

        self.play(Create(callout_line), FadeIn(callout, shift=LEFT * 0.3), run_time=1.0)
        self.wait(0.5)

        pm_note = styled_text(
            "Principia Mathematica took 362 pages\nto prove  1 + 1 = 2.",
            size=22,
            color=WARNING,
        ).shift(DOWN * 2.8)
        self.play(FadeIn(pm_note, shift=UP * 0.2), run_time=0.9)
        self.wait(1.6)

        #self.play(FadeOut(VGroup(*self.mobjects)), run_time=1.0)


# ─────────────────────────────────────────────
# SCENE 7 – SHIELDLAB ENDING
# ─────────────────────────────────────────────

class Scene7(Scene):
    """
    Cinematic closing:  philosophical statement → 1 + 1 = 2
    → ShieldLab brand card fades in.
    """

    def construct(self):
        # ── philosophical statement ──
        statement = Text(
            "Mathematics refuses to take\neven this for granted",
            font_size=38,
            color=OFFWHITE,
            line_spacing=1.4,
        ).shift(UP * 0.6)

        self.play(FadeIn(statement, shift=DOWN * 0.4), run_time=1.4)
        self.wait(1.8)

        # ── 1 + 1 = 2, large and centered ──
        equation = MathTex("1 + 1 = 2", font_size=108, color=SUCCESS)
        self.play(
            statement.animate.shift(UP * 1.4).set_opacity(0.25),
            FadeIn(equation, scale=0.7),
            run_time=1.3,
        )

        glow = SurroundingRectangle(
            equation,
            color=SUCCESS,
            buff=0.4,
            stroke_width=2.2,
            corner_radius=0.25,
        )
        self.play(Create(glow), run_time=0.8)
        self.wait(0.8)

        # ── fade everything out ──
        self.play(
            FadeOut(statement),
            FadeOut(equation),
            FadeOut(glow),
            run_time=1.2,
        )

        # ── ShieldLab brand card ──
        brand_name = Text(
            "ShieldLab",
            font_size=72,
            color=PRIMARY,
        )

        # Decorative underline
        underline = Line(
            start=brand_name.get_left(),
            end=brand_name.get_right(),
            stroke_color=PRIMARY,
            stroke_width=2.5,
        ).next_to(brand_name, DOWN, buff=0.12)


        self.play(FadeIn(brand_name, shift=UP * 0.4), run_time=1.0)
        self.play(Create(underline), run_time=0.5)

        self.wait(2.5)

        # ── final fade to black ──
        self.play(FadeOut(brand_name), run_time=1.6)
        self.wait(0.5)