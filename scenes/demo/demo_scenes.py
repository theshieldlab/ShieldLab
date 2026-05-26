"""
demo_scenes.py
==============
Demo Manim scenes for the Kenyan Shield Creature system.

Run with:
    manim -pql demo_scenes.py DerivativeLessonScene
    manim -pqh demo_scenes.py DerivativeLessonScene
    manim -pql demo_scenes.py CreatureExpressionsDemo
    manim -pql demo_scenes.py EyeSystemDemo
"""

import random
from manim import *
from Shield_Creatures import (
    TeacherCreature, StudentCreature, CreatureScene,
    create_classroom, all_look_at_equation, all_look_at_teacher,
    students_confused, teacher_teaches, student_raises_hand,
    teacher_points_to, blink_staggered, classroom_idle_blinks,
    SHIELD_BLACK, SHIELD_WHITE, TEACHER_COLOR,
    STUDENT_BLUE, STUDENT_GREEN, STUDENT_YELLOW,
)


# ─────────────────────────────────────────────
# SCENE 1: Full Classroom — Derivative Lesson
# ─────────────────────────────────────────────
class DerivativeLessonScene(CreatureScene):
    """
    Full classroom scene:
    - Fully dark background, no ground line
    - Teacher (terracotta) left with pointing stick
    - Three students (blue, green, yellow) right
    - Equations upper right
    - Blinks are random, 10-15s apart, never simultaneous
    """

    def construct(self):
        # ── Full-screen dark background guarantee ──
        bg = Rectangle(
            width=config.frame_width + 1,
            height=config.frame_height + 1,
            fill_color="#111111",
            fill_opacity=1,
            stroke_width=0,
        )
        self.add(bg)

        # ── Equations ──
        equations = VGroup(
            MathTex(r"\frac{d}{dx} \sin x = \cos x"),
            MathTex(r"\frac{d}{dx} e^x = e^x"),
            MathTex(r"\frac{d}{dx} \ln x = \frac{1}{x}"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        equations.scale(1.05).move_to(UP * 1.3 + RIGHT * 2.5)

        # ── Creatures — spread to fill full wide frame ──
        teacher, students = create_classroom()
        blue, green, yellow = students

        teacher.move_to(LEFT * 5.5 + DOWN * 1.2)
        blue.move_to(RIGHT * 0.5 + DOWN * 1.5)
        green.move_to(RIGHT * 2.6 + DOWN * 1.5)
        yellow.move_to(RIGHT * 4.7 + DOWN * 1.5)

        teacher.save_pose()
        for s in students:
            s.save_pose()

        # ── Fade in ──
        self.play(
            FadeIn(teacher, shift=UP * 0.3),
            LaggedStart(
                FadeIn(blue,   shift=UP * 0.3),
                FadeIn(green,  shift=UP * 0.3),
                FadeIn(yellow, shift=UP * 0.3),
                lag_ratio=0.2,
            ),
            run_time=1.2,
        )
        self.wait(0.3)

        # ── Write equations ──
        self.play(Write(equations), run_time=2.2)

        # ── Teacher points to equation 1 ──
        self.play(teacher.look_at(equations), run_time=0.5)
        self.play(teacher.point_to(equations[0]), run_time=0.8)

        # ── Students look at equations ──
        self.play(
            blue.look_at(equations),
            green.look_at(equations),
            yellow.look_at(equations),
            run_time=0.7,
        )
        self.wait(0.8)

        # ── Random blink: teacher — 10-15s gap ──
        self.wait(random.uniform(10.0, 15.0))
        self.play(teacher.blink(), run_time=0.25)

        # ── Teacher moves pointer to equation 2 ──
        self.play(teacher.point_to(equations[1]), run_time=0.7)
        self.play(teacher.explain(), run_time=0.5)

        # ── Blue excited ──
        self.play(blue.be_excited(), run_time=0.6)

        # ── Yellow confused ──
        self.play(yellow.be_confused(), run_time=0.5)

        # ── Yellow raises hand ──
        student_raises_hand(self, yellow, run_time=0.6)

        # ── Teacher looks at yellow ──
        self.play(teacher.look_at_student(yellow), run_time=0.5)

        # ── Random blink: blue — 10-15s gap ──
        self.wait(random.uniform(10.0, 15.0))
        self.play(blue.blink(), run_time=0.25)

        # ── Teacher points to equation 3 ──
        self.play(teacher.point_to(equations[2]), run_time=0.8)
        all_look_at_equation(self, teacher, students, equations[2])

        # ── Green thinking ──
        self.play(green.be_thinking(), run_time=0.7)
        self.play(green.thinking_pose(), run_time=0.5)

        # ── Random blink: green — 10-15s gap ──
        self.wait(random.uniform(10.0, 15.0))
        self.play(green.blink(), run_time=0.25)

        self.wait(0.5)

        # ── Students glance at each other ──
        self.play(blue.glance_at(yellow), run_time=0.4)
        self.play(yellow.glance_at(blue), run_time=0.4)

        # ── Random blink: yellow — 10-15s gap ──
        self.wait(random.uniform(10.0, 15.0))
        self.play(yellow.blink(), run_time=0.25)

        self.wait(0.5)

        # ── All look at teacher ──
        all_look_at_teacher(self, teacher, students)

        self.wait(1.0)


# ─────────────────────────────────────────────
# SCENE 2: Eye System Demo
# ─────────────────────────────────────────────
class EyeSystemDemo(CreatureScene):
    """Demonstrates all eye movement and blink states."""

    def construct(self):
        teacher = TeacherCreature().move_to(ORIGIN)
        self.play(FadeIn(teacher))
        self.wait(0.3)

        label = Text("look_right()", font="Monospace").scale(0.45).to_edge(UP)
        self.play(Write(label))
        self.play(teacher.look_right())
        self.wait(0.5)

        self.play(Transform(label, Text("look_left()", font="Monospace").scale(0.45).to_edge(UP)))
        self.play(teacher.look_left())
        self.wait(0.5)

        self.play(Transform(label, Text("look_up()", font="Monospace").scale(0.45).to_edge(UP)))
        self.play(teacher.look_up())
        self.wait(0.5)

        self.play(Transform(label, Text("look_down()", font="Monospace").scale(0.45).to_edge(UP)))
        self.play(teacher.look_down())
        self.wait(0.5)

        self.play(Transform(label, Text("thinking_eyes()", font="Monospace").scale(0.45).to_edge(UP)))
        self.play(teacher.thinking_eyes())
        self.wait(0.5)

        self.play(Transform(label, Text("confused_eyes()", font="Monospace").scale(0.45).to_edge(UP)))
        self.play(teacher.confused_eyes())
        self.wait(0.5)

        self.play(Transform(label, Text("cross_eyes()", font="Monospace").scale(0.45).to_edge(UP)))
        self.play(teacher.cross_eyes())
        self.wait(0.5)

        self.play(Transform(label, Text("blink()  x3", font="Monospace").scale(0.45).to_edge(UP)))
        for _ in range(3):
            self.play(teacher.blink())
            self.wait(0.4)

        self.wait(0.5)


# ─────────────────────────────────────────────
# SCENE 3: Emotional States Demo
# ─────────────────────────────────────────────
class CreatureExpressionsDemo(CreatureScene):
    """Shows all emotional states across three students."""

    def construct(self):
        creatures = [
            StudentCreature("curious").shift(LEFT * 4),
            StudentCreature("calm").shift(ORIGIN),
            StudentCreature("energetic").shift(RIGHT * 4),
        ]

        labels = [
            Text("Curious / Blue",    font="Monospace").scale(0.38).next_to(creatures[0], DOWN),
            Text("Calm / Green",      font="Monospace").scale(0.38).next_to(creatures[1], DOWN),
            Text("Energetic / Yellow",font="Monospace").scale(0.38).next_to(creatures[2], DOWN),
        ]

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in creatures], lag_ratio=0.2),
            LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.2),
        )
        self.wait(0.5)

        moods = [
            ("be_attentive",  "be_attentive()"),
            ("be_happy",      "be_happy()"),
            ("be_confused",   "be_confused()"),
            ("be_thinking",   "be_thinking()"),
            ("be_excited",    "be_excited()"),
            ("be_tired",      "be_tired()"),
            ("be_suspicious", "be_suspicious()"),
        ]

        mood_label = Text("", font="Monospace").scale(0.5).to_edge(UP)
        self.add(mood_label)

        for method, name in moods:
            new_label = Text(f"creature.{name}", font="Monospace").scale(0.48).to_edge(UP)
            self.play(
                Transform(mood_label, new_label),
                *[getattr(c, method)() for c in creatures],
                run_time=0.8,
            )
            self.wait(0.7)

        self.wait(0.5)


