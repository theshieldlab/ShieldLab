from email.mime import text
from pyclbr import Class

from manim import *


class intro(Scene):

    def construct(self):
      # --- Intro Scene ---

        title = Text("KCSE Mathematics P1 2025 Section 1", font_size=42)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        #---------- QUESTION 1 ----

class Question1(Scene):
    def construct(self):
        question_number = Text("1.",font_size=30)

        question_text = VGroup(
            Text("Without using mathematical tables or a calculator, evaluate:", font_size=23),
            MathTex(r"\sqrt{\frac{11}{12}-\frac{1}{3}\div1\frac{1}{2}}", font_size=34)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        question_number.next_to(question_text, LEFT, buff=0.25)

        question_block = VGroup(question_number,question_text)
        question_block.to_edge(UL,buff=0.25)

        # Show question
        self.play(
            Write(question_number),
            LaggedStart(
                *[Write(x) for x in question_text],
                lag_ratio=0.15
            )
        )

        self.wait(2)

        # ============================================================
        # STEP 1 — BODMAS
        # ============================================================

        step_title = Text("BODMAS",font_size=34)
        step_title.next_to(question_block, DOWN, buff=0.45)
        self.play(Write(step_title))
        self.wait(1.5)

        # Starting expression for solution
        expression = MathTex(r"\sqrt{\frac{11}{12}-\frac{1}{3}\div1\frac{1}{2}}", font_size=52)

        expression.next_to(step_title, DOWN, buff=0.55)

        self.play(Write(expression))
        self.wait(1)

        # Highlight division
        division_box = SurroundingRectangle(
            expression[0][10:15],
            buff=0.08
        )

        bodmas_label = Text(
            "Division first",
            font_size=24
        ).next_to(
            division_box,
            DOWN,
            buff=0.2
        )

        self.play(
            Create(division_box),
            Write(bodmas_label)
        )

        self.wait(1.5)

        # Remove highlight by shrinking it away
        self.play(
            division_box.animate.scale(0.01),
            bodmas_label.animate.set_opacity(0),
            run_time=0.4
        )

        self.remove(division_box, bodmas_label)

        # ============================================================
        # STEP 2 — CONVERT MIXED FRACTION
        # ============================================================

        # Show the mixed fraction conversion separately
        conversion_title = Text(
            "Convert the mixed fraction",
            font_size=27
        )

        conversion_title.next_to(
            expression,
            DOWN,
            buff=0.5
        )

        self.play(
            Write(conversion_title)
        )

        mixed_fraction = MathTex(
            r"1\frac{1}{2}",
            font_size=46
        )

        mixed_fraction.next_to(
            conversion_title,
            DOWN,
            buff=0.35
        )

        self.play(
            Write(mixed_fraction)
        )

        self.wait(0.8)

        # Explain the conversion visually
        conversion_rule = MathTex(
            r"\frac{(1\times2)+1}{2}",
            font_size=42
        )

        conversion_rule.next_to(
            mixed_fraction,
            RIGHT,
            buff=0.45
        )

        equals = MathTex(
            r"=",
            font_size=42
        ).next_to(
            conversion_rule,
            RIGHT,
            buff=0.2
        )

        improper = MathTex(
            r"\frac{3}{2}",
            font_size=46
        ).next_to(
            equals,
            RIGHT,
            buff=0.2
        )

        self.play(
            TransformMatchingTex(
                mixed_fraction.copy(),
                conversion_rule,
                transform_mismatches=True
            ),
            Write(equals),
            Write(improper),
            run_time=1
        )

        self.wait(1.5)

        # ============================================================
        # MORPH ORIGINAL EXPRESSION
        # 1 1/2  --->  3/2
        # ============================================================

        new_expression = MathTex(
            r"\sqrt{\frac{11}{12}-\frac{1}{3}\div\frac{3}{2}}",
            font_size=52
        )

        new_expression.move_to(expression)

        self.play(
            TransformMatchingTex(
                expression,
                new_expression,
                transform_mismatches=True
            ),
            run_time=1.2
        )

        expression = new_expression

        # The conversion explanation is no longer needed.
        # Morph it downward into the next step title.
        self.play(
            conversion_title.animate.scale(0.7).move_to(
                expression.get_bottom() + DOWN * 0.35
            ),
            conversion_rule.animate.scale(0.01),
            equals.animate.scale(0.01),
            improper.animate.scale(0.01),
            run_time=0.5
        )

        self.remove(
            conversion_rule,
            equals,
            improper,
            conversion_title
        )

        # ============================================================
        # STEP 3 — PERFORM THE DIVISION
        # ============================================================

        division_title = Text(
            "Perform the division",
            font_size=27
        ).next_to(
            expression,
            DOWN,
            buff=0.45
        )

        self.play(
            Write(division_title)
        )

        # Show reciprocal idea
        division_work = MathTex(
            r"\frac{1}{3}\div\frac{3}{2}"
            r"="
            r"\frac{1}{3}\times\frac{2}{3}",
            font_size=42
        )

        division_work.next_to(
            division_title,
            DOWN,
            buff=0.3
        )

        self.play(
            Write(division_work)
        )

        self.wait(1.2)

        # Morph into simplified result
        division_result = MathTex(
            r"\frac{1}{3}\div\frac{3}{2}"
            r"="
            r"\frac{2}{9}",
            font_size=42
        )

        division_result.move_to(division_work)

        self.play(
            TransformMatchingTex(
                division_work,
                division_result,
                transform_mismatches=True
            ),
            run_time=1
        )

        self.wait(1)

        # ============================================================
        # MORPH MAIN EXPRESSION
        # ============================================================

        next_expression = MathTex(
            r"\sqrt{\frac{11}{12}-\frac{2}{9}}",
            font_size=52
        )

        next_expression.move_to(expression)

        self.play(
            TransformMatchingTex(
                expression,
                next_expression,
                transform_mismatches=True
            ),
            run_time=1
        )

        expression = next_expression

        # Clear division explanation
        self.play(
            division_title.animate.scale(0.01),
            division_result.animate.scale(0.01),
            run_time=0.4
        )

        self.remove(
            division_title,
            division_result
        )

        # ============================================================
        # STEP 4 — SUBTRACTION
        # ============================================================

        subtraction_title = Text(
            "Now subtract",
            font_size=27
        ).next_to(
            expression,
            DOWN,
            buff=0.45
        )

        self.play(
            Write(subtraction_title)
        )

        subtraction_work = MathTex(
            r"\frac{11}{12}-\frac{2}{9}",
            font_size=44
        )

        subtraction_work.next_to(
            subtraction_title,
            DOWN,
            buff=0.3
        )

        self.play(
            Write(subtraction_work)
        )

        self.wait(1)

        # Common denominator
        common_denominator = MathTex(
            r"="
            r"\frac{33}{36}"
            r"-"
            r"\frac{8}{36}",
            font_size=44
        )

        common_denominator.next_to(
            subtraction_work,
            RIGHT,
            buff=0.4
        )

        self.play(
            Write(common_denominator)
        )

        self.wait(1)

        # Morph subtraction into result
        subtraction_result = MathTex(
            r"\frac{11}{12}-\frac{2}{9}"
            r"="
            r"\frac{25}{36}",
            font_size=44
        )

        subtraction_result.move_to(
            subtraction_work
        )

        self.play(
            TransformMatchingTex(
                subtraction_work,
                subtraction_result,
                transform_mismatches=True
            ),
            common_denominator.animate.scale(0.01),
            run_time=1
        )

        self.remove(common_denominator)

        self.wait(1)

        # ============================================================
        # MORPH MAIN EXPRESSION
        # ============================================================

        final_inside_root = MathTex(
            r"\sqrt{\frac{25}{36}}",
            font_size=52
        )

        final_inside_root.move_to(expression)

        self.play(
            TransformMatchingTex(
                expression,
                final_inside_root,
                transform_mismatches=True
            ),
            run_time=1
        )

        expression = final_inside_root

        # Clear subtraction explanation
        self.play(
            subtraction_title.animate.scale(0.01),
            subtraction_result.animate.scale(0.01),
            run_time=0.4
        )

        self.remove(
            subtraction_title,
            subtraction_result
        )

        # ============================================================
        # STEP 5 — SQUARE ROOT
        # ============================================================

        root_title = Text(
            "Finally, evaluate the square root",
            font_size=27
        ).next_to(
            expression,
            DOWN,
            buff=0.45
        )

        self.play(
            Write(root_title)
        )

        root_work = MathTex(
            r"\sqrt{\frac{25}{36}}"
            r"="
            r"\frac{\sqrt{25}}{\sqrt{36}}",
            font_size=44
        )

        root_work.next_to(
            root_title,
            DOWN,
            buff=0.3
        )

        self.play(
            Write(root_work)
        )

        self.wait(1)

        # ============================================================
        # MORPH TO FINAL ANSWER
        # ============================================================

        final_answer = MathTex(
            r"\sqrt{\frac{25}{36}}"
            r"="
            r"\boxed{\frac{5}{6}}",
            font_size=50
        )

        final_answer.move_to(root_work)

        self.play(
            TransformMatchingTex(
                root_work,
                final_answer,
                transform_mismatches=True
            ),
            run_time=1.2
        )

        self.wait(2)

        # ============================================================
        # FINAL RESULT
        # ============================================================

        final_box = SurroundingRectangle(
            final_answer,
            buff=0.18
        )

        self.play(
            Create(final_box)
        )

        self.wait(3)


        #------------ QUESTION2 ------------
class question2(Scene):
    def construct(self):
        question_number = Text("2.", font_size=32)

        question = VGroup(
            Text("Baraka earns Ksh. 210 per hour working at a supermarket. The employer changed the amount", font_size=21),
            Text("earned per hour in the ratio 8 : 7.", font_size=21),
            MathTex(r"\text{Determine the amount Baraka would earn }" r" 10\frac{1}{2}\text{ hours}", font_size=21)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        question_number.next_to(question[0], LEFT, buff=0.25)

        question_block = VGroup(question_number, question)

        question_block.to_edge(UL, buff=0.25)

        self.play(
            LaggedStart(
                *[FadeIn(mob, shift=UP) for mob in question_block],
                lag_ratio=0.1
            )
        )
        self.wait(2)

        # --- Working it out ---

        heading = Text("Ratio & Proportion", color=BLUE, font_size=26)
        self.play(Write(heading))
        self.wait(1)
        self.play(FadeOut(heading))

        #STEP 1 ------------- start with ehat we know

        original_rate = MathTex(r"\text{Original rate} = \text{Ksh. }210\text{/hour}", font_size=34)
        ratio = MathTex(r"\text{ratio} = 8 : 7",font_size=34)
        hours = MathTex(r"\text{Time} = 10\frac{1}{2}\text{ hours}", font_size=34)

        information = VGroup(original_rate, ratio, hours).arrange(DOWN, buff=0.45)
        self.play(FadeIn(information, shift=UP))
        self.wait(2)
        self.play(FadeOut(information))

        #FIND THE NEW HOURLY RATE
        # 'let's find the new horly rate first'

        step1 = MathTex(r"\text{New rate}" r"=", r"210\times\frac{8}{7}", color=BLUE, font_size=42).move_to(UP)
        self.play(Write(step1))
        self.wait(1)

        step2 = MathTex(r"=\frac{1680}{7}", color=BLUE, font_size=42).next_to(step1, DOWN, buff=0.35)
        self.play(Write(step2))

        step3 = MathTex(r"=240", color=BLUE, font_size=48).next_to(step2, DOWN, buff=0.35)
        self.play(Write(step3))

        answer_rate = MathTex(r"\boxed{\text{New rate}=\text{Ksh. }240\text{ per hour}}", color=GREEN, font_size=38).next_to(step3, DOWN, buff=0.5)
        self.play(Write(answer_rate))
        self.wait(2)

        self.play(FadeOut(step1), FadeOut(step2), FadeOut(step3), answer_rate.animate.shift(UP*3.2), run_time=1.5)
        self.wait(1)

   # convert the mixed fraction to an improper fraction

        equation = MathTex(r"\text{Earnings}" r"=", r"\text{rate}\times\text{time}", color=BLUE, font_size=40)
        self.play(Write(equation))
        self.wait(1)
        self.play(FadeOut(equation))

        mixed = MathTex(r"10\frac{1}{2}\text{ hours}", color=BLUE, font_size=50)
        self.play(Write(mixed))

        conversion = MathTex(r"10\frac{1}{2}" r"=", r"\frac{10\times2+1}{2}", color=BLUE, font_size=42).next_to(mixed, DOWN, buff=0.5)
        self.play(Write(conversion))

        fraction = MathTex(r"\text{time}=\boxed{\frac{21}{2}}", color=GREEN, font_size=50).next_to(conversion, DOWN, buff=0.4)

        self.play(Write(fraction))
        self.wait(2)

        self.play(FadeOut(mixed), FadeOut(conversion), FadeOut(fraction))


        #Calculate Baraka's earnings-- earnings = rate * time

        substitution = MathTex(r"=240\times\frac{21}{2}",color=BLUE, font_size=45)
        self.play(Write(substitution))

        calculation = MathTex(r"=\frac{5040}{2}", font_size=45).next_to(substitution, DOWN, buff=0.4)
        self.play(Write(calculation))

        final_value = MathTex(r"= \text{Ksh. }2,520", color=GREEN, font_size=48).next_to(calculation, DOWN, buff=0.4)
        self.play(Create(SurroundingRectangle(final_value, buff=0.2)), Write(final_value))
        self.wait(2)
