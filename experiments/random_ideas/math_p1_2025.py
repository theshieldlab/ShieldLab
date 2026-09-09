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

        step_title = Text("Remove the denominator", font_size=28).move_to(UP)
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

        step_title = Text("Solve both inequalities", font_size=31).move_to(UP)
        self.play(Write(step_title))
        self.wait(1.5)

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

        step_title = Text("Combine the results", font_size=31).move_to(UP)
        self.play(Write(step_title))

        # Bring results together
        left_result = MathTex(r"x\leq4", font_size=48)
        right_result = MathTex(r"1<x", font_size=48)
        results = VGroup(right_result, left_result).arrange(RIGHT, buff=1.0)
        results.next_to(step_title, DOWN, buff=0.55)

        self.play(Transform(left_b, left_result), Transform(right_b, right_result))

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

        final_box = SurroundingRectangle(combined, buff=0.2)
        self.play(Create(final_box), run_time=0.7)
        self.wait(3)


        ##--- QUESTION 5 ----

class Question5(Scene):

    def construct(self):

        # ============================================================
        # QUESTION
        # ============================================================

        question_number = Text(
            "5.",
            font_size=30
        )

        question_text = VGroup(
            Text(
                "The figure represents a rectangular farm PQRS.",
                font_size=23
            ),
            Text(
                "The dotted area represents a flooded section.",
                font_size=23
            ),
            Text(
                "Estimate, in m², the area of the farm that is not flooded.",
                font_size=23
            )
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.08
        )

        question_number.next_to(
            question_text,
            LEFT,
            buff=0.25
        )

        question_block = VGroup(
            question_number,
            question_text
        )

        question_block.to_edge(
            UP,
            buff=0.25
        )

        self.play(
            Write(question_number),
            LaggedStart(
                *[Write(line) for line in question_text],
                lag_ratio=0.15
            )
        )

        self.wait(2)

        # ============================================================
        # SHRINK QUESTION
        # ============================================================

        self.play(
            question_block.animate
            .scale(0.62)
            .to_edge(UP, buff=0.15),
            run_time=1
        )

        # ============================================================
        # DRAW THE FARM GRID
        # ============================================================

        rows = 4
        cols = 7
        cell_size = 0.8

        grid = VGroup()

        for row in range(rows):
            for col in range(cols):

                square = Square(
                    side_length=cell_size,
                    stroke_width=1.5
                )

                square.move_to(
                    np.array([
                        (col - 3) * cell_size,
                        (1.5 - row) * cell_size - 0.5,
                        0
                    ])
                )

                grid.add(square)

        self.play(
            Create(grid),
            run_time=1.5
        )

        # ============================================================
        # LABEL DIMENSIONS
        # ============================================================

        top_label = MathTex(
            r"210\text{ m}",
            font_size=32
        )

        top_label.next_to(
            grid,
            UP,
            buff=0.2
        )

        left_label = MathTex(
            r"120\text{ m}",
            font_size=32
        )

        left_label.next_to(
            grid,
            LEFT,
            buff=0.3
        )

        self.play(
            Write(top_label),
            Write(left_label)
        )

        self.wait(1)

        # ============================================================
        # STEP 1
        # FIND DIMENSIONS OF ONE GRID SQUARE
        # ============================================================

        step_title = Text(
            "Step 1: Find the dimensions of one square",
            font_size=30
        )

        step_title.next_to(
            question_block,
            DOWN,
            buff=0.35
        )

        self.play(
            Write(step_title)
        )

        # Highlight one horizontal row
        horizontal_arrow = Arrow(
            grid.get_corner(UL) + DOWN * 0.2,
            grid.get_corner(UR) + DOWN * 0.2,
            buff=0.1
        )

        horizontal_text = MathTex(
            r"\frac{210}{7}=30\text{ m}",
            font_size=34
        )

        horizontal_text.next_to(
            grid,
            DOWN,
            buff=0.3
        )

        self.play(
            GrowArrow(horizontal_arrow),
            Write(horizontal_text)
        )

        self.wait(1)

        # Highlight vertical division
        vertical_arrow = Arrow(
            grid.get_corner(UL) + RIGHT * 0.2,
            grid.get_corner(DL) + RIGHT * 0.2,
            buff=0.1
        )

        vertical_text = MathTex(
            r"\frac{120}{4}=30\text{ m}",
            font_size=34
        )

        vertical_text.next_to(
            horizontal_text,
            DOWN,
            buff=0.25
        )

        self.play(
            GrowArrow(vertical_arrow),
            Write(vertical_text)
        )

        self.wait(1.5)

        # ============================================================
        # AREA OF ONE GRID SQUARE
        # ============================================================

        area_one_square = MathTex(
            r"\text{Area of one square}"
            r"="
            r"30\times30"
            r"="
            r"900\text{ m}^2",
            font_size=38
        )

        area_one_square.next_to(
            vertical_text,
            DOWN,
            buff=0.35
        )

        self.play(
            Write(area_one_square)
        )

        self.wait(2)

        # ============================================================
        # CLEAR STEP 1 WORK
        # ============================================================

        self.play(
            FadeOut(step_title),
            FadeOut(horizontal_arrow),
            FadeOut(vertical_arrow),
            FadeOut(horizontal_text),
            FadeOut(vertical_text),
            FadeOut(area_one_square)
        )

        # ============================================================
        # STEP 2
        # ESTIMATE FLOODED AREA
        # ============================================================

        step_title = Text(
            "Step 2: Estimate the flooded area",
            font_size=30
        )

        step_title.next_to(
            question_block,
            DOWN,
            buff=0.35
        )

        self.play(
            Write(step_title)
        )

        # ------------------------------------------------------------
        # Approximate flooded squares
        #
        # These are selected to visually represent approximately
        # 8 squares covered by the dotted region.
        # ------------------------------------------------------------

        flooded_indices = [
            8, 9, 10,
            15, 16, 17, 18,
            23
        ]

        flooded_squares = VGroup(
            *[grid[i].copy() for i in flooded_indices]
        )

        self.play(
            LaggedStart(
                *[
                    Indicate(
                        square,
                        scale_factor=1.15
                    )
                    for square in flooded_squares
                ],
                lag_ratio=0.15
            )
        )

        self.wait(1)

        estimate = MathTex(
            r"\text{Flooded area}\approx8\text{ squares}",
            font_size=38
        )

        estimate.next_to(
            grid,
            DOWN,
            buff=0.35
        )

        self.play(
            Write(estimate)
        )

        self.wait(1.5)

        flooded_area = MathTex(
            r"8\times900"
            r"="
            r"7200\text{ m}^2",
            font_size=42
        )

        flooded_area.next_to(
            estimate,
            DOWN,
            buff=0.3
        )

        self.play(
            TransformMatchingTex(
                estimate.copy(),
                flooded_area,
                transform_mismatches=True
            )
        )

        self.wait(2)

        # ============================================================
        # STEP 3
        # TOTAL AREA OF FARM
        # ============================================================

        self.play(
            FadeOut(step_title),
            FadeOut(estimate),
            FadeOut(flooded_area)
        )

        step_title = Text(
            "Step 3: Find the total area of the farm",
            font_size=30
        )

        step_title.next_to(
            question_block,
            DOWN,
            buff=0.35
        )

        self.play(
            Write(step_title)
        )

        total_area = MathTex(
            r"\text{Total area}"
            r"="
            r"210\times120",
            font_size=42
        )

        total_area.next_to(
            grid,
            DOWN,
            buff=0.4
        )

        self.play(
            Write(total_area)
        )

        self.wait(1)

        total_area_result = MathTex(
            r"=25200\text{ m}^2",
            font_size=46
        )

        total_area_result.next_to(
            total_area,
            DOWN,
            buff=0.3
        )

        self.play(
            Write(total_area_result)
        )

        self.wait(2)

        # ============================================================
        # STEP 4
        # AREA NOT FLOODED
        # ============================================================

        self.play(
            FadeOut(step_title),
            FadeOut(total_area),
            FadeOut(total_area_result)
        )

        step_title = Text(
            "Step 4: Subtract the flooded area",
            font_size=30
        )

        step_title.next_to(
            question_block,
            DOWN,
            buff=0.35
        )

        self.play(
            Write(step_title)
        )

        subtraction = MathTex(
            r"\text{Area not flooded}"
            r"="
            r"25200-7200",
            font_size=44
        )

        subtraction.next_to(
            grid,
            DOWN,
            buff=0.45
        )

        self.play(
            Write(subtraction)
        )

        self.wait(1)

        # ============================================================
        # MORPH TO FINAL ANSWER
        # ============================================================

        final_answer = MathTex(
            r"\boxed{18000\text{ m}^2}",
            font_size=58
        )

        final_answer.next_to(
            subtraction,
            DOWN,
            buff=0.4
        )

        self.play(
            TransformFromCopy(
                subtraction,
                final_answer
            ),
            run_time=1
        )

        self.wait(1)

        final_box = SurroundingRectangle(
            final_answer,
            buff=0.2
        )

        self.play(
            Create(final_box)
        )

        self.wait(3)


        #### QUESTION 6 ####,also check CHatGPT for the solution to this question