# ─────────────────────────────────────────────
# SCENE 4: Arm Poses Demo
# ─────────────────────────────────────────────
class ArmPosesDemo(CreatureScene):
    """Demonstrates arm animation methods."""

    def construct(self):
        teacher = TeacherCreature().move_to(LEFT * 3)
        student = StudentCreature("curious").move_to(RIGHT * 2)
        teacher.save_pose()
        student.save_pose()

        self.play(FadeIn(teacher), FadeIn(student))
        self.wait(0.3)

        label = Text("shrug()", font="Monospace").scale(0.42).to_edge(UP)
        self.play(Write(label))
        self.play(teacher.shrug())
        self.wait(0.5)
        self.play(teacher.relax_arms())

        self.play(Transform(label, Text("raise_hand()", font="Monospace").scale(0.42).to_edge(UP)))
        self.play(student.raise_hand())
        self.wait(0.5)
        self.play(student.lower_hand())

        self.play(Transform(label, Text("thinking_pose()", font="Monospace").scale(0.42).to_edge(UP)))
        self.play(teacher.thinking_pose(), teacher.be_thinking())
        self.wait(0.8)
        self.play(teacher.relax_arms())

        self.play(Transform(label, Text("arm_wave()", font="Monospace").scale(0.42).to_edge(UP)))
        self.play(student.arm_wave())
        self.wait(0.5)


