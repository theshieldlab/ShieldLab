import random

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

def scene_title(text: str, **kwargs) -> Text:
    
    """Small, tasteful scene label in the top-left corner."""

    return Text(
        text,
        font_size=18,
        color=DIMGRAY,
        **kwargs,
    ).to_corner(UL, buff=0.35)


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
        # ── label ──
        label = scene_title("Scene 1 · The Intro")
        self.add(label)


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
        self.wait(1.3)
        self.play(
            Akinyi.stop_thinking(), run_time=0.3
        )
        self.wait(1.3)
        self.play(FadeOut(paper_group), FadeOut(label), FadeOut(Akinyi), run_time=1.0)


         # ──THE QUESTION
        
        vtitle = styled_text(
            "Unaweza Prove That  1 + 1 = 2?",
            size=32,
            color=OFFWHITE,
        )

        self.play(Write(vtitle), run_time=1.6)
        self.wait(0.6)
        self.play(FadeOut(vtitle), run_time=0.8)

        

# ─────────────────────────────────────────────
# SCENE 2 – THE CHALLENGE
# ─────────────────────────────────────────────

class Scene2(Scene):  #the challenge
    """
    Two 'apples' (labelled circles) combine then we show
    that observation ≠ proof.
    """

    def construct(self):
        label = scene_title("Scene 2 · Observation ≠ Proof")
        self.add(label)

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

        orange1 = make_orange("🍊").shift(LEFT * 3.5)
        orange2 = make_orange("🍊").shift(RIGHT * 3.5)

        self.play(FadeIn(teacher), run_time=0.8)
        self.wait(1.3)

        heading = styled_text("let us count oranges…", size=30, color=OFFWHITE).to_edge(UP, buff=1.1)

        self.play(Write(heading), run_time=0.8)
        self.play(teacher.blink(), run_time=0.3)
        self.wait(0.8)

        self.play(FadeIn(orange1, shift=RIGHT * 0.4), run_time=0.7)
        self.wait(0.4)
        self.play(teacher.point_to(orange1), run_time=0.6) #point at orange 1
        self.wait(0.3)

        self.play(FadeIn(orange2, shift=LEFT * 0.4), run_time=0.7)
        self.wait(0.4)
        self.play(teacher.blink(), run_time=0.3)
        self.play(teacher.point_to(orange2), run_time=0.6) #point at orange 2

        # ── combine ──
        plus_sign = styled_math("+", size=60, color=OFFWHITE)
        self.play(FadeIn(plus_sign), run_time=0.4)

        result_oranges = VGroup(
            orange1, orange2,
        )

        self.play(
            orange1.animate.shift(RIGHT * 2.0),
            orange2.animate.shift(LEFT * 2.0),
            FadeOut(plus_sign),
            run_time=1.0,
        )
        self.wait(0.3)

        count = styled_text("= 2 oranges", size=36, color=ACCENT).shift(DOWN * 1.5)

        box_oranges = SurroundingRectangle(result_oranges, color=ORANGE, buff=0.2, stroke_width=2)
        self.play(Create(box_oranges), run_time=0.8)
        self.play(teacher.blink(), run_time=0.3)
        self.play(Write(count), run_time=0.9)
        self.play(teacher.look_at(count), run_time=0.5)
        self.wait(0.7)

        self.play(
            FadeOut(orange1),
            FadeOut(orange2),
            FadeOut(count),
            FadeOut(heading),
            FadeOut(teacher),
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

        self.play(FadeOut(VGroup(neq_line, box, label)), run_time=0.8)


# ─────────────────────────────────────────────
# SCENE 3 – WHY PROOFS EXIST
# ─────────────────────────────────────────────

class Scene3(Scene):
    """
    A layered block tower, built bottom-to-top, illustrates
    how mathematics is constructed on rigorous foundations.
    """

    TOWER_LAYERS = [
        ("Definitions",  PRIMARY,  True),
        ("Axioms",       PRIMARY,  True),
        ("Proofs",       PRIMARY,  True),
        ("Algebra",      OFFWHITE, False),
        ("Calculus",     OFFWHITE, False),
        ("Physics",      OFFWHITE, False),
        ("Engineering",  OFFWHITE, False),
        ("AI",           ACCENT,   False),
    ]

    def construct(self):
        label = scene_title("Scene 3 · Why Proofs Exist")
        self.add(label)

        heading = styled_text(
            "Mathematics is built like a tower",
            size=30,
            color=OFFWHITE,
        ).to_edge(UP, buff=1.0)
        self.play(Write(heading), run_time=0.9)

        block_w, block_h, gap = 3.4, 0.52, 0.06
        total = len(self.TOWER_LAYERS)
        start_y = -total * (block_h + gap) / 2 + 0.3

        blocks = []
        for i, (text, color, is_foundation) in enumerate(self.TOWER_LAYERS):
            rect = Rectangle(
                width=block_w - i * 0.18,   #slight taper toward top
                height=block_h,
                fill_color=color,
                fill_opacity=0.18 if not is_foundation else 0.30,
                stroke_color=color,
                stroke_width=1.6,
            )
            rect.move_to(UP * (start_y + i * (block_h + gap)))
            lbl = Text(
                text,
                font_size=20,
                color=color if not is_foundation else WHITE,
            ).move_to(rect.get_center())
            block = VGroup(rect, lbl)
            blocks.append(block)

        # Build bottom-to-top
        for block in blocks:
            self.play(FadeIn(block, shift=UP * 0.15), run_time=0.35)

        self.wait(0.5)

        # ── highlight foundation ──
        foundation_group = VGroup(*blocks[:3])
        highlight = SurroundingRectangle(
            foundation_group,
            color=PRIMARY,
            buff=0.12,
            stroke_width=2.5,
        )
        foundation_label = styled_text(
            "Foundation",
            size=22,
            color=PRIMARY,
        ).next_to(highlight, LEFT, buff=0.25)

        self.play(Create(highlight), FadeIn(foundation_label, shift=RIGHT * 0.2), run_time=0.9)
        self.wait(1.2)

        caption = styled_text(
            "Remove the foundation → the tower collapses.",
            size=24,
            color=WARNING,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.8)
        self.wait(1.4)

        self.play(
            FadeOut(VGroup(*blocks, highlight, foundation_label, caption, heading, label)),
            run_time=1.0,
        )


# ─────────────────────────────────────────────
# SCENE 4 – BUILDING NUMBERS FROM SCRATCH
# ─────────────────────────────────────────────

class Scene4(Scene):
    """
    Introduces the successor concept and grows a number line
    from 0 outward using arrows.
    """

    def construct(self):
        label = scene_title("Scene 4 · Building Numbers")
        self.add(label)

        heading = styled_text("What even is  '1'?", size=34, color=OFFWHITE).to_edge(UP, buff=1.0)
        self.play(Write(heading), run_time=0.9)

        # ── 0 appears ──
        zero = styled_math("0", size=64, color=ACCENT).shift(LEFT * 4.5)
        self.play(FadeIn(zero, scale=0.6), run_time=0.7)

        # ── successor chain: 0 → 1 → 2 → 3 → 4 ──
        nodes = [zero]
        positions = [zero.get_center()]
        for i in range(1, 5):
            pos = LEFT * (4.5 - i * 2.0) + np.array([0, 0, 0])
            num = styled_math(str(i), size=64, color=OFFWHITE if i < 4 else SUCCESS)
            num.move_to(pos)
            arr = Arrow(
                start=positions[-1] + RIGHT * 0.55,
                end=pos + LEFT * 0.55,
                color=PRIMARY,
                buff=0.05,
                stroke_width=2.5,
                tip_length=0.22,
            )
            succ_lbl = Text(
                "S(·)",
                font_size=17,
                color=PRIMARY,
            ).move_to(arr.get_center() + UP * 0.32)

            self.play(
                Create(arr),
                FadeIn(succ_lbl, shift=DOWN * 0.1),
                run_time=0.5,
            )
            self.play(FadeIn(num, scale=0.5), run_time=0.4)
            nodes.append(num)
            positions.append(pos)
            self.wait(0.15)

        self.wait(0.6)

        # ── successor definition box ──
        defn = MathTex(
            r"S(n) = n + 1 \quad \text{(Peano axiom)}",
            font_size=34,
            color=ACCENT,
        ).shift(DOWN * 2.3)
        defn_box = SurroundingRectangle(defn, color=ACCENT, buff=0.2, stroke_width=1.8)

        self.play(Write(defn), Create(defn_box), run_time=1.2)
        self.wait(1.4)



# ─────────────────────────────────────────────
# SCENE 5 – DEFINING ADDITION
# ─────────────────────────────────────────────

class Scene5(Scene):
    """
    Step-by-step transform:  1 + 1  →  S(1)  →  2
    Ends with a glowing highlight on '2'.
    """

    def construct(self):
        label = scene_title("Scene 5 · Defining Addition")
        self.add(label)

        heading = styled_text(
            "Addition via the Successor",
            size=30,
            color=OFFWHITE,
        ).to_edge(UP, buff=1.0)
        self.play(Write(heading), run_time=0.8)

        # Step 1 – original expression
        step1 = MathTex("1", "+", "1", font_size=96)
        step1.set_color_by_tex("1", OFFWHITE)
        step1.set_color_by_tex("+", PRIMARY)

        # Step 2 – successor form
        step2 = MathTex(r"S(1)", font_size=96, color=ACCENT)

        # Step 3 – final result
        step3 = MathTex("2", font_size=128, color=SUCCESS)

        annotation1 = styled_text(
            "Adding 1 means applying the successor once.",
            size=24,
            color=DIMGRAY,
        ).shift(DOWN * 2.0)
        annotation2 = styled_text(
            "By definition:  S(1) is called '2'.",
            size=24,
            color=DIMGRAY,
        ).shift(DOWN * 2.0)

        self.play(Write(step1), run_time=1.0)
        self.play(FadeIn(annotation1, shift=UP * 0.15), run_time=0.6)
        self.wait(0.6)

        # 1 + 1  →  S(1)
        self.play(
            ReplacementTransform(step1, step2),
            ReplacementTransform(annotation1, annotation2),
            run_time=1.2,
        )
        self.wait(0.6)

        # S(1)  →  2
        self.play(
            ReplacementTransform(step2, step3),
            FadeOut(annotation2),
            run_time=1.2,
        )
        self.wait(0.4)

        # ── subtle highlight glow ──
        glow_rect = SurroundingRectangle(
            step3,
            color=SUCCESS,
            buff=0.35,
            stroke_width=2.5,
            corner_radius=0.2,
        )
        self.play(Create(glow_rect), run_time=0.7)
        self.play(glow_rect.animate.set_stroke(opacity=0.3), run_time=0.9)
        self.play(glow_rect.animate.set_stroke(opacity=1.0), run_time=0.9)

        therefore = MathTex(
            r"\therefore \quad 1 + 1 = 2 \quad \blacksquare",
            font_size=42,
            color=ACCENT,
        ).shift(DOWN * 2.2)
        self.play(Write(therefore), run_time=1.1)
        self.wait(1.6)

        #self.play(FadeOut(VGroup(*self.mobjects)), run_time=0.9)


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
        label = scene_title("Scene 6 · A Century of Foundations")
        self.add(label)

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

class Scene7Ending(Scene):
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