class KCSE_Question6(Scene):

    def construct(self):

        # ============================================================
        # QUESTION
        # ============================================================

        question_number = Text(
            "6.",
            font_size=30
        )

        question = VGroup(
            Text(
                "A relief organisation donated 240 kg of maize",
                font_size=22
            ),
            Text(
                "and 150 kg of beans to needy families.",
                font_size=22
            ),
            Text(
                "Each family received exactly the same quantity",
                font_size=22
            ),
            Text(
                "by mass of either maize or beans.",
                font_size=22
            ),
            Text(
                "No family received both. Determine the least",
                font_size=22
            ),
            Text(
                "possible number of needy families.",
                font_size=22
            )
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.04
        )

        question_number.next_to(
            question,
            LEFT,
            buff=0.25
        )

        question_block = VGroup(
            question_number,
            question
        )

        question_block.to_edge(
            UP,
            buff=0.15
        )

        self.play(
            Write(question_number),
            LaggedStart(
                *[Write(line) for line in question],
                lag_ratio=0.12
            ),
            run_time=2.5
        )

        self.wait(2)

        # ============================================================
        # SHRINK QUESTION TO REFERENCE
        # ============================================================

        self.play(
            question_block.animate
            .scale(0.55)
            .to_edge(UP, buff=0.12),
            run_time=1
        )

        # ============================================================
        # STEP 1 — UNDERSTAND WHAT WE NEED
        # ============================================================

        step1 = Text(
            "Step 1: Find the largest equal quantity",
            font_size=30
        ).next_to(
            question_block,
            DOWN,
            buff=0.35
        )

        self.play(Write(step1))

        explanation = MathTex(
            r"\text{Same mass per family}"
            r"\quad\Longrightarrow\quad"
            r"\text{common factor}",
            font_size=40
        )

        explanation.next_to(
            step1,
            DOWN,
            buff=0.5
        )

        self.play(Write(explanation))
        self.wait(2)

        # ============================================================
        # STEP 2 — HCF
        # ============================================================

        self.play(
            FadeOut(step1),
            FadeOut(explanation)
        )

        step2 = Text(
            "Step 2: Find the HCF of 240 and 150",
            font_size=30
        ).next_to(
            question_block,
            DOWN,
            buff=0.35
        )

        self.play(Write(step2))

        factors = VGroup(
            MathTex(
                r"240=2^4\times3\times5",
                font_size=40
            ),
            MathTex(
                r"150=2\times3\times5^2",
                font_size=40
            )
        ).arrange(
            DOWN,
            buff=0.3
        )

        factors.next_to(
            step2,
            DOWN,
            buff=0.45
        )

        self.play(
            Write(factors[0]),
            Write(factors[1])
        )

        self.wait(1.5)

        # Highlight common factors
        common = MathTex(
            r"\text{Common factors: }2\times3\times5=30",
            font_size=40
        )

        common.next_to(
            factors,
            DOWN,
            buff=0.45
        )

        self.play(
            Write(common)
        )

        self.wait(2)

        hcf = MathTex(
            r"\therefore\quad \mathrm{HCF}(240,150)=30\text{ kg}",
            font_size=44
        )

        hcf.next_to(
            common,
            DOWN,
            buff=0.35
        )

        self.play(
            TransformMatchingTex(
                common.copy(),
                hcf,
                transform_mismatches=True
            )
        )

        self.wait(2)

        # ============================================================
        # STEP 3 — NUMBER OF FAMILIES
        # ============================================================

        self.play(
            FadeOut(step2),
            FadeOut(factors),
            FadeOut(common),
            FadeOut(hcf)
        )

        step3 = Text(
            "Step 3: Find the number of families",
            font_size=30
        ).next_to(
            question_block,
            DOWN,
            buff=0.35
        )

        self.play(Write(step3))

        maize = MathTex(
            r"\text{Maize:}\quad \frac{240}{30}=8\text{ families}",
            font_size=40
        )

        beans = MathTex(
            r"\text{Beans:}\quad \frac{150}{30}=5\text{ families}",
            font_size=40
        )

        portions = VGroup(
            maize,
            beans
        ).arrange(
            DOWN,
            buff=0.45
        )

        portions.next_to(
            step3,
            DOWN,
            buff=0.5
        )

        self.play(
            Write(maize)
        )

        self.wait(1)

        self.play(
            Write(beans)
        )

        self.wait(2)

        # ============================================================
        # COMBINE
        # ============================================================

        total = MathTex(
            r"8+5=13\text{ families}",
            font_size=48
        )

        total.next_to(
            portions,
            DOWN,
            buff=0.5
        )

        self.play(
            TransformMatchingTex(
                VGroup(maize.copy(), beans.copy()),
                total,
                transform_mismatches=True
            ),
            run_time=1.5
        )

        self.wait(2)

        # ============================================================
        # FINAL ANSWER
        # ============================================================

        final = MathTex(
            r"\boxed{13\text{ families}}",
            font_size=58
        )

        final.move_to(total)

        self.play(
            TransformMatchingTex(
                total,
                final
            ),
            run_time=1
        )

        self.wait(1)

        final_box = SurroundingRectangle(
            final,
            buff=0.2
        )

        self.play(
            Create(final_box)
        )

        self.wait(3)

        #Question7-----


