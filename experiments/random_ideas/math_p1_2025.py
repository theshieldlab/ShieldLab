from manim import *


class question2(Scene):

    def construct(self):

        # ============================================================
        # 1. TITLE
        # ============================================================

        title = Text("KCSE Mathematics P1 2025", font_size=42)

        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))


        #------------ QUESTION2 ------------

        question_number = Text("Question2", font_size=38).to_edge(UL)

        question = VGroup(
            Text("Baraka earns Ksh. 210 per hour working at a supermarket. The employer changed the amount", font_size=28),
            Text("earned per hour in the ratio 8 : 7.", font_size=28),
            Text("Determine the amount Baraka would earn", font_size=28),
            MathTex(r"10\frac{1}{2}\text{ hours}", font_size=34)
        ).next_to(question_number, DOWN, aligned_edge=LEFT, buff=0.5).arrange(DOWN, buff=0.18)

        self.play(Write(question_number))
        self.play(
            LaggedStart(
                *[FadeIn(line, shift=UP) for line in question],
                lag_ratio=0.15
            )
        )

        self.wait(2)


        # --- Working it out---

        heading = Text( "Ratio & Proportion", font_size=34).to_edge(UP)

        #STEM 1 ------------- start with ehat we know

        original_rate = MathTex(r"\text{Original rate} = \text{Ksh. }210\text{/hour}", font_size=34)
        ratio = MathTex(r"\text{ratio} = 8 : 7",font_size=34)
        hours = MathTex(r"\text{Time} = 10\frac{1}{2}\text{ hours}", font_size=34)

        information = VGroup( original_rate, ratio, hours).arrange(DOWN, buff=0.45)

        self.play(Write(heading))
        self.play(FadeIn(information, shift=UP))
        self.wait(2)
        self.play(FadeOut(information), FadeOut(heading))


        # FIND THE NEW HOURLY RATE
        heading = Text("Find the new hourly rate", font_size=34).to_edge(UP)
        self.play(Write(heading))

        step1 = MathTex(r"\text{New rate}" r"=", r"210\times\frac{8}{7}", font_size=42)

        self.play(Write(step1))
        self.wait(1)

        step2 = MathTex(r"=\frac{1680}{7}", font_size=42).next_to(step1, DOWN, buff=0.35)
        self.play(Write(step2))

        step3 = MathTex(r"=240", font_size=48).next_to(step2, DOWN, buff=0.35)
        self.play(Write(step3))

        answer_rate = MathTex(r"\boxed{\text{New rate}=\text{Ksh. }240\text{/hour}}", font_size=38).next_to(step3, DOWN, buff=0.5)
        self.play(Write(answer_rate))

        self.wait(2)

        self.play(FadeOut(step1), FadeOut(step2), FadeOut(step3), FadeOut(answer_rate), FadeOut(heading))


        # ============================================================
        # 6. CONVERT THE MIXED FRACTION
        # ============================================================

        
   # convert the mixed fraction to an improper fraction

        mixed = MathTex(r"10\frac{1}{2}\text{ hours}", font_size=50).move_to(UP*2)
        self.play(Write(mixed))

        conversion = MathTex(r"10\frac{1}{2}" r"=", r"\frac{10\times2+1}{2}", font_size=42).next_to(mixed, DOWN, buff=0.5)
        self.play(Write(conversion))

        fraction = MathTex(r"=\frac{21}{2}", font_size=50).next_to(conversion, DOWN, buff=0.4)
        self.play(Write(fraction))
        self.wait(2)

        self.play(FadeOut(mixed), FadeOut(conversion), FadeOut(fraction), FadeOut(heading))


        #Calculate Baraka's earnings

        equation = MathTex(r"\text{Earnings}" r"=", r"\text{rate}\times\text{time}", font_size=40).move_to(UP*2)
        self.play(Write(equation))

        substitution = MathTex(r"=240\times\frac{21}{2}",font_size=45).next_to(equation, DOWN, buff=0.5)
        self.play(Write(substitution))

        calculation = MathTex(r"=\frac{5040}{2}", font_size=45).next_to(substitution, DOWN, buff=0.4)
        self.play(Write(calculation))

        final_value = MathTex(r"=2520", font_size=48).next_to(calculation, DOWN, buff=0.4)
        self.play(Write(final_value))
        self.wait(2)


        #FINAL ANSWER

        self.play(FadeOut(equation), FadeOut(substitution), FadeOut(calculation), FadeOut(final_value), FadeOut(heading))

        final_answer = MathTex(r"\text{Ksh. }2,520}", font_size=60)
        self.play(Create(SurroundingRectangle(final_answer, buff=0.2)), Write(final_answer))
        self.wait(3)


        