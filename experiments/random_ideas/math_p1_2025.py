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
