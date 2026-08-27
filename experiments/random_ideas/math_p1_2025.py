from manim import *


class question2(Scene):

    def construct(self):

        # ============================================================
        # 1. TITLE
        # ============================================================

        title = Text(
            "KCSE Mathematics",
            font_size=42
        )

        subtitle = Text(
            "Ratio & Proportion",
            font_size=30
        ).next_to(title, DOWN, buff=0.2)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)

        self.play(
            FadeOut(title),
            FadeOut(subtitle)
        )


        # ============================================================
        # 2. DISPLAY THE QUESTION
        # ============================================================

        question_title = Text(
            "Question",
            font_size=38
        ).to_edge(UP)

        question = VGroup(
            Text(
                "Baraka earns Ksh. 210 per hour",
                font_size=28
            ),
            Text(
                "working at a supermarket.",
                font_size=28
            ),
            Text(
                "The employer changed the amount",
                font_size=28
            ),
            Text(
                "earned per hour in the ratio 8 : 7.",
                font_size=28
            ),
            Text(
                "Determine the amount Baraka would earn",
                font_size=28
            ),
            MathTex(
                r"10\frac{1}{2}\text{ hours}",
                font_size=34
            ),
        ).arrange(DOWN, buff=0.18)

        self.play(Write(question_title))
        self.play(
            LaggedStart(
                *[FadeIn(line, shift=UP) for line in question],
                lag_ratio=0.15
            )
        )

        self.wait(2)

        self.play(
            FadeOut(question),
            FadeOut(question_title)
        )


        # ============================================================
        # 3. EXTRACT THE INFORMATION
        # ============================================================

        heading = Text(
            "Step 1: Identify what we know",
            font_size=34
        ).to_edge(UP)

        original_rate = MathTex(
            r"\text{Original rate} = \text{Ksh. }210\text{/hour}",
            font_size=34
        )

        ratio = MathTex(
            r"\text{New : Original} = 7 : 8",
            font_size=34
        )

        hours = MathTex(
            r"\text{Time} = 10\frac{1}{2}\text{ hours}",
            font_size=34
        )

        information = VGroup(
            original_rate,
            ratio,
            hours
        ).arrange(DOWN, buff=0.45)

        self.play(Write(heading))
        self.play(FadeIn(information, shift=UP))

        self.wait(2)


        # ============================================================
        # 4. EXPLAIN THE RATIO
        # ============================================================

        self.play(
            FadeOut(information),
            FadeOut(heading)
        )

        heading = Text(
            "Step 2: Understand the ratio",
            font_size=34
        ).to_edge(UP)

        self.play(Write(heading))

        ratio_visual = MathTex(
            r"8 : 7",
            font_size=60
        )

        self.play(Write(ratio_visual))

        explanation = Text(
            "The old rate corresponds to 8 parts.",
            font_size=27
        ).next_to(ratio_visual, DOWN, buff=0.5)

        explanation2 = Text(
            "The new rate corresponds to 7 parts.",
            font_size=27
        ).next_to(explanation, DOWN, buff=0.2)

        self.play(FadeIn(explanation))
        self.play(FadeIn(explanation2))

        self.wait(2)


        # ============================================================
        # 5. FIND THE NEW HOURLY RATE
        # ============================================================

        self.play(
            FadeOut(ratio_visual),
            FadeOut(explanation),
            FadeOut(explanation2),
            FadeOut(heading)
        )

        heading = Text(
            "Step 3: Find the new hourly rate",
            font_size=34
        ).to_edge(UP)

        self.play(Write(heading))

        step1 = MathTex(
            r"\text{New rate}"
            r"=",
            r"210\times\frac{7}{8}",
            font_size=42
        )

        self.play(Write(step1))

        self.wait(1)

        step2 = MathTex(
            r"=\frac{1470}{8}",
            font_size=42
        ).next_to(step1, DOWN, buff=0.35)

        self.play(Write(step2))

        step3 = MathTex(
            r"=183.75",
            font_size=48
        ).next_to(step2, DOWN, buff=0.35)

        self.play(Write(step3))

        answer_rate = MathTex(
            r"\boxed{\text{New rate}=\text{Ksh. }183.75\text{/hour}}",
            font_size=38
        ).next_to(step3, DOWN, buff=0.5)

        self.play(
            Create(SurroundingRectangle(answer_rate, buff=0.15)),
            Write(answer_rate)
        )

        self.wait(2)


        # ============================================================
        # 6. CONVERT THE MIXED FRACTION
        # ============================================================

        self.play(
            FadeOut(step1),
            FadeOut(step2),
            FadeOut(step3),
            FadeOut(answer_rate),
            FadeOut(heading)
        )

        heading = Text(
            "Step 4: Convert the working time",
            font_size=34
        ).to_edge(UP)

        self.play(Write(heading))

        mixed = MathTex(
            r"10\frac{1}{2}\text{ hours}",
            font_size=50
        )

        self.play(Write(mixed))

        conversion = MathTex(
            r"10\frac{1}{2}"
            r"=",
            r"\frac{10\times2+1}{2}",
            font_size=42
        ).next_to(mixed, DOWN, buff=0.5)

        self.play(Write(conversion))

        fraction = MathTex(
            r"=\frac{21}{2}",
            font_size=50
        ).next_to(conversion, DOWN, buff=0.4)

        self.play(Write(fraction))

        self.wait(2)


        # ============================================================
        # 7. CALCULATE TOTAL EARNINGS
        # ============================================================

        self.play(
            FadeOut(mixed),
            FadeOut(conversion),
            FadeOut(fraction),
            FadeOut(heading)
        )

        heading = Text(
            "Step 5: Calculate Baraka's earnings",
            font_size=34
        ).to_edge(UP)

        self.play(Write(heading))

        equation = MathTex(
            r"\text{Earnings}"
            r"=",
            r"\text{rate}\times\text{time}",
            font_size=40
        )

        self.play(Write(equation))

        substitution = MathTex(
            r"=183.75\times\frac{21}{2}",
            font_size=45
        ).next_to(equation, DOWN, buff=0.5)

        self.play(Write(substitution))

        calculation = MathTex(
            r"=\frac{3858.75}{2}",
            font_size=45
        ).next_to(substitution, DOWN, buff=0.4)

        self.play(Write(calculation))

        final_value = MathTex(
            r"=1929.375",
            font_size=48
        ).next_to(calculation, DOWN, buff=0.4)

        self.play(Write(final_value))

        self.wait(2)


        # ============================================================
        # 8. FINAL ANSWER
        # ============================================================

        self.play(
            FadeOut(equation),
            FadeOut(substitution),
            FadeOut(calculation),
            FadeOut(final_value),
            FadeOut(heading)
        )

        final_heading = Text(
            "Answer",
            font_size=42
        ).to_edge(UP)

        final_answer = MathTex(
            r"\boxed{\text{Ksh. }1,929.38}",
            font_size=60
        )

        note = Text(
            "Correct to 2 decimal places",
            font_size=27
        ).next_to(final_answer, DOWN, buff=0.4)

        self.play(Write(final_heading))
        self.play(
            Create(SurroundingRectangle(final_answer, buff=0.2)),
            Write(final_answer)
        )
        self.play(FadeIn(note))

        self.wait(3)