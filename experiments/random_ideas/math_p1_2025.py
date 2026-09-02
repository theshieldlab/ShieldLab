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

        step_title = Text("BODMAS", color=BLUE, font_size=34)
        step_title.next_to(question_block, DOWN, buff=0.45)
        self.play(Write(step_title))
        self.wait(1.5)

        # Starting expression for solution
        expression = MathTex(r"\sqrt{\frac{11}{12}-\frac{1}{3}\div1\frac{1}{2}}", font_size=52)

        expression.next_to(step_title, DOWN, buff=0.55)

        self.play(Write(expression))
        self.wait(2)

        #highlight division
        division_box = SurroundingRectangle(expression[0][10:15], buff=0.08)
        bodmas_label = Text("Division first", font_size=24, color=YELLOW).next_to(division_box, DOWN, buff=0.2)
        self.play(Create(division_box), Write(bodmas_label))
        self.wait(1.5)

        # Remove highlight
        self.play(
            division_box.animate.scale(0.01),
            bodmas_label.animate.set_opacity(0),
            run_time=0.4
        )

        self.remove(division_box, bodmas_label)

        #convert mixed fraction to improper fraction
       
        # Show the mixed fraction conversion separately
        conversion_title = Text("Convert the mixed fraction", font_size=27)
        conversion_title.next_to(expression, DOWN, buff=0.5)
        self.play(Write(conversion_title))

        mixed_fraction = MathTex(r"1\frac{1}{2}", color=BLUE, font_size=46)
        mixed_fraction.next_to(conversion_title, DOWN, buff=0.35)

        self.play(Write(mixed_fraction))

        self.wait(0.8)

        # Explain the conversion visually
        conversion_rule = MathTex(r" = \frac{(1\times2)+1}{2}", color=BLUE, font_size=42)
        conversion_rule.next_to(mixed_fraction, RIGHT, buff=0.45)
        equals = MathTex(r"=", color=BLUE, font_size=42).next_to(conversion_rule, RIGHT, buff=0.2)
        improper = MathTex(r"\frac{3}{2}", color=BLUE, font_size=46).next_to(equals, RIGHT, buff=0.2)

        self.play(TransformMatchingTex(
                mixed_fraction.copy(),
                conversion_rule,
                transform_mismatches=True
            ),
            Write(equals), Write(improper), run_time=1
        )

        self.wait(1.5)
        # ============================================================
        # MORPH ORIGINAL EXPRESSION
        # 1 1/2  --->  3/2
        # ============================================================
   #our original expression now becomes 11/12 - 1/3 ÷ 3/2
        new_expression = MathTex(r"\sqrt{\frac{11}{12}-\frac{1}{3}\div\frac{3}{2}}", font_size=52)
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
        self.wait(1) 
        self.remove(conversion_rule, equals, improper, conversion_title, mixed_fraction)

        self.wait(1.5)

        # ============================================================
        #PERFORM THE DIVISION
        # ============================================================

        division_title = Text("Perform the division", color=BLUE, font_size=27).next_to(expression, DOWN, buff=0.45)
        self.play(Write(division_title))

        #show reciprocal idea
        division_work = MathTex(r"\frac{1}{3}\div\frac{3}{2}" r"=" r"\frac{1}{3}\times\frac{2}{3}",
            color=BLUE, font_size=42
        )

        division_work.next_to(division_title, DOWN, buff=0.3)

        self.play(Write(division_work))
        self.wait(1.2)

        #morph into simplified result
        division_result = MathTex(r"\frac{1}{3}\div\frac{3}{2}" r"=" r"\frac{2}{9}", color=BLUE, font_size=42)
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
        next_expression = MathTex(r"\sqrt{\frac{11}{12}-\frac{2}{9}}", font_size=52)
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

        #clear division explanation
        self.play(division_title.animate.scale(0.01), division_result.animate.scale(0.01), run_time=0.4)
        self.remove(division_title, division_result)

        # ============================================================
        #SUBTRACTION
        # ============================================================
        subtraction_title = Text("Now subtract", color=BLUE, font_size=27).next_to(expression, DOWN, buff=0.45)
        self.play(Write(subtraction_title))

        subtraction_work = MathTex(r"\frac{11}{12}-\frac{2}{9}", color=BLUE, font_size=44)
        subtraction_work.next_to(subtraction_title, DOWN, buff=0.3)
        self.play(Write(subtraction_work))

        self.wait(1)

        # Common denominator
        common_denominator = MathTex(r"=" r"\frac{33}{36}" r"-" r"\frac{8}{36}", color=BLUE, font_size=44)
        common_denominator.next_to(subtraction_work, RIGHT, buff=0.4)
        self.play(Write(common_denominator))

        self.wait(1)

        # Morph subtraction into result
        subtraction_result = MathTex(r"\frac{11}{12}-\frac{2}{9}" r"=" r"\frac{25}{36}",
            color=BLUE, font_size=44
        )
        subtraction_result.move_to(subtraction_work)

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

        final_inside_root = MathTex(r"\sqrt{\frac{25}{36}}", font_size=52)
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

        self.wait(1.5)

        # Clear subtraction explanation
        self.play(subtraction_title.animate.scale(0.01), subtraction_result.animate.scale(0.01), run_time=0.4)
        self.remove(subtraction_title, subtraction_result)

        # ============================================================
        # SQUARE ROOT
        # ============================================================

        root_title = Text("Finally, evaluate the square root", color=BLUE, font_size=27).next_to(expression, DOWN, buff=0.45)
        self.play(Write(root_title))
        self.wait(1)

        root_work = MathTex(r"\sqrt{\frac{25}{36}}" r"=" r"\frac{\sqrt{25}}{\sqrt{36}}", color=BLUE, font_size=44)

        root_work.next_to(root_title, DOWN, buff=0.3)
        self.play(Write(root_work))

        self.wait(1)

        # ============================================================
        # MORPH TO FINAL ANSWER
        # ============================================================

        final_answer = MathTex(r"\sqrt{\frac{25}{36}}" r"=" r"\boxed{\frac{5}{6}}",
            color=BLUE, font_size=50
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

        # Then explain the ± distinction  square root → positive answer; solving a squared equation → ± answers
        #The square-root symbol means the principal (non-negative) square root
        #You get \(\pm\frac56\) when solving an equation such as

        note = MathTex(r"\text{If }x^2=\frac{25}{36},\quad x=\pm\frac{5}{6}", font_size=32)
        note.next_to(final_answer, DOWN, buff=0.5)

        self.play(Write(note))
        self.wait(2)

        # ============================================================
        # FINAL RESULT
        # ============================================================

        final_box = SurroundingRectangle(final_answer, buff=0.18)

        self.play(Create(final_box))
        self.wait(3)


        #------------ QUESTION2 ------------
class Question2(Scene):
    def construct(self):
        question_number = Text("2.", font_size=32)

   #question text
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


        # calculate Baraka's earnings -- earnings = rate * time

        substitution = MathTex(r"=240\times\frac{21}{2}",color=BLUE, font_size=45)
        self.play(Write(substitution))

        calculation = MathTex(r"=\frac{5040}{2}", font_size=45).next_to(substitution, DOWN, buff=0.4)
        self.play(Write(calculation))

        final_value = MathTex(r"= \text{Ksh. }2,520", color=GREEN, font_size=48).next_to(calculation, DOWN, buff=0.4)
        self.play(Create(SurroundingRectangle(final_value, buff=0.2)), Write(final_value))
        self.wait(2)


class Question3(Scene):

    def construct(self):

        # question number and text

        question_number = Text("3.", font_size=30)

        question_text = VGroup(Text("Solve for x in the equation.", font_size=25),
            MathTex(r"4^{3x}\times8" r"=" r"\left(\frac{1}{32}\right)^{2x-3}", font_size=38)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        question_number.next_to(question_text[0], LEFT, buff=0.25)
        question_block = VGroup(question_number, question_text)

        question_block.to_edge(UL, buff=0.25)

        # Show question
        self.play(Write(question_number),
            LaggedStart(
                *[Write(mob) for mob in question_text],
                lag_ratio=0.15
            )
        )

        self.wait(2)

        # ============================================================
        # STEP 1 write everything in terms of base 2

        step_title = Text("Express everything as powers of 2", font_size=31)
        step_title.next_to(question_block, DR, buff=0.5)

        self.play(Write(step_title))

        self.wait(1)

        # Original equation
        equation = MathTex(r"4^{3x}\times8" r"=" r"\left(\frac{1}{32}\right)^{2x-3}", color=BLUE, font_size=48)
        equation.next_to(step_title, DOWN, buff=0.5)
        self.play(Write(equation))
        self.wait(1)

        # ------------------------------------------------------------
        # Show the substitutions
        # ------------------------------------------------------------

        substitutions = VGroup(MathTex(r"4=2^2", color=BLUE, font_size=32),
            MathTex(r"8=2^3", color=GREEN, font_size=32),
            MathTex(r"\frac{1}{32}=2^{-5}", color=ORANGE, font_size=32)
        ).arrange(RIGHT, buff=0.6)

        substitutions.next_to(equation, DOWN, buff=0.45)

        self.play(
            LaggedStart(
                *[Write(x) for x in substitutions],
                lag_ratio=0.8
            )
        )

        self.wait(1.5)

        # ============================================================
        # MORPH INTO POWERS OF 2

        powers_of_two = MathTex(r"(2^2)^{3x}\times2^3" r"=" r"(2^{-5})^{2x-3}", color=BLUE, font_size=48)
        powers_of_two.move_to(equation)

        self.play(TransformMatchingTex(equation, powers_of_two, transform_mismatches=True), run_time=1.3)

        equation = powers_of_two

        self.wait(1)

        # Remove substitutions
        self.play(
            *[
                mob.animate.scale(0.01)
                for mob in substitutions
            ],
            step_title.animate.scale(0.01),
            run_time=0.4
        )

        self.remove(substitutions, step_title)

        # ============================================================
        # STEP 2 Apply law: (a^m)^n = a^(mn)

        step_title = Text("Apply the laws of indices", font_size=31)

        step_title.next_to(question_block, DR, buff=0.45)
        self.play(Write(step_title))

        law = MathTex(r"(a^m)^n=a^{mn}", color=YELLOW, font_size=32)
        law.next_to(step_title, DOWN, buff=0.3)
        self.play(Write(law))

        self.wait(1)

        # ------------------------------------------------------------
        # Expand the powers

        expanded = MathTex(r"2^{6x}\times2^3" r"=" r"2^{-10x+15}", font_size=48)
        expanded.move_to(equation)

        self.play(
            TransformMatchingTex(
                equation,
                expanded,
                transform_mismatches=True
            ),
            run_time=1.3
        )

        equation = expanded

        self.wait(1.5)

        # Remove law
        self.play(law.animate.scale(0.01), step_title.animate.scale(0.01), run_time=0.4)

        self.remove(law, step_title)

        # ============================================================
        # STEP 3: Combine powers with same base

        step_title = Text("Combine powers with the same base",font_size=31)
        step_title.next_to(question_block, DR, buff=0.45)

        self.play(Write(step_title))

        law = MathTex(r"a^m\times a^n=a^{m+n}", color=YELLOW, font_size=32)
        law.next_to(step_title, DOWN, buff=0.3)

        self.play(Write(law))
        self.wait(1)

        # Morph into combined powers
        combined = MathTex(r"2^{6x+3}" r"=" r"2^{-10x+15}", color=BLUE, font_size=50)
        combined.move_to(equation)

        self.play(
            TransformMatchingTex(
                equation,
                combined,
                transform_mismatches=True
            ),
            run_time=1.2
        )

        equation = combined
        self.wait(1.5)

        # Remove law
        self.play(law.animate.scale(0.01), step_title.animate.scale(0.01), run_time=0.4)

        self.remove(law, step_title)

        # ============================================================
        # STEP 4: Equate the exponents
        step_title = Text("Equate the exponents", font_size=31)
        step_title.next_to(question_block, DR, buff=0.45)
        self.play(Write(step_title))

        explanation = Text("Same base → same exponent", font_size=27)
        explanation.next_to(step_title, DOWN, buff=0.25)

        self.play(Write(explanation))
        self.wait(1)

        # ------------------------------------------------------------
        # Morph into exponent equation

        exponent_equation = MathTex(r"6x+3=-10x+15", color=BLUE, font_size=50)
        exponent_equation.move_to(equation)

        self.play(TransformMatchingTex(equation, exponent_equation, transform_mismatches=True), run_time=1.1)

        equation = exponent_equation
        self.wait(1.5)

        # Remove explanation
        self.play(explanation.animate.scale(0.01), step_title.animate.scale(0.01), run_time=0.4)
        self.remove(explanation, step_title)

        # ============================================================
        # STEP 5: Solve the linear equation

        step_title = Text("Solve for x", font_size=31)
        step_title.next_to(question_block, DR, buff=0.45)
        self.play(Write(step_title))

        # ------------------------------------------------------------
        # Move +10x to left

        step_a = MathTex(r"6x+10x" r"=" r"15-3", color=BLUE, font_size=48)
        step_a.move_to(equation)

        self.play(TransformMatchingTex(equation, step_a, transform_mismatches=True), run_time=1)

        equation = step_a
        self.wait(1)

        # ------------------------------------------------------------
        # Simplify

        step_b = MathTex(r"16x=12", color=BLUE,  font_size=50)
        step_b.move_to(equation)

        self.play(TransformMatchingTex(equation, step_b, transform_mismatches=True), run_time=0.9)

        equation = step_b

        self.wait(1)

        # ------------------------------------------------------------
        # Divide by 16

        step_c = MathTex(r"x=\frac{12}{16}", color=BLUE, font_size=50)
        step_c.move_to(equation)

        self.play(TransformMatchingTex(equation, step_c, transform_mismatches=True), run_time=0.9)
        equation = step_c

        self.wait(1)

        # ------------------------------------------------------------
        # Simplify fraction

        final_answer = MathTex(r"x= {\frac{3}{4}}", color=YELLOW,     font_size=56)
        final_answer.move_to(equation)

        self.play(TransformMatchingTex(equation, final_answer, transform_mismatches=True), run_time=1)
        equation = final_answer

        self.wait(2)

        # FINAL ANSWER
        final_box = SurroundingRectangle(final_answer, buff=0.18)
        self.play(Create(final_box), run_time=0.7)
        self.wait(3)

        #------ Question 4 ----

class Question4(Scene):

    def construct(self):

        question_number = Text("4.", font_size=30)
        question_text = VGroup(Text("Solve the inequality, giving the answer", font_size=24),
            Text("as a combined inequality.", font_size=24),
            MathTex(r"-1\leq\frac{5-2x}{3}<2x-1", font_size=40)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        question_number.next_to(question_text[0], LEFT, buff=0.25)
        question_block = VGroup(question_number, question_text)
        question_block.to_edge(UL, buff=0.25)

        # ------------------------------------------------------------
        # Show question

        self.play(
            Write(question_number),
            LaggedStart(
                *[Write(mob) for mob in question_text],
                lag_ratio=0.15
            )
        )

        self.wait(2)

        # ============================================================
        # STEP 1 — REMOVE THE DENOMINATOR

        step_title = Text("Remove the denominator", UP*1.5, font_size=28)

        self.play(Write(step_title))

        equation = MathTex(r"-1\leq\frac{5-2x}{3}<2x-1", color=BLUE, font_size=40)
        equation.next_to(step_title, DOWN, buff=0.5)
        self.play(Write(equation))

        self.wait(1)

        # Explain multiplying ALL parts by 3
        operation = MathTex(r"\times3", color=YELLOW, font_size=34)
        operation.next_to(equation, DOWN, buff=0.3)
        self.play(Write(operation))

        self.wait(1)

        # ------------------------------------------------------------
        # Morph into denominator-free inequality
        # ------------------------------------------------------------

        multiplied = MathTex(r"-3\leq 5-2x < 6x-3", color=BLUE,font_size=52,
                        substrings_to_isolate=[
                                                r"-3",
                                                r"5-2x",
                                                r"6x-3"
                                            ])
        multiplied.move_to(equation)

        self.play(TransformMatchingTex(equation, multiplied, transform_mismatches=True), operation.animate.scale(0.01), run_time=1.2)

        self.remove(operation)

        equation = multiplied

        self.wait(2)

        # Remove step title
        self.play(step_title.animate.scale(0.01), run_time=0.4)
        self.remove(step_title)

        left_number = multiplied.get_part_by_tex(r"-3")
        middle = multiplied.get_part_by_tex(r"5-2x")
        right_number = multiplied.get_part_by_tex(r"6x-3")

        # Highlight first inequality
        left_box = SurroundingRectangle(VGroup(left_number, middle), buff=0.15)

        left_label = Text("First inequality", font_size=24).next_to(left_box, DOWN, buff=0.15)

        self.play(Create(left_box), Write(left_label))

        self.wait(1.5)

        # Move the highlight away
        self.play(FadeOut(left_box), FadeOut(left_label))

        # Highlight second inequality
        right_box = SurroundingRectangle(VGroup(middle, right_number), buff=0.15)

        right_label = Text("Second inequality", font_size=24).next_to(right_box, DOWN, buff=0.15)

        self.play(Create(right_box), Write(right_label))

        self.wait(1.5)

        self.play(FadeOut(right_box), FadeOut(right_label))
        

        # ============================================================
        # STEP 2 — SPLIT THE COMPOUND INEQUALITY

        step_title = Text("Solve both inequalities", font_size=31)
        step_title.next_to(question_block, UP*1.5, buff=0.45)
        self.play(Write(step_title))

        # Visual split
        left_ineq = MathTex(r"-3\leq5-2x", color=RED,font_size=46)
        right_ineq = MathTex(r"5-2x<6x-3", color=GREEN, font_size=46)
        two_inequalities = VGroup(left_ineq, right_ineq).arrange(DOWN, buff=0.55)
        two_inequalities.move_to(equation)

        self.play(TransformMatchingTex(equation, left_ineq, transform_mismatches=True), run_time=0.8)

        self.play(Write(right_ineq))

        self.wait(2)

        # ============================================================
        # LEFT INEQUALITY
        # ============================================================

        left_step = MathTex(r"-3\leq5-2x", color=RED, font_size=42)
        left_step.to_edge(LEFT, buff=1.0)
        left_label = Text("First inequality", font_size=24).next_to(left_step, UP, buff=0.25)

        self.play(FadeIn(left_label), Transform(left_ineq, left_step))
        self.wait(1.5)

        # Move 5
        left_a = MathTex(r"-8\leq-2x", color=RED, font_size=44)
        left_a.next_to(left_step, DOWN, buff=0.25)

        self.play(TransformMatchingTex(left_step, left_a, transform_mismatches=True), run_time=0.9)

        self.wait(1.5)

        # Divide by -2
        left_b = MathTex(r"x\leq4", color=RED, font_size=48)
        left_b.next_to(left_a, DOWN, buff=0.25)

        self.play(TransformMatchingTex(left_a, left_b, transform_mismatches=True), run_time=0.9)

        # ============================================================
        # IMPORTANT: EXPLAIN REVERSING INEQUALITY


        warning = Text("dividing by a negative reverses the sign", color=YELLOW, font_size=18)
        warning.next_to(left_b, DOWN, buff=0.25)
        self.play(Write(warning))

        self.wait(1.5)

        # ============================================================
        # RIGHT INEQUALITY
        # ============================================================

        right_step = MathTex(r"5-2x<6x-3", color=GREEN, font_size=42)
        right_step.to_edge(RIGHT, buff=1.0)

        right_label = Text("Second inequality", font_size=24).next_to(right_step, UP, buff=0.25)
        self.play(FadeIn(right_label), Transform(right_ineq, right_step))
        self.wait(1.5)

        # Move terms
        right_a = MathTex(r"8<8x", color=GREEN, font_size=44)
        right_a.next_to(right_step, DOWN, buff=0.25)

        self.play(TransformMatchingTex(right_step, right_a, transform_mismatches=True), run_time=0.9)

        self.wait(1.5)

        # Divide by 8
        right_b = MathTex(r"1<x", color=GREEN, font_size=48)
        right_b.next_to(right_a, DOWN, buff=0.25)

        self.play(TransformMatchingTex(right_a, right_b, transform_mismatches=True), run_time=0.9)

        self.wait(2)

        # ============================================================
        # CLEAN UP
        # ============================================================

        self.play(FadeOut(left_label), FadeOut(right_label), FadeOut(warning), FadeOut(step_title), run_time=0.5)

        # ============================================================
        # STEP 3 — COMBINE THE RESULTS
        # ============================================================

        step_title = Text("Combine the results", UP*1.5, font_size=31)
        self.play(Write(step_title))

        # Bring results together
        left_result = MathTex(r"x\leq4", font_size=48)
        right_result = MathTex(r"1<x", font_size=48)
        results = VGroup(right_result, left_result).arrange(RIGHT, buff=1.0)
        results.next_to(step_title, DOWN, buff=0.55)

        self.play(Transform(left_step, left_result), Transform(right_step, right_result))

        self.wait(1)

        # ------------------------------------------------------------
        # Morph into combined inequality
        # ------------------------------------------------------------

        combined = MathTex(r"1<x\leq4", color=YELLOW, font_size=58)
        combined.next_to(results, DOWN, buff=0.55)

        self.play(TransformMatchingTex(results, combined, transform_mismatches=True), run_time=1.2)

        self.wait(1)

        # ============================================================
        # FINAL ANSWER
        # ============================================================

        final_box = SurroundingRectangle(combined, buff=0.2)
        self.play(Create(final_box), run_time=0.7)
        self.wait(3)