class KCSE_Question7(Scene):

    def construct(self):

        # ============================================================
        # QUESTION
        # ============================================================

        question_number = Text(
            "7.",
            font_size=30
        )

        question_text = MathTex(
            r"\text{Simplify }\quad"
            r"\frac{x^2-4y^2}{x^2+4xy+4y^2}",
            font_size=40
        )

        question_number.next_to(
            question_text,
            LEFT,
            buff=0.25
        )

        question_block = VGroup(
            question_number,
            question_text
        )

        question_block.to_edge(
            UP,
            buff=0.2
        )

        self.play(
            Write(question_number),
            Write(question_text)
        )

        self.wait(2)

        # ============================================================
        # KEEP QUESTION AT TOP
        # ============================================================

        self.play(
            question_block.animate
            .scale(0.65)
            .to_edge(UP, buff=0.15),
            run_time=1
        )

        # ============================================================
        # ORIGINAL EXPRESSION
        # ============================================================

        expression = MathTex(
            r"\frac{x^2-4y^2}{x^2+4xy+4y^2}",
            font_size=62
        )

        expression.move_to(
            ORIGIN
        )

        self.play(
            Write(expression)
        )

        self.wait(2)

        # ============================================================
        # STEP 1 — FACTOR THE NUMERATOR
        # ============================================================

        step1 = Text(
            "Step 1: Factor the numerator",
            font_size=30
        )

        step1.next_to(
            question_block,
            DOWN,
            buff=0.35
        )

        self.play(
            Write(step1)
        )

        # Highlight numerator
        numerator_box = SurroundingRectangle(
            expression.get_part_by_tex(
                r"x^2-4y^2"
            ),
            buff=0.12
        )

        self.play(
            Create(numerator_box)
        )

        self.wait(1)

        # Difference of squares explanation
        difference = MathTex(
            r"x^2-4y^2"
            r"="
            r"x^2-(2y)^2"
            r"="
            r"(x-2y)(x+2y)",
            font_size=40
        )

        difference.next_to(
            expression,
            DOWN,
            buff=0.6
        )

        self.play(
            Write(difference)
        )

        self.wait(2)

        # ============================================================
        # MORPH WHOLE EXPRESSION
        # ============================================================

        factored_numerator = MathTex(
            r"\frac{(x-2y)(x+2y)}"
            r"{x^2+4xy+4y^2}",
            font_size=62
        )

        factored_numerator.move_to(
            expression
        )

        self.play(
            TransformMatchingTex(
                expression,
                factored_numerator,
                transform_mismatches=True
            ),
            FadeOut(numerator_box),
            FadeOut(difference),
            run_time=1.4
        )

        self.wait(2)

        # ============================================================
        # STEP 2 — FACTOR THE DENOMINATOR
        # ============================================================

        self.play(
            FadeOut(step1)
        )

        step2 = Text(
            "Step 2: Factor the denominator",
            font_size=30
        )

        step2.next_to(
            question_block,
            DOWN,
            buff=0.35
        )

        self.play(
            Write(step2)
        )

        denominator_box = SurroundingRectangle(
            factored_numerator.get_part_by_tex(
                r"x^2+4xy+4y^2"
            ),
            buff=0.12
        )

        self.play(
            Create(denominator_box)
        )

        self.wait(1)

        denominator_factor = MathTex(
            r"x^2+4xy+4y^2"
            r"="
            r"(x+2y)^2",
            font_size=42
        )

        denominator_factor.next_to(
            factored_numerator,
            DOWN,
            buff=0.6
        )

        self.play(
            Write(denominator_factor)
        )

        self.wait(2)

        # ============================================================
        # MORPH TO FULLY FACTORED FORM
        # ============================================================

        fully_factored = MathTex(
            r"\frac{(x-2y)(x+2y)}"
            r"{(x+2y)^2}",
            font_size=62
        )

        fully_factored.move_to(
            factored_numerator
        )

        self.play(
            TransformMatchingTex(
                factored_numerator,
                fully_factored,
                transform_mismatches=True
            ),
            FadeOut(denominator_box),
            FadeOut(denominator_factor),
            run_time=1.4
        )

        self.wait(2)

        # ============================================================
        # STEP 3 — EXPAND THE SQUARE JUST ENOUGH TO SEE CANCELLATION
        # ============================================================

        self.play(
            FadeOut(step2)
        )

        step3 = Text(
            "Step 3: Cancel the common factor",
            font_size=30
        )

        step3.next_to(
            question_block,
            DOWN,
            buff=0.35
        )

        self.play(
            Write(step3)
        )

        # Rewrite denominator so common factor is obvious
        cancellation_form = MathTex(
            r"\frac{(x-2y)(x+2y)}"
            r"{(x+2y)(x+2y)}",
            font_size=62
        )

        cancellation_form.move_to(
            fully_factored
        )

        self.play(
            TransformMatchingTex(
                fully_factored,
                cancellation_form,
                transform_mismatches=True
            ),
            run_time=1.2
        )

        self.wait(1)

        # ============================================================
        # HIGHLIGHT COMMON FACTORS
        # ============================================================

        numerator_common = cancellation_form.get_part_by_tex(
            r"x+2y"
        )

        denominator_common = cancellation_form.get_parts_by_tex(
            r"x+2y"
        )

        # Surround all visible x+2y factors
        common_boxes = VGroup()

        for part in denominator_common:
            common_boxes.add(
                SurroundingRectangle(
                    part,
                    buff=0.08
                )
            )

        self.play(
            LaggedStart(
                *[Create(box) for box in common_boxes],
                lag_ratio=0.15
            )
        )

        self.wait(1)

        # ============================================================
        # CANCEL
        # ============================================================

        simplified = MathTex(
            r"\frac{x-2y}{x+2y}",
            font_size=66
        )

        simplified.move_to(
            cancellation_form
        )

        self.play(
            TransformMatchingTex(
                cancellation_form,
                simplified,
                transform_mismatches=True
            ),
            FadeOut(common_boxes),
            run_time=1.3
        )

        self.wait(2)

        # ============================================================
        # FINAL ANSWER
        # ============================================================

        final_box = SurroundingRectangle(
            simplified,
            buff=0.2
        )

        self.play(
            Create(final_box)
        )

        self.wait(3)