# ─────────────────────────────────────────────
# SCENE 5: Creature Intro
# ─────────────────────────────────────────────
class CreatureIntroScene(CreatureScene):
    """Branded intro — reveals each creature with its name."""

    def construct(self):
        title    = Text("Shield Creatures", font="serif").scale(1.1).to_edge(UP, buff=0.4)
        subtitle = Text("Kenyan STEM Mascot System", font="serif").scale(0.48).next_to(title, DOWN)

        self.play(Write(title), FadeIn(subtitle, shift=DOWN * 0.2))
        self.wait(0.5)

        teacher, students = create_classroom()
        teacher.move_to(LEFT * 5.0 + DOWN * 0.5)
        students[0].move_to(LEFT * 1.5 + DOWN * 0.8)
        students[1].move_to(RIGHT * 0.8 + DOWN * 0.8)
        students[2].move_to(RIGHT * 3.0 + DOWN * 0.8)

        t_label = Text("Teacher",    font="serif").scale(0.42).next_to(teacher,     DOWN, buff=0.15)
        s_labels = [
            Text("Curious",   font="serif").scale(0.38).next_to(students[0], DOWN, buff=0.1),
            Text("Calm",      font="serif").scale(0.38).next_to(students[1], DOWN, buff=0.1),
            Text("Energetic", font="serif").scale(0.38).next_to(students[2], DOWN, buff=0.1),
        ]

        self.play(FadeIn(teacher, shift=UP * 0.4), Write(t_label))
        self.play(teacher.look(RIGHT * 0.5))
        self.wait(0.3)
        self.play(teacher.blink())

        for s, lbl in zip(students, s_labels):
            self.play(FadeIn(s, shift=UP * 0.3), Write(lbl), run_time=0.6)
            self.play(s.personality_idle(), run_time=0.5)

        self.wait(0.5)

        self.play(
            *[c.look(UP * 0.5 + RIGHT * 0.3) for c in [teacher] + students],
            run_time=0.8,
        )

        # Staggered blinks — each one a different creature
        for c in [teacher] + students:
            self.play(c.blink(), run_time=0.25)
            self.wait(0.25)

        self.wait(1.0)

class Teacher(Scene):
    def construct(self):
        teacher = TeacherCreature()
        self.play(FadeIn(teacher))