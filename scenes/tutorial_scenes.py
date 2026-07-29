from manim import *

import numpy as np

from manim.mobject.geometry.tips import ArrowSquareTip
from manim.mobject.geometry.tips import ArrowCircleFilledTip


class AnimatedBoundary(Scene):
    def construct(self):
        text = Text("So shiny!")
        boundary = AnimatedBoundary(text, colors =  [RED, GREEN, BLUE],
                                    cycle_rate=3)
        self.add(text, boundary)
        self.wait(2)
        

# Trace the path of a point returned by a function call 

class TracePath(Scene):
    def construct(self):
        circ = Circle(color=RED).shift(4*LEFT)
        dot = Dot (color=RED).move_to(circ.get_start())
        rolling_circle = VGroup(circ, dot)
        trace = TracedPath(circ.get_start)
        rolling_circle.add_updater(lambda m: m.rotate(-0.3))
        self.add(trace, rolling_circle)
        self.play(rolling_circle.animate.shift(8*RIGHT), run_time= 4, rate_function= linear)


#Dissipating path

class DissipatingPath(Scene):
    def construct(self):
        a = Dot(RIGHT*2)
        b = TracedPath(a.get_center, dissipating_time=0.5, stroke_opacity = [0,1])
        self.add(a, b)
        self.play(a.animate(path_arc= PI / 4).shift(LEFT * 2))
        self.play(a.animate(path_arc= PI / 4).shift(LEFT * 2))
        self.wait(2)


# Lagged Start - Adjusts the timimg of a series of Animation according to lag_ratio
# lag_ratio defines the delay after which the animation is applied to submobjects. A lag ration of n.nn means that the next animation will play when nnn% of the current animation has played

class LaggedStart(Scene):
    def construct(self):
        title = Title("Lag_ratio = 0.25").to_edge(UP)

        dot1 = Dot(point=LEFT * 2 + UP, radius = 0.16)
        dot2 = Dot(point = LEFT * 2, radius=0.16)
        dot3 = Dot(point=LEFT * 2 + DOWN, radius = 0.16)
        line_25 = DashedLine(
            start = LEFT + UP * 2,
            end = LEFT + DOWN * 2,
            color =RED
        )
        label = Text ("25%", font_size=24). next_to(line_25, UP)
        self.add(title, dot1, dot2, dot3, line_25, label)


        self.play(LaggedStart(
            dot1.animate.shift(RIGHT*4),
            dot2.animate.shift(RIGHT*4),
            dot3.animate.shift(RIGHT*4),
            lag_ratio=0.25,
            run_time=4
        ))


#LaggedStartMap - Plays a series ofanimation while mapping a function to submobjects

class LaggedStartMap(Scene):
    def construct(self):
        title = Text("LaggedStartMap").to_edge(UP, buff=LARGE_BUFF)
        dots = VGroup(
            *[Dot(radius=0.16) for _ in range (35)]
        ).arrange_in_grid(rows=5, cols=7, buff=MED_LARGE_BUFF)

        self.add(dots, title)

        #Animate yellow ripple effect

        for mob in dots, title:
            self.play(LaggedStartMap(
                ApplyMethod, mob,
                lambda m : (m.set_color, YELLOW),
                lag_ratio = 0.1,
                rate_funct = there_and_back,
                run_time = 2
            ))


#Succession - plays a series of animations in succession

class Succession(Scene):
    def construct(self):
       dot1 = Dot(point= LEFT * 2 + UP * 2, radius= 0.16, color= BLUE)
       dot2 = Dot(point= LEFT * 2 + DOWN * 2, radius= 0.16, color= MAROON)
       dot3 = Dot(point= RIGHT * 2 + DOWN * 2, radius= 0.16, color= GREEN)
       dot4 = Dot(point= RIGHT * 2 + UP * 2, radius= 0.16, color= YELLOW)

       self.add(dot1, dot2, dot3, dot4)

       self.play(Succession(
           dot1.animate.move_to(dot2),
           dot2.animate.move_to(dot3),
           dot3.animate.move_to(dot4),
           dot4.animate.move_to(dot1)
       ))

                   #Creation - Animate the display or removal of a mobject from a scene

                                    #Classes

#1. AddTextLetterByLetter
#2. AddTextWordByWord
#3. Create - Incrementally show a VMobject

class CreateScene(Scene):
    def construct(self):
        self.play(Create(Square))


#4. DrawBorderthenFill
class ShowDrawBorderThenFill(Scene):
    def construct(self):
        self.play(DrawBorderThenFill(Square(fill_opacity= 1, fill_color= BLUE)))


#5. RemovetextletterByLetter
#6. ShowIncreasingsubsets - Show one submobjest at a time, leaving all previous ones displayed on screen

class ShowIncreasingSubsets(Scene):
    def construct(self):
        p = VGroup(Dot(), Square(), Triangle())
        self.add(p)
        self.play(ShowIncreasingSubsets(p))
        self.wait()
        


#7. ShowPartial - Abstract class for animations that show the Vmobject partially
#8. ShowSubmobjectsOneByOne - Show one submobject at a time, removing allpreviously displayed ones from the screen
#9. SpiralIn

class SpiralInExample(Scene):
    def construct(self):
        pi = MathTex(r"\pi").scale(7)
        pi.shift(2.25 * LEFT + 1.5 * UP)
        circle = Circle(color= GREEN, fill_opacity = 1).shift(LEFT)
        square = Square(color = BLUE, fill_opacity = 1).shift(UP)
        shapes = VGroup(pi, circle, square)
        self.play(SpiralIn(shapes))


#10. TypeWithCursor - Similar to add text letter by letter but with an additional cursor mobject at the end

class TypeWithCursorExample(Scene):
    def construct(self):
        text = Text("Inserting", color= PURPLE).scale(1.5).to_edge(LEFT)
        cursor = Rectangle(
            color= GREY_A,
            fill_color = GREY_A,
            fill_opacity = 1,
            height = 1.1,
            width = 0.5,
        ).move_to(text[0])  #position the cursor

        self.play(TypeWithCursor(text, cursor))
        self.play(Blink(cursor, blinks = 2))

#11. Uncreate - reverse of create

class ShowUncreate(Scene):
    def construct(self):
        self.play(Uncreate(Square))


#12. UntypeWithCursor 

class deletingTextExample(Scene):
    def construct(self):
        text = Text("Deleting", color = PURPLE).scale(1.5).to_edge(LEFT)
        cursor = Rectangle(
            color = GREY_A, 
            fill_color = GREY_A,
            fill_opacity = 1,
            height = 1.1,
            width = 0.5,            
        ).move_to(text[0])   #position the cursor

        self.play(UntypeWithCursor(text, cursor))
        self.play(Blink(cursor, blinks = 2))


#13. Unwrite - Simulate erasing by handa text or a Vmobject

class UnwriteReverseTrue(Scene):
    def construct(self):
        text = Tex("Alice and Bob").scale(3)
        self.add(text)
        self.play(Unwrite(text))       #set True to have the animation start erasing from the last submobject first


    #b. Unwrite (False)

class UnwriteReverseFalse(Scene):
    def construct(self):
        text = Tex("Alice and Bob").scale(3)
        self.add(text)
        self.play(Unwrite(text, reverse= False))



#14. Write

  #a.

class ShowWrite(Scene):
    def construct(self):
        self.play(Write(Text("Hello", font_size=144)))


        #b.ShowWriteReversed

class ShowWriteReversed(Scene):
    def construct(self):
        self.play(Write(Text("Hello", font_size = 144, reverse = True, remover = False)))



        # Fading - Fading in and out of view

class Fading(Scene):
    def construct(self):
        tex_in = Tex("Fade", "In").scale(3)
        tex_out = Tex("Fade", "Out").scale(3)
        self.play(FadeIn(tex_in, shift = DOWN, scale = 0.66))
        self.play(ReplacementTransform(tex_in, tex_out))
        self.play(FadeOut(tex_out, shit = DOWN * 2, scale = 1.5))



     #FadeIn

class FadeInExample(Scene):
    def construct(self):
        dot = Dot(UP * 2 + LEFT)
        self.add(dot)
        tex = Tex(
            "FadeIn with ", "shift ", "r or target\_position", " and scale"
        ).scale(1)

        animations = [
            FadeIn(tex[0]),
            FadeIn(tex[1], shift = DOWN),
            FadeIn(tex[2], target_position = dot),
            FadeIn(tex[3], scale = 1.5),
        ]
        self.play(AnimationGroup(*animations, lag_ratio= 0.5))


        #FadeOUt

class FadeOutExample(Scene):
    def construct(self):
        dot = Dot(UP * 2 + LEFT)
        self.add(dot)
        tex = Tex(
            "FadeOut with ", "shift ", "r or target\_position", " and scale"
        ).scale(1)

        animations = [
            FadeOut(tex[0]),
            FadeOut(tex[1], shift = DOWN),
            FadeOut(tex[2], target_position = dot),
            FadeOut(tex[3], scale = 1.5),
        ]
        self.play(AnimationGroup(*animations, lag_ratio= 0.5))



        #Growing - animations that introduce mobjectsto scene by growing them from points

class Growing(Scene):
    def construct(self):
        square = Square()
        circle = Circle()
        triangle = Triangle()
        arrow = Arrow(LEFT, RIGHT)
        star = Star()

        VGroup(square, circle, triangle).set_x(0).arrange(buff=1.5).set_y(2)
        VGroup(arrow, star).move_to(DOWN).set_x(0).arrange(buff = 1.5).set_y(-2)

        self.play(GrowFromPoint(square, ORIGIN))
        self.play(GrowFromCenter(circle))
        self.play(GrowFromEdge(arrow))
        self.play(SpinInFromNothing(star))


        #GRowArrow

class GrowArrowExample(Scene):
    def construct(self):
        arrows = [Arrow(2 * LEFT, 2 * RIGHT), Arrow(2 * DR, 2* UR)]
        VGroup(*arrows).set_x(0).arrange(buff=2)
        self.play(GrowArrow(arrows[0]))
        self.play(GrowArrow(arrows[1], point_color=RED))


        #GrowFromCenter 

class GrowFromCenterExa(Scene):
    def construct(self):
        squares = [Square() for i in range (2)]
        VGroup(*squares).set_x(0).arrange(buff = 2)
        self.play(GrowFromCenter(squares[0]))
        self.play(GrowFromCenter(squares[1], point_color=RED))


        #GrowFromEdge

class GrowFromEdgeExample(Scene):
    def construct(self):
        squares = [Square() for i in range(4)]
        VGroup(*squares).set_x(0).arrange(buff=1)
        self.play(GrowFromEdge(squares[0], DOWN))
        self.play(GrowFromEdge(squares[1], RIGHT))
        self.play(GrowFromEdge(squares[2], UR))
        self.play(GrowFromEdge(squares[3], UP, point_color=RED))


        #GrowFromPoint

class GrowFromPointExapmle(Scene):
    def construct(self):
        dot = Dot(3 * UR, color = GREEN)
        squares = [Square() for i in range(4)]
        VGroup(*squares).set_x(0).arrange(buff = 1)
        self.add(dot)
        self.play(GrowFromPoint(squares[0], ORIGIN))
        self.play(GrowFromPoint(squares[1], [-2, 0, 2]))
        self.play(GrowFromPoint(squares[2], [3, -2, 0], RED))
        self.play(GrowFromPoint(squares[3], dot, dot.get_color()))



    #SpinInFromNothing

class SpinInFromNothingExample(Scene):
    def construct(self):
        squares = [Square() for i in range(3)]
        VGroup(*squares).set_x(0).arrange(buff = 2)
        self.play(SpinInFromNothing(squares[0]))
        self.play(SpinInFromNothing(squares[1], angle= 2* PI))
        self.play(SpinInFromNothing(squares[2], point_color=RED))



             #INDICATION - Animations drawing attention to particular mobject


class Indications(Scene):
    def construct(self):
        indications = [ApplyWave, Circumscribe, Flash, FocusOn, Indicate, ShowPassingFlash, Wiggle]
        names = [Tex(i._name_).scale(3) for i in indications]

        self.add(names[0])
        for i in range(len(names)):
            if indications[i] is Flash:
                self.play(Flash(UP))
            elif indications[i] is ShowPassingFlash:
                self.play(ShowPassingFlash(Underline(names[i])))
            else: 
                self.play(indications[i](names[i]))
            self.play(AnimationGroup(
                FadeOut(names[i], shift = UP*1.5),
                FadeIn(names[(i+1)%len(names)], shift= UP*1.5),
            ))



            #ApplyWave

class ApplyWaveExample(Scene):
    def construct(self):
        tex = Tex("WaveWaveWave").scale(2)
        self.play(ApplyWave(tex))
        self.play(ApplyWave(
            tex,
            direction= RIGHT,
            time_width=0.5,
            amplitude=0.3
        ))
        self.play(ApplyWave(
            tex,
            rate_function = linear,
            ripples=4
        ))


            #Blink

class BlinkExample(Scene):
    def construct(self):
        text = Text("Blinking").sclae(1.5)
        self.add(text)
        self.play(Blink(text, blinks= 3))


        #Circumscribe

class UsingCircumscribe(Scene):
    def construct(self):
        lbl = Tex(r"Circum-\\scribe").scale(2)
        self.add(lbl)
        self.play(Circumscribe(lbl))
        self.play(Circumscribe(lbl, Circle))
        self.play(Circumscribe(lbl, fade_out=True))
        self.play(Circumscribe(lbl, time_width=2))
        self.play(Circumscribe(lbl, Circle, True))


        #FLASH - send out lines in all directions

class UsingFlash(Scene):
    def construct(self):
        dot = Dot(color=YELLOW).shift(DOWN)
        self.add(Tex("Flash the dot below:"), dot)
        self.play(Flash(dot))
        self.wait()


        #flash on circle

class flashOnCircle(Scene):
    def construct(self):
        radius = 2
        circle = Circle(radius)
        self.add(circle)
        self.play(Flash(
            circle, line_length=1,
            num_lines= 30, color = RED,
            flash_radius = radius+SMALL_BUFF,
            time_width= 0.3, run_time=2,
            rate_func = rush_from
        ))



        #FocusOn

class UsingFocusOn(Scene):
    def construct(self):
        dot = Dot(color=YELLOW).shift(DOWN)
        self.add(Tex("Focusing on the dot below:"), dot)
        self.play(FocusOn(dot))
        self.wait()
        

        #Indicate

class UsingIndicate(Scene):
    def construct(self):
        tex = Tex("Indicate").scale(3)
        self.play(Indicate(tex))
        self.wait()


        #ShowPassingFlash - show only a sliver of the VMobject each frame

class TimeWidthValues(Scene):
    def construct(self):
        p = RegularPolygon(5, color = DARK_GRAY, stroke_width=6).scale(3)
        lbl = VMobject()
        self.add(p, lbl)
        p = p.copy().set_color(BLUE)
        for time_width in [0.2, 0.5, 1, 2]:
            lbl.become(Tex(r"\texttt{time\_width={{%.1f}}}"%time_width))
            self.play(ShowPassingFlash(
                p.copy().set_color(BLUE),
                run_time = 2,
                time_width=time_width
            ))



            #Wiggle

class ApplyingWaves(Scene):
    def construct(self):
        tex = Tex("Wiggle").scale(3)
        self.play(Wiggle(tex))
        self.wait()


        #Movement- Animations related to movement

        #classes 
           #1- ComplexHomotopy


           #2- Homotopy - An animation transforming the points of a mobject according to the specified transformation function. With the parameter t moving from 0 to 1 throughoutthe animation and (x,y,z) describing the coordinates of the point of a mobject, the function passed to the homotopy keyword argument shold transform the tuple(x,y,z,t) to (x', y', z'), the coordinates of the original point is transformed to at time t

class HomotopyEx(Scene):

    def construct(self):
        square = Square()

        def homotopy(x, y, z, t):
            if t <= 0.25:
                progress = t / 0.25
                return (x, y + progress * 0.2 *np.sin(x), z)
            else:
                wave_progress = (t - 0.25) / 0.75
                return (x, y + 0.2 * np.sin(x + 10 * wave_progress), z)
            
        self.play(Homotopy(homotopy, square, rate_func= linear, run_time=2))


           #3- MovealongPath - Make one object move along the path of another object

class MoveAlongPath(Scene):
    def construct(self):
        d1 = Dot().set_color(ORANGE)
        l1 = Line(LEFT, RIGHT)
        l2 = VMobject()

        self.add(d1, l1, l2)
        l2.add_updater(lambda x: x.become(Line(LEFT, d1.get_center()).set_color(ORANGE)))

        self.play(MoveAlongPath(d1, l1), rate_func= linear)

           #4- SmoothedVectorizedHomotopy


           # NUMBERS - Animations for changing numbers

    #1. ChangeDecimalToValue - Animate a decimal number to a target value using linear interpolation(0,, 0.01..., 10.00)

class ChangeDecimalToValue(Scene):
    def construct(self):
        number = DecimalNumber(0)
        self.add(number)
        self.play(ChangeDecimalToValue(number, 10, run_time = 3))
        self.wait()



    #2. ChangingDecimal- Animate a decimal number to values specified by a user-supplied function

class ChangingDecimal(Scene):
    def construct(self):
        number = DecimalNumber(0)
        self.add(number)
        self.play(
            ChangingDecimal(
            number,
            lambda a: 5 * a,
            run_time = 3
            )
        )
        self.wait()

 
       # ROTATION

       #1. Rotate - animation that rotates a Mobject

class UsingRotate(Scene):
    def construct(self):
        self.play(
            Rotate( 
                Square(side_length=0.5).shift(UP * 2), 
                angle=2 * PI, 
                about_point=ORIGIN, 
                rate_func=linear, 
            ),
            Rotate(Square(side_length=0.5), angle=2*PI, rate_func=linear))
        

       #2. Rotating -  Animation that rotates a Mobject

class RotatingDemo(Scene):
     def construct(self):
         circle = Circle(radius=1, color=BLUE)
         line = Line(start=ORIGIN, end=RIGHT)
         arrow = Arrow(start=ORIGIN, end=RIGHT, buff=0, color=GOLD)
         vg = VGroup(circle,line,arrow)
         self.add(vg)
         anim_kw = {"about_point": arrow.get_start(), "run_time": 1} 
         self.play(Rotating(arrow, 180*DEGREES, **anim_kw))
         self.play(Rotating(arrow, PI, **anim_kw))
         self.play(Rotating(vg, PI, about_point=RIGHT))
         self.play(Rotating(vg, PI, axis=UP, about_point=ORIGIN))
         self.play(Rotating(vg, PI, axis=RIGHT, about_edge=UP))
         self.play(vg.animate.move_to(ORIGIN))



# RotatingDifferentAxis

class RotatingDifferentAxis(ThreeDScene): 
    def construct(self): 
        axes = ThreeDAxes()
        cube = Cube()
        arrow2d = Arrow(start=[0, -1.2, 1], end=[0, 1.2, 1], color=YELLOW_E)
        cube_group = VGroup(cube,arrow2d)
        self.set_camera_orientation(gamma=0, phi=40 * DEGREES, theta=40 * DEGREES)
        self.add(axes, cube_group)
        play_kw = {r"\run_time": 1.5} 
        self.play(Rotating(cube_group, PI), **play_kw) 
        self.play(Rotating(cube_group, PI, axis=UP), *play_kw) 
        self.play(Rotating(cube_group, 180 * DEGREES, axis=RIGHT), **play_kw)
        self.wait(0.5)

    #specialized

    #class: Broadcast - broadcast a mobject starting from an initial-width, up to the actual sixe of the mobject

class Broadcast(Scene):
    def construct(self):
        mob = Circle(radius=4, color=TEAL_A)
        self.play(Broadcast(mob))

        ChangeSpeed

        #SpeedModifier - Utilities for modifying the speed at which animations are played
#clasess - ChangeSpeed - Modifies the speed of passed animation

#SpeedModifierExample

class SpeedModifierExample(Scene):
     def construct(self):
         a = Dot().shift(LEFT * 4)
         b = Dot().shift(RIGHT * 4)
         self.add(a, b)
         self.play( 
             ChangeSpeed( 
                 AnimationGroup( 
                     a.animate(run_time=1).shift(RIGHT * 8), 
                     b.animate(run_time=1).shift(LEFT * 8),                 
                ), 
                speedinfo={0.3: 1, 0.4: 0.1, 0.6: 0.1, 1: 1},
                rate_func=linear, 
             ) 
         )

#SpeedModifierUpdaterExample

class SpeedModifierUpdaterExample(Scene): 
    def construct(self): 
        a = Dot().shift(LEFT * 4) 
        self.add(a)

        ChangeSpeed.add_updater(a, lambda x, dt: x.shift(RIGHT * 4 * dt))
        self.play(
             ChangeSpeed(
                  Wait(2), 
                  speedinfo={0.4: 1, 0.5: 0.2, 0.8: 0.2, 1: 1},
                    affects_speed_updaters=True, ))

#SpeedModifierUpdaterExample2

class SpeedModifierUpdaterExample2(Scene): 
    def construct(self): 
        a = Dot().shift(LEFT * 4)
        self.add(a)

        ChangeSpeed.add_updater(a, lambda x, dt: x.shift(RIGHT * 4 * dt)) 
        self.wait() 
        self.play(
            ChangeSpeed(
              Wait(), 
              speedinfo={1: 0}, 
              affects_speed_updaters=True

         ) 
     )
        
        #TRANSFORM

        #1. ApplyComplexFunction

        #2. ApplyFunction

        #3. ApplyMatrix - Applies a matrix transform to a mobject

class ApplyMatrixExample(Scene):
     def construct(self):
         matrix = [[1, 1], [0, 2/3]]
         self.play(ApplyMatrix
                   (matrix, 
                    Text("Hello World!")),
                    ApplyMatrix(matrix, NumberPlane()))

        #4. ApplyMethod - animates a mobject by applying a method

        #5. ApplyPointWiseFunction - animation that applies a pointwise function to a mobject

class WarpSquare(Scene):
     def construct(self): 
        square = Square() 
        self.play(
             ApplyPointwiseFunction(
                  lambda point: complex_to_R3(np.exp(R3_to_complex(point))), square ) )
        self.wait()


        #6. ApplyPointWiseFunctionToCenter 

        #7. ClockwiseTransform - Transforms the points of a mobject along a clockwise oriented arc

class ClockwiseExample(Scene): 
    def construct(self):
         dl, dr = Dot(), Dot() 
         sl, sr = Square(), Square()

         VGroup(dl, sl).arrange(DOWN).shift(2 * LEFT)
         VGroup(dr, sr).arrange(DOWN).shift(2 * RIGHT)

         self.add(dl, dr) 
         self.wait() 
         self.play(
              ClockwiseTransform(dl, sl), 
              Transform(dr, sr)
         ) 

         self.wait()


#8. CounterClockWiseTransform - Transforms the points of a mobject along a counterclockwise oriented arc

class CounterclockwiseTransform_vs_Transform(Scene): 
    def construct(self):

        #set up the numbers
        c_transform = VGroup(DecimalNumber(number=3.141, num_decimal_places=3), DecimalNumber(number=1.618, num_decimal_places=3)) 
        text_1 = Text("CounterclockwiseTransform", color=RED) 
        c_transform.add(text_1)

        transform = VGroup(DecimalNumber(number=1.618, num_decimal_places=3), DecimalNumber(number=3.141, num_decimal_places=3)) 
        text_2 = Text("Transform", color=BLUE) 
        transform.add(text_2)

        ints = VGroup(c_transform, transform) 
        texts = VGroup(text_1, text_2).scale(0.75) 
        c_transform.arrange(direction=UP, buff=1) 
        transform.arrange(direction=UP, buff=1)

        ints.arrange(buff=2) 
        self.add(ints, texts)

        #The mobs move in clockwise direction for ClockwiseTransform()
        self.play(CounterclockwiseTransform(c_transform[0], c_transform[1]))

        #The mobs move straight up for Transform()

        self.play(Transform(transform[0], transform[1]))




        #9. CyclicReplace - an animation moving mobjects cyclically 
class CyclicReplaceExample(Scene): 
    def construct(self): 
        group = VGroup(Square(), Circle(), Triangle(), Star()) 
        group.arrange(RIGHT) 
        self.add(group)

        for _ in range(4): self.play(CyclicReplace(*group))


        #10. FadeToColor - Animation that changes color of a mobject

class FadeToColorExample(Scene): 
    def construct(self): 
        self.play(FadeToColor(Text("Hello World!"), color=RED))


        #11. FadeTransform - Fades one mobject into aother

class DifferentFadeTransforms(Scene): 
    def construct(self): 
        starts = [Rectangle(width=4, height=1) for _ in range(3)] 
        VGroup(starts).arrange(DOWN, buff=1).shift(3 * LEFT) 
        targets = [Circle(fill_opacity=1).scale(0.25) for _ in range(3)] 
        VGroup(targets).arrange(DOWN, buff=1).shift(3 * RIGHT)

        self.play(*[FadeIn(s) for s in starts]) 
        self.play( 
            FadeTransform(starts[0], targets[0], stretch=True), 
            FadeTransform(starts[1], targets[1], stretch=False, dim_to_match=0), 
            FadeTransform(starts[2], targets[2], stretch=False, dim_to_match=1) 
        )

        self.play(*[FadeOut(mobj) for mobj in self.mobjects])


        #12. FadeTransformPieces - Fades submobjects of one mobject into submobjects of another one

class FadeTransformSubmobjects(Scene): 
    def construct(self): 
        src = VGroup(Square(), Circle().shift(LEFT + UP)) 
        src.shift(3*LEFT + 2*UP) 
        src_copy = src.copy().shift(4*DOWN)

        target = VGroup(Circle(), Triangle().shift(RIGHT + DOWN)) 
        target.shift(3*RIGHT + 2*UP) 
        target_copy = target.copy().shift(4*DOWN)

        self.play(FadeIn(src), FadeIn(src_copy)) 
        self.play( FadeTransform(src, target), FadeTransformPieces(src_copy, target_copy) ) 
        self.play(*[FadeOut(mobj) for mobj in self.mobjects])


        #13. MoveToTarget - Transforms a mobject to the mobject stored in its target attribute

class MoveToTargetExample(Scene): 
    def construct(self): 
        c = Circle()

        c.generate_target() 
        c.target.set_fill(color=GREEN, opacity=0.5) 
        c.target.shift(2*RIGHT + UP).scale(0.5)

        self.add(c) 
        self.play(MoveToTarget(c))



        #14. ReplacementTransform - Replaces and morphs a mobject into a target mobject

class ReplacementTransformOrTransform(Scene): 
    def construct(self):

                      #set up the numbers
        r_transform = VGroup(*[Integer(i) for i in range(1,4)]) 
        text_1 = Text("ReplacementTransform", color=RED) 
        r_transform.add(text_1)

        transform = VGroup(*[Integer(i) for i in range(4,7)]) 
        text_2 = Text("Transform", color=BLUE) 
        transform.add(text_2)

        ints = VGroup(r_transform, transform) 
        texts = VGroup(text_1, text_2).scale(0.75) 
        r_transform.arrange(direction=UP, buff=1) 
        transform.arrange(direction=UP, buff=1)

        ints.arrange(buff=2) 
        self.add(ints, texts)

        #The mobs replace each other and none are left behind
        self.play(ReplacementTransform(r_transform[0], r_transform[1])) 
        self.play(ReplacementTransform(r_transform[1], r_transform[2]))

        #The mobs linger after the Transform()
        self.play(Transform(transform[0], transform[1])) 
        self.play(Transform(transform[1], transform[2])) 
        self.wait()

        

        #15. Restore - Transforms a mobject to its last saved state

class RestoreExample(Scene): 
    def construct(self): 
        s = Square() 
        s.save_state() 
        self.play(FadeIn(s)) 
        self.play(s.animate.set_color(PURPLE).set_opacity(0.5).shift(2*LEFT).scale(3)) 
        self.play(s.animate.shift(5*DOWN).rotate(PI/4)) 
        self.wait() 
        self.play(Restore(s), run_time=2)

        #16. ScaleInPlace - scales a mobject by a certain factor

class ScaleInPlaceExample(Scene): 
    def construct(self): 
        self.play(ScaleInPlace(Text("Hello World!"), 2))


        #17. ShrinkToCenter - Makes a mobject shrink to center

class ShrinkToCenterExample(Scene): 
    def construct(self): 
        self.play(ShrinkToCenter(Text("Hello World!")))


        #18. Swap


        #19. Transform - Transforms a mobject into a target mobject

#TransformPathArc

class TransformPathArc(Scene): 
    def construct(self): 
        def make_arc_path(start, end, arc_angle): 
            points = [] 
            p_fn = path_along_arc(arc_angle)

                #alpha animates between 0.0 and 1.0, where 0.0 is the beginning of the animation and 1.0 is the end.
            for alpha in range(0, 11): 
                points.append(p_fn(start, end, alpha / 10.0)) 
                
            path = VMobject(stroke_color=YELLOW) 
            path.set_points_smoothly(points) 
            return path

        left = Circle(stroke_color=BLUE_E, fill_opacity=1.0, radius=0.5).move_to(LEFT * 2) 
        colors = [TEAL_A, TEAL_B, TEAL_C, TEAL_D, TEAL_E, GREEN_A]

                #Positive angles move counter-clockwise, negative angles move clockwise.
        examples = [-90, 0, 30, 90, 180, 270] 
        anims = [] 
        for idx, angle in enumerate(examples): 
            left_c = left.copy().shift((3 - idx) * UP) 
            left_c.fill_color = colors[idx] 
            right_c = left_c.copy().shift(4 * RIGHT) 
            path_arc = make_arc_path(left_c.get_center(), right_c.get_center(), arc_angle=angle * DEGREES) 
            desc = Text('%d°' % examples[idx]).next_to(left_c, LEFT)

                 #Make the circles in front of the text in front of the arcs.
            self.add( 
                path_arc.set_z_index(1), 
                desc.set_z_index(2), 
                left_c.set_z_index(3)
             ) 
            anims.append(Transform(left_c, right_c, path_arc=angle * DEGREES))

        self.play(*anims, run_time=2) 
        self.wait()


        #20. TransformAnimations 

        #21. TransformFromCopy - Perform a reversed transform

        #22. TransformMatchingTex - trys to transform rendered LaTex strings

        #23. TransformMatchingAbstractBase

        #24. TransformMatchingShapes - trys to transform groups by matching the shape of their submobjects

class Anagram(Scene): 
    def construct(self): 
        src = Text("the morse code") 
        tar = Text("here come dots") 
        self.play(Write(src)) 
        self.wait(0.5) 
        self.play(TransformMatchingShapes(src, tar, path_arc=PI/2)) 
        self.wait(0.5)


        #25. TransformMatchingTex - trys to transform rendered LaTex strings

class MatchingEquationParts(Scene): 
    def construct(self): 
        variables = VGroup(MathTex("a"), MathTex("b"), MathTex("c")).arrange_submobjects().shift(UP)

        eq1 = MathTex("{{x}}^2", "+", "{{y}}^2", "=", "{{z}}^2") 
        eq2 = MathTex("{{a}}^2", "+", "{{b}}^2", "=", "{{c}}^2") 
        eq3 = MathTex("{{a}}^2", "=", "{{c}}^2", "-", "{{b}}^2")

        self.add(eq1) 
        self.wait(0.5) 
        self.play(TransformMatchingTex(Group(eq1, variables), eq2)) 
        self.wait(0.5) 
        self.play(TransformMatchingTex(eq2, eq3)) 
        self.wait(0.5)



        # UPDATERS - animations and utility related to update functions

        #1. mobject_update_utils

        #a. tangent animation Ex

class TangentAnimation(Scene):
    def construct(self):
        ax = Axes()
        sine = ax.plot(np.sin, color= RED)
        alpha = ValueTracker(0)
        point = always_redraw(
            lambda: Dot(
                sine.point_from_proportion(alpha.get_value()),
                color=BLUE
            )
        )
        tangent = always_redraw(
            lambda: TangentLine(
                sine,
                alpha= alpha.get_value(),
                color= YELLOW,
                length = 4
            )
        )

        self.add(ax, sine, point, tangent)
        self.play(alpha.animate.set_value(1), rate_func = linear, run_time = 2)



        #b. SPINNING TRIANGLE Ex

class SpinningTriangle(Scene):
    def construct(self):
        tri = Triangle().set_fill(opacity=1).set_z_index(2)
        sq = Square().to_edge(LEFT)

        #will keep spinning while there's an animation going on

        always_rotate(tri, rate=2*PI, about_point= ORIGIN)

        self.add(tri, sq)
        self.play(sq.animate.to_edge(RIGHT), rate_func= linear, run_time = 1)



        #c. shifting square

class ShiftingSquare(Scene):
    def construct(self):
        sq = Square().set_fill(opacity=1)
        tri = Triangle()

        VGroup(sq, tri).arrange(LEFT)

        #construct a square which is continuously shifted to the right
        always_shift(sq, RIGHT, rate=5)

        self.add(sq)
        self.play(tri.animate.set_fill(opacity=1))


        #   WELCOME TO MANIM  - INTRO AND LOGO

class WelcomeToManim(Scene):
    def construct(self):
        words = Text("Welcome to")
        banner = ManimBanner().scale(0.5)
        VGroup(words, banner).arrange(DOWN)

        turn_animation_into_updater(Write(words, run_time=0.9))
        self.add(words)
        self.wait(0.5)
        self.play(banner.expand(), run_time= 0.5)


        # UPDATE - Animations that update mobjects

        #1. MaintainPositionRelativeTo
        #2. UpdateFromAlphaFunc
        #3. UpdateFromFunc


    #CAMERAS

    #1. camera - converts the mobjects contained in a scene into an array of pixels
    #a. BackgroundColoredMobjectDisplayer - Auxilliary class that handles displaying vectorized mobjects with a set background image
    #b. Camera - Base camera class


    #2. mapping_camera - A camera module that supports spacial mapping between mobjects for distortion effects
    #a. mappingCamera
    #2. OldMultiCamera
    #3. SplitScreenCamera - Initializes a split screen camera setup with two side by side cameras


    #3. moving camera - A camera that can span, zoom through a scene
    #a. MovingCamera - A camera that follows and matches the size and position of its 'frame', a rectangle(or similar Mobject)


    #4. multi_camera - A camera supporting multiple perspectives

    #5. three_d_camera - A camera that can be positioned and oriented in 3d space
    #a. ThreeDCamera - Initialized the 3d camera


    #............................MOBJECTS......................................

    #1. .....frame - special rectangle

    #a.FullScreenRectangle
    #b. ScreenRectangle


    #2. ..............geometry - various geometric mobjects

    #a. arc - mobjects that are curved

class UsefulAnnotations(Scene):
    def construct(self):
        m0= Dot()
        m1 = AnnotationDot()
        m2 = LabeledDot("ii")
        m3 = LabeledDot(MathTex(r"\alpha")).set_color(ORANGE)
        m4 = CurvedArrow(2 * LEFT, 2 * RIGHT, radius = -5)
        m5 = CurvedArrow(2 * LEFT, 2 * RIGHT, radius = 8)
        m6 = CurvedDoubleArrow(ORIGIN, 2 * RIGHT)

        self.add(m0, m1, m2, m3, m4, m5, m6)
        for i, mobj in enumerate(self.mobjects):
            mobj.shift(DOWN * (i-3))

    #...classes... ARc
    #1. AnnotationDot - A dot with bigger radius and bold stroke to annotate scenes

    #2. AnnularSector - a sector of an annulus

class AnnularSector(Scene):
    def construct(self):
        self.camera.background_color= WHITE  #chages background color for clear visuals

        s1 = AnnularSector(color = YELLOW).move_to(2 * UL) # the default parameter start_angle is 0, so the AnnularSector starts from the +x-axis

                  #different inner_radius and outer_radius than the default
        s2 = AnnularSector(inner_radius = 1.5, outer_radius = 2, angle=45 * DEGREES, color=RED).move_to(2 * UR)
                 #fill_opacity is typically a number >0 and <=1. If 0, the mobject is transparent
        s3 = AnnularSector(inner_radius= 1, outer_radius=1.5, angle= PI, fill_opacity=0.25, color=BLUE).move_to(2 *DL)
                    #With a negative value for the angle, the Annularsector is drawn clockwise from the start value
        s4 = AnnularSector(inner_radius= 1, outer_radius=1.5, angle= -3 * PI / 2, color=GREEN).move_to(2 *DR)

        self.add(s1, s2, s3, s4)



    #3. Annulus - Region b3n 2 concentric circles

class AnnulusEx(Scene):
    def construct(self):
        annulus1 = Annulus(inner_radius=0.5, outer_radius=1).shift(UP)
        annulus2 = Annulus(inner_radius=0.3, outer_radius=0.6, color= RED).next_to(annulus1, DOWN)
        self.add(annulus1, annulus2)

    #4. Arc - a circlular arc

class ArcExamole(Scene):
    def construct(self):
        self.add(Arc(angle= PI))


    #5. ArcBetweenPoints - Inherits from Arc and additionally takes 2 points b2n which the arc is spanned

class ArcB2nPoints(Scene):
    def construct(self):
        circle= Circle(radius=2, stroke_color= GREY)
        dot1= Dot(color= GREEN).move_to([2, 0, 0]).scale(0.5)
        dot1_text= Tex("(2,0)").scale(0.5).next_to(dot1, RIGHT).set_color(BLUE)

        dot2= Dot(color= GREEN).move_to([0, 2, 0]).scale(0.5)
        dot2_text= Tex("(0,2)").scale(0.5).next_to(dot2, UP).set_color(BLUE)

        arc= ArcBetweenPoints(start=2 * RIGHT, end =2 * UP, stroke_color = YELLOW)

        self.add(circle, dot1, dot2, dot1_text, dot2_text)
        self.play(Create(arc))
     
    #6. ArcPolygon - A generalized polygon allowing for points to be connected with arcs 

class SeveralArcPolygons(Scene):
    def construct(self):
        a =[0, 0, 0]
        b= [2, 0, 0]
        c= [0, 2, 0]

        ap1= ArcPolygon(a, b, c, radius=2)
        ap2= ArcPolygon(a, b, c, angle=45 * DEGREES)
        ap3= ArcPolygon(a, b, c, arc_config={'radius': 1.7, 'color': RED})
        ap4= ArcPolygon(a, b, c, color= RED, fill_opacity = 1,
                        arc_config=[{'radius' : 1.7, 'color': RED},
                                    {'angle': 20 * DEGREES, 'color': BLUE},
                                    {'radius': 1}])
        ap_group = VGroup(ap1, ap2, ap3, ap4).arrange()
        self.play(*[Create(ap) for ap in [ap1, ap2, ap3, ap4]])
        self.wait()

    #7. ArcPolygonFromArcs - A generalized polygon allowing for points to be connected with arcs

class ArcPolygonEx1(Scene):
    def construct(self):
        arc_conf = {"stroke_width": 0}
        poly_conf = {"stroke_width": 10, "stroke_color": BLUE,
                     "fill_opacity": 1, "color": PURPLE}
        a = [-1, 0, 0]
        b = [1, 0, 0]
        c= [0, np.sqrt(3), 0]
        arc0 = ArcBetweenPoints(a, b, radius=2, **arc_conf)
        arc1 = ArcBetweenPoints(b, c, radius=2, **arc_conf)
        arc2 = ArcBetweenPoints(c, a, radius=2, **arc_conf)
        reuleaux_tri = ArcPolygonFromArcs(arc0, arc1, arc2, **poly_conf)
        self.play(FadeIn(reuleaux_tri))
        self.wait(2)

#Example2

class ArcPolygonEx2(Scene):
    def construct(self):
        arc_conf = {"stroke_width": 3, "stroke_color": BLUE,
                    "fill_opacity": 0.5, "color": GREEN}
        poly_conf = {"color": None}
        a = [-1, 0, 0]
        b = [1, 0, 0]
        c= [0, np.sqrt(3), 0]
        arc0 = ArcBetweenPoints(a, b, radius=2, **arc_conf)
        arc1 = ArcBetweenPoints(b, c, radius=2, **arc_conf)
        arc2 = ArcBetweenPoints(c, a, radius=2, stroke_color= RED)
        reuleaux_tri = ArcPolygonFromArcs(arc0, arc1, arc2, **poly_conf)
        self.play(FadeIn(reuleaux_tri))
        self.wait(2)


    #8. Circle - a circle

class CirclesExample(Scene):
    def construct(self):
        circle1 = Circle(radius = 1)
        circle2 = Circle(radius = 1.5, color= GREEN)
        circle3 = Circle(radius=1, color= BLUE_B, fill_opacity = 1)

        circ_group = Group(circle1, circle2, circle3).arrange(buff=1)
        self.add(circ_group)

#CircleFromPoints

class CircleFromPointExample(Scene):
    def construct(self):
        circle = Circle.from_three_points(LEFT, LEFT + UP, UP*2, color=RED)

        dots = VGroup(
            Dot(LEFT),
            Dot(LEFT + UP),
            Dot(UP * 2),
        )
        self.add(NumberPlane(), circle, dots)

#pointAtAngle
class PointAtAngle(Scene):
    def construct(self):
        circle = Circle(radius=2.0)
        p1 = circle.point_at_angle(PI / 2)
        p2 = circle.point_at_angle(270 * DEGREES)

        s1 = Square(side_length=0.25). move_to(p1)
        s2 = Square(side_length=0.25).move_to(p2)
        self.add(circle, s1, s2)

#CircleSurround

class CircleSurround(Scene):
    def construct(self):
        triangle1 = Triangle()
        circle1 = Circle(). surround(triangle1)
        group1 = Group(triangle1, circle1) # treat the two mobjects a s one

        line2 = Line()
        circle2 = Circle().surround(line2, buffer_factor=2.0)
        group2 = Group(line2, circle2)

        #Buff-factor <1, so the circle is less than the square

        square3 = Square()
        circle3 = Circle().surround(square3, buffer_factor=0.5)
        group3 = Group(square3, circle3)

        group = Group(group1, group2, group3). arrange(buff=1)
        self.add(group)


    #9. CubicBezier - A cubic Bezier curve

class BezierSpline(Scene):
    def construct(self):
        p1 = np.array([-3, 1, 0])
        p1b = p1 + [1, 0, 0]
        d1 = Dot(point=p1).set_color(BLUE)
        l1= Line(p1, p1b)
        p2 = np.array([3, -1, 0])
        p2b = p2 - [1, 0, 0]
        d2 = Dot(point=p2).set_color(RED)
        l2 = Line(p2, p2b)
        bezier = CubicBezier(p1b, p1b + 3 * RIGHT, p2b - 3 *RIGHT, p2b)
        self.add(l1, d1, l2, d2, bezier)

    #10. CurvedArrow

    #11. CurvedDoubleArrow


    #12. Dot - A circle with a very small radius

class DotEx(Scene):
    def construct(self):
        dot1 = Dot(point=LEFT, radius=0.08)
        dot2 = Dot(point=ORIGIN)
        dot3 = Dot(point=RIGHT) 
        self.add(dot1, dot2, dot3)

    #13. Ellipse - A circular shape: oval, circle

class EllipseExampl(Scene):
    def construct(self): 
        ellipse_1 = Ellipse(width=2.0, height=4.0, color=BLUE_B) 
        ellipse_2 = Ellipse(width=4.0, height=1.0, color=BLUE_D) 
        ellipse_group = Group(ellipse_1,ellipse_2).arrange(buff=1) 
        self.add(ellipse_group)

    #14. LabeledDot - A dot containing a label in its center

class SeveralLabeledDots(Scene): 
    def construct(self): 
        sq = Square(fill_color=RED, fill_opacity=1) 
        self.add(sq) 
        dot1 = LabeledDot(Tex("42", color=RED)) 
        dot2 = LabeledDot(MathTex("a", color=GREEN)) 
        dot3 = LabeledDot(Text("ii", color=BLUE)) 
        dot4 = LabeledDot("3") 
        dot1.next_to(sq, UL) 
        dot2.next_to(sq, UR) 
        dot3.next_to(sq, DL) 
        dot4.next_to(sq, DR) 
        self.add(dot1, dot2, dot3, dot4)

    #15. Sector - a sector of a circle 

class ExampleSector(Scene): 
    def construct(self): 
        sector = Sector(radius=2) 
        sector2 = Sector(radius=2.5, angle=60*DEGREES).move_to([-3, 0, 0]) 
        sector.set_color(RED) 
        sector2.set_color(PINK) 
        self.add(sector, sector2)

    #16. TangentialArc - Construct an arc that is tangent to 2 intersectig lines

class TangentialArcExample(Scene): 
    def construct(self): 
        line1 = DashedLine(start=3 * LEFT, end=3 * RIGHT) 
        line1.rotate(angle=31 * DEGREES, about_point=ORIGIN) 
        line2 = DashedLine(start=3 * UP, end=3 * DOWN) 
        line2.rotate(angle=12 * DEGREES, about_point=ORIGIN)

        arc = TangentialArc(line1, line2, radius=2.25, corner=(1, 1), color=TEAL) 
        self.add(arc, line1, line2)

    #17. TipableVMobject - Meant for shared functionality b2n Arc and Line

          
    #b. Booloean_ops - Boolean ops for 2d mobjecs

#a. Difference- subtracts one Vmobject from another one

class DifferenceExample(Scene): 
    def construct(self): 
        sq = Square(color=RED, fill_opacity=1) 
        sq.move_to([-2, 0, 0]) 
        cr = Circle(color=BLUE, fill_opacity=1) 
        cr.move_to([-1.3, 0.7, 0]) 
        un = Difference(sq, cr, color=GREEN, fill_opacity=1) 
        un.move_to([1.5, 0, 0]) 
        self.add(sq, cr, un)

#b. Exclusion - Find the XOR b2n 2 mobjects

class IntersectionExample(Scene): 
    def construct(self): 
        sq = Square(color=RED, fill_opacity=1) 
        sq.move_to([-2, 0, 0]) 
        cr = Circle(color=BLUE, fill_opacity=1) 
        cr.move_to([-1.3, 0.7, 0]) 
        un = Exclusion(sq, cr, color=GREEN, fill_opacity=1) 
        un.move_to([1.5, 0.4, 0]) 
        self.add(sq, cr, un)


#c. Intersection - Find the intersection of 2 Vmobjects

class IntersectionExample(Scene): 
    def construct(self): 
        sq = Square(color=RED, fill_opacity=1) 
        sq.move_to([-2, 0, 0]) 
        cr = Circle(color=BLUE, fill_opacity=1) 
        cr.move_to([-1.3, 0.7, 0]) 
        un = Intersection(sq, cr, color=GREEN, fill_opacity=1) 
        un.move_to([1.5, 0, 0]) 
        self.add(sq, cr, un)

#d. Union - Union of 2 or more VMobjects

class UnionExample(Scene): 
    def construct(self): 
        sq = Square(color=RED, fill_opacity=1) 
        sq.move_to([-2, 0, 0]) 
        cr = Circle(color=BLUE, fill_opacity=1) 
        cr.move_to([-1.3, 0.7, 0]) 
        un = Union(sq, cr, color=GREEN, fill_opacity=1) 
        un.move_to([1.5, 0.3, 0]) 
        self.add(sq, cr, un)

    #c. labled - Mobjects that inherit from lines and contain a label along the path

#a. Label - A label consisting of text surrounded by a frame

class LabelExample(Scene): 
    def construct(self): 
        label = Label( 
            label=Text('Label Text', font='sans-serif'), 
            box_config = { 
                "color" : BLUE, 
                "fill_opacity" : 0.75 
            } 
        ) 
        label.scale(3) 
        self.add(label)


#b. LabeledArrow - Constructs an arrow containing a label box somewhere along its length

class LabeledArrowExample(Scene): 
    def construct(self): 
        l_arrow = LabeledArrow("0.5", start=LEFT * 3, end=RIGHT * 3 + UP*2, label_position=0.5)

        self.add(l_arrow)

#c. LabeledLine - Constructs a line containing a label box somewhere along its length

class LabeledLineExample(Scene): 
    def construct(self): 
        line = LabeledLine( 
            label = '0.5', 
            label_position = 0.8, 
            label_config = { 
                "font_size" : 20 
            }, 
            start=LEFT+DOWN, 
            end=RIGHT+UP)

        line.set_length(line.get_length() * 2) 
        self.add(line)

#d. LabeledPolygram - Constructs a polygram containing a labeled box as its pole of inaccessibility

class LabeledPolygon(Scene):
    def construct(self):
        #define rings
        ring1 = [ 
            [-3.8, -2.4, 0], [-2.4, -2.5, 0], [-1.3, -1.6, 0], [-0.2, -1.7, 0], 
            [1.7, -2.5, 0], [2.9, -2.6, 0], [3.5, -1.5, 0], [4.9, -1.4, 0], 
            [4.5, 0.2, 0], [4.7, 1.6, 0], [3.5, 2.4, 0], [1.1, 2.5, 0], 
            [-0.1, 0.9, 0], [-1.2, 0.5, 0], [-1.6, 0.7, 0], [-1.4, 1.9, 0], 
            [-2.6, 2.6, 0], [-4.4, 1.2, 0], [-4.9, -0.8, 0], [-3.8, -2.4, 0] 
            
        ]
        
        ring2 = [ 
            [0.2, -1.2, 0], [0.9, -1.2, 0], [1.4, -2.0, 0], [2.1, -1.6, 0], 
            [2.2, -0.5, 0], [1.4, 0.0, 0], [0.4, -0.2, 0], [0.2, -1.2, 0] 
        ] 
        
        ring3 = [[-2.7, 1.4, 0], [-2.3, 1.7, 0], [-2.8, 1.9, 0], [-2.7, 1.4, 0]]

       #create Polygons (for reference)
        p1 = Polygon(*ring1, fill_opacity=0.75) 
        p2 = Polygon(*ring2, fill_color=BLACK, fill_opacity=1) 
        p3 = Polygon(*ring3, fill_color=BLACK, fill_opacity=1)

        #create Labeled Polygram
        polygram = LabeledPolygram( 
            *[ring1, ring2, ring3], 
            label=Text('Pole', font='sans-serif'), 
            precision=0.01, 
        )

        #display Circle (for reference)
        circle = Circle(radius=polygram.radius, color=WHITE).move_to(polygram.pole)

        self.add(p1, p2, p3) 
        self.add(polygram) 
        self.add(circle)





    #d. LINE - Mobjects that are lines or variations of them

#a. Angle - A circular arc or elbow type mobject representing an angle of two lines

#RightArcAngleExample

class RightArcAngleExample(Scene): 
    def construct(self): 
        line1 = Line( LEFT, RIGHT ) 
        line2 = Line( DOWN, UP ) 
        rightarcangles = [ 
            Angle(line1, line2, dot=True), 
            Angle(line1, line2, radius=0.4, quadrant=(1,-1), dot=True, other_angle=True), 
            Angle(line1, line2, radius=0.5, quadrant=(-1,1), stroke_width=8, dot=True, dot_color=YELLOW, dot_radius=0.04, other_angle=True), 
            Angle(line1, line2, radius=0.7, quadrant=(-1,-1), color=RED, dot=True, dot_color=GREEN, dot_radius=0.08), 
        ] 
        plots = VGroup() 
        for angle in rightarcangles: 
            plot=VGroup(line1.copy(),line2.copy(), angle) 
            plots.add(plot) 
        plots.arrange(buff=1.5) 
        self.add(plots)

      #AngleExample 2

class AngleExample(Scene): 
    def construct(self): 
        line1 = Line( LEFT + (1/3) * UP, RIGHT + (1/3) * DOWN ) 
        line2 = Line( DOWN + (1/3) * RIGHT, UP + (1/3) * LEFT ) 
        angles = [ 
            Angle(line1, line2), 
            Angle(line1, line2, radius=0.4, quadrant=(1,-1), other_angle=True), 
            Angle(line1, line2, radius=0.5, quadrant=(-1,1), stroke_width=8, other_angle=True), 
            Angle(line1, line2, radius=0.7, quadrant=(-1,-1), color=RED), 
            Angle(line1, line2, other_angle=True), 
            Angle(line1, line2, radius=0.4, quadrant=(1,-1)), 
            Angle(line1, line2, radius=0.5, quadrant=(-1,1), stroke_width=8), 
            Angle(line1, line2, radius=0.7, quadrant=(-1,-1), color=RED, other_angle=True), 
        ] 
        plots = VGroup() 
        for angle in angles: 
            plot=VGroup(line1.copy(),line2.copy(), angle) 
            plots.add(VGroup(plot,SurroundingRectangle(plot, buff=0.3))) 
        plots.arrange_in_grid(rows=2,buff=1) 
        self.add(plots)


    #FilledAngle 3

class FilledAngle(Scene): 
    def construct(self): 
        l1 = Line(ORIGIN, 2 * UP + RIGHT).set_color(GREEN) 
        l2 = ( 
            Line(ORIGIN, 2 * UP + RIGHT) 
            .set_color(GREEN) 
            .rotate(-20 * DEGREES, about_point=ORIGIN) 
        ) 
        norm = l1.get_length() 
        a1 = Angle(l1, l2, other_angle=True, radius=norm - 0.5).set_color(GREEN) 
        a2 = Angle(l1, l2, other_angle=True, radius=norm).set_color(GREEN) 
        q1 = a1.points # save all coordinates of points of angle a1 
        q2 = a2.reverse_direction().points # save all coordinates of points of angle a1 (in reversed direction) 
        pnts = np.concatenate([q1, q2, q1[0].reshape(1, 3)]) # adds points and ensures that path starts and ends at same point 
        mfill = VMobject().set_color(ORANGE) 
        mfill.set_points_as_corners(pnts).set_fill(GREEN, opacity=1) 
        self.add(l1, l2) 
        self.add(mfill)

        #(methods)

        #1 from_three_points - The angle b2n the lines AB and BC

class AngleFrm3PointsEx(Scene):
    def construct(self):

        sample_angle = Angle.from_three_points(UP, ORIGIN, LEFT)
        red_angle = Angle.from_three_points(LEFT +UP, ORIGIN, RIGHT, radius=0.8, quadrant = (-1, 1), color= RED, stroke_width = 8, other_angle= True)
        self.add(red_angle, sample_angle)
    

        #2. get_lines - Get the lines forming an angle of the Angle class

line1, line2  = Line(ORIGIN, RIGHT), Line(ORIGIN, UR)
angle = Angle(line1, line2)
angle.get_lines()
VGroup(Line, Line)

        #3. get_value - get the value of an angleof the Angle class

  #GetValueExample

class GetValueExample(Scene): 
    def construct(self): 
        line1 = Line(LEFT+(1/3)*UP, RIGHT+(1/3)*DOWN) 
        line2 = Line(DOWN+(1/3)*RIGHT, UP+(1/3)*LEFT)

        angle = Angle(line1, line2, radius=0.4)

        value = DecimalNumber(angle.get_value(degrees=True), unit=r"^{\circ}") 
        value.next_to(angle, UR)

        self.add(line1, line2, angle, value)

#b. Arrow - an arrow
         #arrowExample

class ArrowExample(Scene): 
    def construct(self): 
        arrow_1 = Arrow(start=RIGHT, end=LEFT, color=GOLD) 
        arrow_2 = Arrow(start=RIGHT, end=LEFT, color=GOLD, tip_shape=ArrowSquareTip).shift(DOWN) 
        g1 = Group(arrow_1, arrow_2)

            #the effect of buff
        square = Square(color=MAROON_A) 
        arrow_3 = Arrow(start=LEFT, end=RIGHT) 
        arrow_4 = Arrow(start=LEFT, end=RIGHT, buff=0).next_to(arrow_1, UP) 
        g2 = Group(arrow_3, arrow_4, square)

        #a shorter arrow has a shorter tip and smaller stroke width
        arrow_5 = Arrow(start=ORIGIN, end=config.top).shift(LEFT * 4) 
        arrow_6 = Arrow(start=config.top + DOWN, end=config.top).shift(LEFT * 3) 
        g3 = Group(arrow_5, arrow_6)

        self.add(Group(g1, g2, g3).arrange(buff=2))


      #ArrowExample 2

class ArrowExample(Scene): 
    def construct(self): 
        left_group = VGroup()

            #As buff increases, the size of the arrow decreases.
        for buff in np.arange(0, 2.2, 0.45): 
            left_group += Arrow(buff=buff, start=2 * LEFT, end=2 * RIGHT)

            #Required to arrange arrows.
        left_group.arrange(DOWN) 
        left_group.move_to(4 * LEFT)

        middle_group = VGroup()

        #As max_stroke_width_to_length_ratio gets bigger, the width of stroke increases.
        for i in np.arange(0, 5, 0.5): 
            middle_group += Arrow(max_stroke_width_to_length_ratio=i) 
        middle_group.arrange(DOWN)

        UR_group = VGroup()

        #As max_tip_length_to_length_ratio increases, the length of the tip increases.
        for i in np.arange(0, 0.3, 0.1): 
            UR_group += Arrow(max_tip_length_to_length_ratio=i) 
        UR_group.arrange(DOWN) 
        UR_group.move_to(4 * RIGHT + 2 * UP)

        DR_group = VGroup() 
        DR_group += Arrow(start=LEFT, end=RIGHT, color=BLUE, tip_shape=ArrowSquareTip) 
        DR_group += Arrow(start=LEFT, end=RIGHT, color=BLUE, tip_shape=ArrowSquareFilledTip) 
        DR_group += Arrow(start=LEFT, end=RIGHT, color=YELLOW, tip_shape=ArrowCircleTip) 
        DR_group += Arrow(start=LEFT, end=RIGHT, color=YELLOW, tip_shape=ArrowCircleFilledTip) 
        DR_group.arrange(DOWN) 
        DR_group.move_to(4 * RIGHT + 2 * DOWN)

        self.add(left_group, middle_group, UR_group, DR_group)


#c. DashedLine - A dashed line

class DashedLineExample(Scene): 
    def construct(self):

        #dash_length increased
        dashed_1 = DashedLine(config.left_side, config.right_side, dash_length=2.0).shift(UP*2)

        #normal
        dashed_2 = DashedLine(config.left_side, config.right_side)

        #dashed_ratio decreased
        dashed_3 = DashedLine(config.left_side, config.right_side, dashed_ratio=0.1).shift(DOWN*2) 
        self.add(dashed_1, dashed_2, dashed_3)


#d. DoubleArrow - An arrow with tips on both ends

          #doubleArrowExample

 
class DoubleArrowExample(Scene): 
    def construct(self): 
        circle = Circle(radius=2.0) 
        d_arrow = DoubleArrow(start=circle.get_left(), end=circle.get_right()) 
        d_arrow_2 = DoubleArrow(tip_shape_end=ArrowCircleFilledTip, tip_shape_start=ArrowCircleFilledTip) 
        group = Group(Group(circle, d_arrow), d_arrow_2).arrange(UP, buff=1) 
        self.add(group)

   #doubleArrowExample2 

class DoubleArrowExample2(Scene): 
    def construct(self): 
        box = Square() 
        p1 = box.get_left() 
        p2 = box.get_right() 
        d1 = DoubleArrow(p1, p2, buff=0) 
        d2 = DoubleArrow(p1, p2, buff=0, tip_length=0.2, color=YELLOW) 
        d3 = DoubleArrow(p1, p2, buff=0, tip_length=0.4, color=BLUE) 
        Group(d1, d2, d3).arrange(DOWN) 
        self.add(box, d1, d2, d3)


#e. Elbow - two lines that create a right angle about each other: L-shape

class ElbowExample(Scene): 
    def construct(self): 
        elbow_1 = Elbow() 
        elbow_2 = Elbow(width=2.0) 
        elbow_3 = Elbow(width=2.0, angle=5*PI/4)

        elbow_group = Group(elbow_1, elbow_2, elbow_3).arrange(buff=1) 
        self.add(elbow_group)


    
#f. Line - A straight or curved line segment b2n two points or mobjects

class LineExample(Scene): 
    def construct(self): 
        line1 = Line(LEFT*2, RIGHT*2) 
        line2 = Line(LEFT*2, RIGHT*2, buff=0.5) 
        line3 = Line(LEFT*2, RIGHT*2, path_arc=PI/2) 
        grp = VGroup(line1,line2,line3).arrange(DOWN, buff=2) 
        self.add(grp)

#set start and end coordinate of a line

class LineEx(Scene):
    def construct(self):
        d = VGroup()
        for i in range(0, 10):
            d.add(Dot())
        d.arrange_in_grid(buff=1)
        self.add(d)
        l = Line(d[0], d[1])
        self.add(l)
        self.wait()
        l.put_start_and_end_on(d[1].get_center(), d[2].get_center())
        self.wait()
        l.put_start_and_end_on(d[4].get_center(), d[7].get_center())
        self.wait()


#g. RightAngle - An elbow-type mobject representing a right angle b2n 2 lines

class RightAngleExample(Scene): 
    def construct(self): 
        line1 = Line( LEFT, RIGHT ) 
        line2 = Line( DOWN, UP ) 
        rightangles = [ 
            RightAngle(line1, line2), 
            RightAngle(line1, line2, length=0.4, quadrant=(1,-1)), 
            RightAngle(line1, line2, length=0.5, quadrant=(-1,1), stroke_width=8), 
            RightAngle(line1, line2, length=0.7, quadrant=(-1,-1), color=RED), 
        ]   
        plots = VGroup() 
        for rightangle in rightangles: 
            plot=VGroup(line1.copy(),line2.copy(), rightangle) 
            plots.add(plot) 
        plots.arrange(buff=1.5) 
        self.add(plots)


#h. TangentLine - Constructs a line tangent to a VmMobject at a specific point

class TangentLineExample(Scene): 
    def construct(self): 
        circle = Circle(radius=2) 
        line_1 = TangentLine(circle, alpha=0.0, length=4, color=BLUE_D) # right 
        line_2 = TangentLine(circle, alpha=0.4, length=4, color=GREEN) # top left 
        self.add(circle, line_1, line_2)


#i. Vector - A vector specialized for use in graphs

class VectorExample(Scene): 
    def construct(self): 
        plane = NumberPlane() 
        vector_1 = Vector([1,2]) 
        vector_2 = Vector([-5,-2])
        self.add(plane, vector_1, vector_2)

#Vector coordinateLabel Example

class VectorCoordinateLabel(Scene): 
    def construct(self): 
        plane = NumberPlane()

        vec_1 = Vector([1, 2]) 
        vec_2 = Vector([-3, -2]) 
        label_1 = vec_1.coordinate_label() 
        label_2 = vec_2.coordinate_label(color=YELLOW)

        self.add(plane, vec_1, vec_2, label_1, label_2)

    #e. POLYGRAM - mobjects that are simple geometric shapes

#i. Convexhull - Constructs a convex hull for a set of points in no particular order

class ConvexHullExample(Scene): 
    def construct(self): 
        points = [ 
            [-2.35, -2.25, 0], 
            [1.65, -2.25, 0], 
            [2.65, -0.25, 0], 
            [1.65, 1.75, 0], 
            [-0.35, 2.75, 0], 
            [-2.35, 0.75, 0], 
            [-0.35, -1.25, 0], 
            [0.65, -0.25, 0], 
            [-1.35, 0.25, 0], 
            [0.15, 0.75, 0] 
        ] 
        hull = ConvexHull(points, color=BLUE) 
        dots = VGroup([Dot(point) for point in points]) 
        self.add(hull) 
        self.add(dots)


#ii. Cutout - A shape with smaller cutouts

class CutoutExample(Scene): 
    def construct(self): 
        s1 = Square().scale(2.5) 
        s2 = Triangle().shift(DOWN + RIGHT).scale(0.5) 
        s3 = Square().shift(UP + RIGHT).scale(0.5) 
        s4 = RegularPolygon(5).shift(DOWN + LEFT).scale(0.5) 
        s5 = RegularPolygon(6).shift(UP + LEFT).scale(0.5) 
        c = Cutout(s1, s2, s3, s4, s5, fill_opacity=1, color=BLUE, stroke_color=RED) 
        self.play(Write(c), run_time=4) 
        self.wait()


#iii. Polygon - A shape consisting of one closed loop of vertices

class PolygonExample(Scene): 
    def construct(self): 
        isosceles = Polygon([-5, 1.5, 0], [-2, 1.5, 0], [-3.5, -2, 0]) 
        position_list = [ 
            [4, 1, 0], # middle right 
            [4, -2.5, 0], # bottom right 
            [0, -2.5, 0], # bottom left
            [0, 3, 0], # top left
            [2, 1, 0], # middle 
            [4, 3, 0], # top right 
        ] 
        square_and_triangles = Polygon(*position_list, color=PURPLE_B) 
        self.add(isosceles, square_and_triangles)

#iv. Polygram - a generalized polygon, allowing for disconnected sets of edges

class PolygramExample(Scene): 
    def construct(self): 
        hexagram = Polygram( 
            [[0, 2, 0], [-np.sqrt(3), -1, 0], [np.sqrt(3), -1, 0]], 
            [[-np.sqrt(3), 1, 0], [0, -2, 0], [np.sqrt(3), 1, 0]], 
        ) 
        self.add(hexagram)

        dot = Dot()
        self.play(MoveAlongPath(dot, hexagram), run_time=5, rate_func=linear) 
        self.remove(dot) 
        self.wait()

    #PolygramRoundCornersEx 

class PolygramRoundCorners(Scene): 
    def construct(self): 
        star = Star(outer_radius=2)

        shapes = VGroup(star) 
        shapes.add(star.copy().round_corners(radius=0.1)) 
        shapes.add(star.copy().round_corners(radius=0.25))

        shapes.arrange(RIGHT) 
        self.add(shapes)

        
#v. Rectangle - a quadrilateral with 2 sets of parallel sides

class RectangleExample(Scene): 
    def construct(self): 
        rect1 = Rectangle(width=4.0, height=2.0, grid_xstep=1.0, grid_ystep=0.5) 
        rect2 = Rectangle(width=1.0, height=4.0) 
        rect3 = Rectangle(width=2.0, height=2.0, grid_xstep=1.0, grid_ystep=1.0) 
        rect3.grid_lines.set_stroke(width=1)

        rects = Group(rect1, rect2, rect3).arrange(buff=1) 
        self.add(rects)


#vi. RegularPolygon - an n-sided regular polygon

class RegularPolygonExample(Scene): 
    def construct(self): 
        poly_1 = RegularPolygon(n=6) 
        poly_2 = RegularPolygon(n=6, start_angle=30*DEGREES, color=GREEN) 
        poly_3 = RegularPolygon(n=10, color=RED)

        poly_group = Group(poly_1, poly_2, poly_3).scale(1.5).arrange(buff=1) 
        self.add(poly_group)


#vii. RegularPolygram   a polygram with regularly spaced vertices

class RegularPolygramExample(Scene): 
    def construct(self): 
        pentagram = RegularPolygram(5, radius=2) 
        self.add(pentagram)

#viii. RoundedRectangle

class RoundedRectangleExample(Scene): 
    def construct(self): 
        rect_1 = RoundedRectangle(corner_radius=0.5) 
        rect_2 = RoundedRectangle(corner_radius=1.5, height=4.0, width=4.0)

        rect_group = Group(rect_1, rect_2).arrange(buff=1) 
        self.add(rect_group)


#ix. Square

class SquareExample(Scene): 
    def construct(self): 
        square_1 = Square(side_length=2.0).shift(DOWN) 
        square_2 = Square(side_length=1.0).next_to(square_1, direction=UP) 
        square_3 = Square(side_length=0.5).next_to(square_2, direction=UP) 
        self.add(square_1, square_2, square_3)


#x. Star

#StarExample1

class StarExample(Scene): 
    def construct(self): 
        pentagram = RegularPolygram(5, radius=2) 
        star = Star(outer_radius=2, color=RED)

        self.add(pentagram) 
        self.play(Create(star), run_time=3) 
        self.play(FadeOut(star), run_time=2)

 #DifferentDensitiesExample2

class DifferentDensitiesExample(Scene): 
    def construct(self): 
        density_2 = Star(7, outer_radius=2, density=2, color=RED) 
        density_3 = Star(7, outer_radius=2, density=3, color=PURPLE)

        self.add(VGroup(density_2, density_3).arrange(RIGHT))


#xi. Triangle - An equilateral triangle

class TriangleExample(Scene): 
    def construct(self): 
        triangle_1 = Triangle() 
        triangle_2 = Triangle().scale(2).rotate(60*DEGREES) 
        tri_group = Group(triangle_1, triangle_2).arrange(buff=1) 
        self.add(tri_group)

    #f. shape_matchers - Mobjects used to mark and annotate other mobbjects

#i. BackgroundRectangle - A background rectangle

class ExampleBackgroundRectangle(Scene): 
    def construct(self): 
        circle = Circle().shift(LEFT) 
        circle.set_stroke(color=GREEN, width=20) 
        triangle = Triangle().shift(2 * RIGHT) 
        triangle.set_fill(PINK, opacity=0.5) 
        backgroundRectangle1 = BackgroundRectangle(circle, color=WHITE, fill_opacity=0.15) 
        backgroundRectangle2 = BackgroundRectangle(triangle, color=WHITE, fill_opacity=0.15) 
        self.add(backgroundRectangle1) 
        self.add(backgroundRectangle2) 
        self.add(circle) 
        self.add(triangle) 
        self.play(Rotate(backgroundRectangle1, PI / 4)) 
        self.play(Rotate(backgroundRectangle2, PI / 2))


#ii. Cross - Creates a cross

class ExampleCross(Scene): 
    def construct(self): 
        cross = Cross() 
        self.add(cross)

#iii. SurroundingRectangle - A rect surrounding a Mobject

class SurroundingRectExample(Scene): 
    def construct(self): 
        title = Title("A Quote from Newton") 
        quote = Text( 
            "If I have seen further than others, \n" 
            "it is by standing upon the shoulders of giants.", 
            color=BLUE, 
        ).scale(0.75) 
        box = SurroundingRectangle(quote, color=YELLOW, buff=MED_LARGE_BUFF)

        t2 = Tex(r"Hello World").scale(1.5) 
        box2 = SurroundingRectangle(t2, corner_radius=0.2) 
        mobjects = VGroup(VGroup(box, quote), VGroup(t2, box2)).arrange(DOWN) 
        self.add(title, mobjects)

#iv. Underline - creates and underline

class UnderLine(Scene): 
    def construct(self): 
        man = Tex("Manim") # Full Word 
        ul = Underline(man) # Underlining the word 
        self.add(man, ul)

    #g. tips - A collection of tip mobjects for use with TipableVMobject

#i. ArrowCircleFilledTip - Circular arrow tip with filled tip

#ii. ArrowCircleTip - Circular arrow tip
#iii. ArrowSquareFilledTip - Square arrow tip with filled tip
#iv. ArrowSquareTip - Aquare arrow tip
#v. ArrowTip - Base class for arrow tips

        #CustomTipExample

from manim import RegularPolygon, Arrow 

class MyCustomArrowTip(ArrowTip, RegularPolygon):
    def __init__(self, length=0.35, **kwargs): 
        RegularPolygon.__init__(self, n=5, **kwargs) 
        self.width = length 
        self.stretch_to_fit_height(length)

arr = Arrow( np.array([-2, -2, 0]), np.array([2, 2, 0]), tip_shape=MyCustomArrowTip 
                    )

isinstance(arr.tip, RegularPolygon) 
True

from manim import Scene, Create 
class CustomTipExample(Scene):  
    def construct(self):  
        self.play(Create(arr))


       #ArrowTipsShowcase

class ArrowTipsShowcase(Scene): 
    def construct(self): 
        tip_names = [ 
            'Default (YELLOW)', 'ArrowTriangleTip', 'Default', 'ArrowSquareTip', 
            'ArrowSquareFilledTip', 'ArrowCircleTip', 'ArrowCircleFilledTip', 'StealthTip' 
        ]

        big_arrows = [ 
            Arrow(start=[-4, 3.5, 0], end=[2, 3.5, 0], color=YELLOW), 
            Arrow(start=[-4, 2.5, 0], end=[2, 2.5, 0], tip_shape=ArrowTriangleTip), 
            Arrow(start=[-4, 1.5, 0], end=[2, 1.5, 0]), 
            Arrow(start=[-4, 0.5, 0], end=[2, 0.5, 0], tip_shape=ArrowSquareTip),

            Arrow([-4, -0.5, 0], [2, -0.5, 0], tip_shape=ArrowSquareFilledTip), 
            Arrow([-4, -1.5, 0], [2, -1.5, 0], tip_shape=ArrowCircleTip), 
            Arrow([-4, -2.5, 0], [2, -2.5, 0], tip_shape=ArrowCircleFilledTip), 
            Arrow([-4, -3.5, 0], [2, -3.5, 0], tip_shape=StealthTip) 
        ]

        small_arrows = ( 
            arrow.copy().scale(0.5, scale_tips=True).next_to(arrow, RIGHT) for arrow in big_arrows 
        )

        labels = ( 
            Text(tip_names[i], font='monospace', font_size=20, color=BLUE).next_to(big_arrows[i], LEFT) for i in range(len(big_arrows)) 
        )

        self.add(*big_arrows, *small_arrows, *labels)

#vi. ArrowTriangleFilledTip - Triangular arrow tip
#vii. StealthTip - 'Stealth' fighter/ kite arrow shape


   
    #3. graph - Mobjects used to represent mathematical graphs(think graph theory, not plotting)

#i. DiGraph - A direct graph

           #MovingDiGraph Ex1

class MovingDiGraph(Scene): 
    def construct(self): 
        vertices = [1, 2, 3, 4] 
        edges = [(1, 2), (2, 3), (3, 4), (1, 3), (1, 4)]

        g = DiGraph(vertices, edges)

        self.add(g) 
        self.play( g[1].animate.move_to([1, 1, 1]), g[2].animate.move_to([-1, 1, 2]), g[3].animate.move_to([1, -1, -1]), g[4].animate.move_to([-1, -1, 0]), ) 
        self.wait()

#You can customize the edges and arrow tips globally or locally.


          #CustomDiGraph Ex2

class CustomDiGraph(Scene): 
    def construct(self): 
        vertices = [i for i in range(5)] 
        edges = [ 
            (0, 1), 
            (1, 2), 
            (3, 2), 
            (3, 4), 
        ]

        edge_config = { 
            "stroke_width": 2, 
            "tip_config": { 
                "tip_shape": ArrowSquareTip, 
                "tip_length": 0.15, 
            }, 
            (3, 4): { 
                "color": RED, 
                "tip_config": {"tip_length": 0.25, "tip_width": 0.25} 
            },
        }

        g = DiGraph( 
            vertices, 
            edges, 
            labels=True, 
            layout="circular", 
            edge_config=edge_config, 
        ).scale(1.4)

        self.play(Create(g)) 
        self.wait()

#Since this implementation respects the labels boundary you can also use it for an undirected moving graph with labels

      #UndirectedMovingDiGraph

class UndirectedMovingDiGraph(Scene): 
    def construct(self): 
        vertices = [i for i in range(5)] 
        edges = [ 
            (0, 1), 
            (1, 2), 
            (3, 2), 
            (3, 4), 
        ]

        edge_config = { 
            "stroke_width": 2, 
            "tip_config": {"tip_length": 0, "tip_width": 0}, 
            (3, 4): {"color": RED}, 
        }

        g = DiGraph( 
            vertices, 
            edges, 
            labels=True, 
            layout="circular", 
            edge_config=edge_config, 
        ).scale(1.4)

        self.play(Create(g)) 
        self.wait()

        self.play( 
            g[1].animate.move_to([1, 1, 1]), 
            g[2].animate.move_to([-1, 1, 2]), 
            g[3].animate.move_to([-1.5, -1.5, -1]), 
            g[4].animate.move_to([1, -2, -1]), 
        ) 
        self.wait()


#ii. GenericGraph - Abstract base class(that is, a collection of vertices connected with edges)

class ChangeGraphLAyout(Scene):
    def construct(self):
        G = Graph([1, 2, 3, 4, 5], [(1, 2), (2, 3), (3, 4), (4, 5)],
                  layout={1: [-2, 0, 0], 2: [-1, 0, 0], 3: [0, 0, 0],
                          4: [1, 0, 0], 5: [2, 0, 0]}
                    )
        self.play(Create(G))
        self.play(G.animate.change_layout("circular"))
        self.wait()


from manim import *

import networkx as nx

nxgraph = nx.erdos_renyi_graph(14, 0.5)

class ImportNetworkxGraph(Scene):
    def construct(self):
        G = Graph.from_networkx(nxgraph, layout = "spring", layout_scale = 3.5)
        self.play(Create(G))
        self.play(*[G[v].animate.move_to(5*RIGHT*np.cos(ind/7 *PI) + 
                                         3*UP*np.sin(ind/7 *PI))
                    for ind, v in enumerate(G.vertices)])
        self.play(Uncreate(G))


#iii. Graph - An undirected graph (vertices connected with edges)

   #Ex1. Moving Vertices

class MovingVertices(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (2, 3), (3, 4), (1, 3), (1, 4)]
        g = Graph(vertices, edges)
        self.play(Create(g))
        self.wait()
        self.play(g[1].animate.move_to([1, 1, 0]),
                  g[2].animate.move_to([-1, 1, 0]),
                  g[3].animate.move_to([1, -1, 0]),
                  g[4].animate.move_to([-1, -1, 0]))
        self.wait()


#there are several automatic positioning algorithms to choose from :

#Ex2 Graph auto position
class GraphAutoPosition(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4, 5, 6, 7, 8]
        edges = [(1, 7), (1, 8), (2, 3), (2, 4), (2, 5),
                 (2, 8), (3, 4), (6, 1), (6, 2),
                 (6, 3), (7, 2), (7, 4)]
        autolayouts = ["spring", "circular", "kamada_kawai", 
                       "planar", "random", "shell", 
                       "spectral", "spiral"]
        graphs= [Graph(vertices, edges, layout=lt).scale(0.5)
                 for lt in autolayouts]
        r1 = VGroup(*graphs[:3]).arrange()
        r2 = VGroup(*graphs[3:6]).arrange()
        r3 = VGroup(*graphs[6:]).arrange()
        self.add(VGroup(r1, r2, r3).arrange(direction=DOWN))


#Ex3. Vertices can also be positioned manually


class GraphManualPosition(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
        lt = {1: [0, 0, 0], 2:[1, 1, 0], 3:[1, -1, 0], 4: [-1, 0, 0]}
        G= Graph(vertices, edges, layout=lt)
        self.add(G)

   #Ex4. the vertices in graphs can be labelled, and configurations for vertices can be modified both by default and for specificvertices and edges

class LabeledModifiedGraph(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4, 5, 6, 7, 8]
        edges = [(1, 7), (1, 8), (2, 3), (2, 4), (2, 5),
                 (2, 8), (3, 4), (6, 1), (6, 2),
                 (6, 3), (7, 2), (7, 4)]
        g = Graph(vertices, edges, layout="circular", layout_scale= 3,
                  labels = True, vertex_config={7: {"fill_color":RED}},
                  edge_config={(1, 7): {"stroke_color": RED},
                               (2, 7): {"stroke_color": RED},
                               (4, 7): {"stroke_color": RED}})
        self.add(g)

  #Ex5. You can also layout a partite graph on columns by specifying a list of the vertices on each side and choosong the partite layout
import networkx as nx

class Partitegraph(Scene):
    def construct(self):
        G = nx.Graph()
        G.add_nodes_from([0, 1, 2, 3])
        G.add_edges_from([(0, 2), (0, 3), (1, 2)])
        graph= Graph(list(G.nodes), list(G.edges), layout="partite", partitions=[[0, 1]])
        self.play(Create(graph))

    #Ex6. The representation of a linear artificial neuro network is facilitated by the use of the partite layout and defining partitions for each layer

class LinearNN(Scene):
    def construct(self):
        edges = []
        partitions = []
        c = 0
        layers = [2, 3, 3, 2]  #the number of neurons in each layer

        for i in layers:
            partitions.append(list(range(c + 1, c + i + 1 )))
            c += i 
        for i, v in enumerate(layers[1:]):
            last = sum(layers[:i+1])
            for j in range(v):
                for k in range(last - layers[i], last):
                    edges.append((k + 1, j + last + 1))

        vertices = np.arange(1, sum(layers) + 1)

        graph = Graph(
            vertices,
            edges,
            layout='partite',
            partitions=partitions,
            layout_scale=3,
            vertex_config={'radius': 0.20},
        )
        self.add(graph)

#Ex7. The csutom tree layout can be used to show the graph by distance from the root vertex. You must pass the root vertex of the tree

import networkx as nx 

class Tree(Scene):
    def construct(self):
        G = nx.Graph()

        G.add_node("ROOT")

        for i in range(5):
            G.add_node("Child_%i" % i)
            G.add_node("Grandchild_%i" % i)
            G.add_node("Greatgrandchild_%i" % i)

            G.add_edge("ROOT", "Child_%i" % i)
            G.add_edge("Child_%i" % i, "Grandchild_%i" % i)
            G.add_edge("Grandchild_%i" % i, "Greatgrandchild_%i" % i)

        self.play(Create(
            Graph(list(G.nodes), list(G.edges), layout= "tree", root_vertex = "ROOT"))
        )

#Ex8. LargeTreeGeneration

class LargeTreeGeneration(MovingCameraScene):
    DEPTH = 4
    CHILDREN_PER_VERTEX = 3
    LAYOUT_CONFIG = {"vertex_spacing": (0.5, 1)}
    VERTEX_CONFIG = {"radius": 0.25, "color": BLUE_B, "fill_opacity": 1}

    def expand_vertex(self, g, vertex_id: str, depth: int):
        new_vertices = [
            f"{vertex_id}/{i}" for i in range(self.CHILDREN_PER_VERTEX)
        ]
        new_edges = [(vertex_id, child_id) for child_id in new_vertices]
        g.add_edges(
            *new_edges,
            vertex_config=self.VERTEX_CONFIG,
            positions={
                k: g.vertices[vertex_id].get_center() + 0.1 * DOWN
                for k in new_vertices
            },
        )
        if depth < self.DEPTH:
            for child_id in new_vertices:
                self.expand_vertex(g, child_id, depth + 1)

            return g
        
    def construct(self):
        g = Graph(["ROOT"], [], vertex_config=self.VERTEX_CONFIG)
        g = self.expand_vertex(g, "ROOT", 1)
        self.add(g)

        self.play(
            g.animate.change_layout(
                "tree",
                root_vertex= "ROOT",
                layout_config= self.LAYOUT_CONFIG,
            )
        )
        self.play(self.camera.auto_zoom(g, margin = 1), run_time=0.5)



#iv. LayoutFunction - A protocol for automatic layout functions that compute a layout for a graph to be used in change_layout()

#here's an example that arranges nodes in an n x m grid in sorted order


class CustomLayoutExample(Scene):
    def construct(self):
        import numpy as np
        import networkx as nx

        #create custom layout
        def custom_layout(
            graph: nx.Graph,
            scale: float | tuple[float, float, float] = 2,
            n: int | None = None,
            *args: Any,
            **kwargs: Any,
        ):
            nodes = sorted(list(graph))
            height = len(nodes) // n
            return{
                node: (scale * np.array([
                    (i % n) -(n-1)/2,
                    -(i // n) + height/2,
                    0
                  ])) for i, node in enumerate(graph)
            }
        #draw graph
        n = 4
        graph = Graph(
            [i for i in range(4 * 2 - 1)],
            [(0, 1), (0, 4), (1, 2), (1, 5), (2, 3), (2,6), (4, 5), (5, 6)],
            labels = True,
            layout= custom_layout,
            layout_config={'n': n}
        )
        self.add(graph)

#Circular layout places the vertices on a circle

class CircularLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6,],
            [(1, 2), (2, 3), (3,4), (4,5), (5, 6), (6, 1), (5, 1), (1, 3), (3, 5)],
            layout = "circular",
            labels=True
        )
        self.add(graph)

#Kamada Kawai Layout: tries to place the vertices such that the given distance b2n them are respected

class KamadaKawaiLayout(Scene):
    def construct(self):
        from collections import defaultdict
        distances: dict[int, dict[int, float]] = defaultdict(dict)

        #set desired distances
        distances[1][2] = 1 # distances b2n vertices 1 and 2 = 1
        distances[2][3] = 1 # distance b2n vertices 2 and 3 = 1
        distances[3][4] = 2 #etc 
        distances[4][5] = 3 
        distances[5][6] = 5 
        distances[6][1] = 8 

        graph = Graph(
            [1, 2, 3, 4, 5, 6],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)],
            layout="kamada_kawai",
            layout_config={"dist": distances},
            layout_scale=4,
            labels=True
        )
        self.add(graph)

#partite Layout - places vertices into distinct partitions

class PartiteLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (5, 1), (1, 3), (3, 5)],
            layout="partite",
            layout_config={"partitions": [[1,2], [3,4], [5,6]]},
            labels=True
        )
        self.add(graph)

#Planar Layout - Places vertices such that the edges do not cross

class PlanarLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (5, 1), (1, 3), (3, 5)],
            layout="planar", 
            layout_config=4,
            labels=True
        )
        self.add(graph)

#Random Layout: layout randomly places vertices

class RandomLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (5, 1), (1, 3), (3, 5)],
            layout="random",
            labels=True
        )
        self.add(graph)

#Shell Layout: places vertices in concentric circles

class ShellLayout(Scene):
    def construct(self):
        nlist = [[1, 2, 3], [4, 5, 6, 7, 8, 9]]
        graph = Graph(
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [(1, 2), (2, 3), (3, 1), (4, 1), (4, 2), (5, 2), (6, 2), (6, 3), (7, 3), (8, 3), (8, 1), (9, 1)],
            layout="shell",
            layout_config={"nlist": nlist},
            labels= True
        )
        self.add(graph)

#Spectral Layout - Places the vertices using the eigenvectors of the graph Laplacian (clusters nodes which are an approximation of the ratio cut)

class SpectralLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (5, 1), (1, 3), (3, 5)],
            layout="spectral",
            labels=True
         )
        self.add(graph)

#Spiral Layout - places vertices in a spiralling pattern

class SpiralLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (5, 1), (1, 3), (3, 5)],
            layout="spiral",
            labels=True
        )
        self.add(graph)

#Spring LAyout - places nodes according to the Fruchteman-Reingold force-directed algorithm(attempts to minimize edge-length while maximizing node separation)

class SpringLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (5, 1), (1, 3), (3, 5)],
            layout="spring",
            labels=True
        )
        self.add(graph)

#TRee Layout - places vertices into a tree with a root node and branches (can only be used with legal trees)

class TreeLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6, 7],
            [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
            layout="tree",
            layout_config={"root_vertex": 1},
            labels= True
        )
        self.add(graph)



    #4. graphing - Coordinate systems and function graphing related mobjects
#a. COordinate_systems - mobjects that represent coordinate systems

#i. Axes - Creates a set of axes

#Ex1   LogScalingEx

class LogScalingEx(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 6, 1],
            tips=False,
            axis_config={"include_numbers": True},
            y_axis_config={"scaling": LogBase(custom_labels=True)},
        )

        #x must be > 0 bcs log is undefined at 0
        graph = ax.plot(lambda x: x ** 2, x_range=[0.001, 10], use_smoothing= False)
        self.add(ax, graph)

#Ex2. Axes with different tips
class AxesWithDiffTips(Scene):
    def construct(self):
        ax = Axes(axis_config={'tip_shape': StealthTip})
        self.add(ax)

#Ex3. Coordinates to points

class CoordsToPoints(Scene):
    def construct(self):
        ax = Axes().add_coordinates()

        #a dot with respect to the axes
        dot_axes = Dot(ax.coords_to_point(2, 2), color=GREEN)
        lines = ax.get_lines_to_point(ax.c2p(2, 2))

        #a dot with respect to the scene
        ## the default plane corresponds to the coordinates of the scene
        plane = NumberPlane()
        dot_scene = Dot((2, 2, 0), color= RED)

        self.add(plane, dot_scene, ax, dot_axes, lines)

 #Ex4. GetAxisLabels

class GetAxisLabels(Scene):
    def construct(self):
        ax = Axes()
        labels = ax.get_axis_labels(
            Tex("x-axis").scale(0.7), Text("y-axis").scale(0.45)
        )
        self.add(ax, labels)

#Ex5 Line Graph

class LIneGraph(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=(0, 7),
            y_range= (0, 5),
            x_length=7,
            axis_config={"include_numbers": True},
        )
        plane.center()
        line_graph = plane.plot_line_graph(
            x_values= [0, 1.5, 2, 2.8, 4, 6.25],
            y_values= [1, 3, 2.25, 4, 2.5, 1.75],
            line_color=GOLD_E,
            vertex_dot_style=dict(stroke_width=3, fill_color=PURPLE),
            stroke_width=4,
        )

        self.add(plane, line_graph)

#Ex6.  PointToCoords

class PointToCoords(Scene):
    def construct(self):
        ax = Axes(x_range=[0,10, 2]).add_coordinates()
        circ = Circle(radius=0.5).shift(UR * 2)

        #get the coordinates of the circle with respect to the axes
        coords = np.around(ax.point_to_coords(circ.get_right()), decimals=2)

        label = (
            Matrix([[coords[0]], [coords[1]]]).scale(0.75).next_to(circ, RIGHT)
        )
        self.ass(ax, circ, label, Dot(circ.get_right()))
        


#ii.ComplexPlane - A NumberPlane specialized for use with complex numbers

class ComplexPLane(Scene):
    def construct(self):
        plane = ComplexPLane().add_coordinates()
        self.add(plane)
        d1 = Dot(plane.n2p(2 + 1j), color=YELLOW)
        d2 = Dot(plane.n2p(-3 - 2j), color=YELLOW)
        label1 = MathTex("2+i").next_to(d1, UR, 0.1)
        label2 = MathTex("-3 - 2i").next_to(d2, UR, 0.1)
        self.add(
            d1,
            label1,
            d2,
            label2
        )


#iii. CoordinateSystem - Abstract base class for Axes and NumberPLane

#Ex1. 

class CoordSysEx(Scene):
    def construct(self):
        #the location of the ticks depends on the x_range and y_range
        grid = Axes(
            x_range=[0, 1, 0.05], #step size determines num_decimal_places
            y_range=[0, 1, 0.05],
            x_length=9,
            y_length=5.5,
            axis_config={
                "numbers_to_include": np.arange(0, 1 + 0.1, 0.1),
                "font_size": 24,
            },
            tips=False,
        )

        #labels for the x and y axes
        y_label = grid.get_y_axis_label("y", edge=LEFT, direction=LEFT, buff=0.4)
        x_label = grid.get_x_axis_label("x")
        grid_labels = VGroup(x_label, y_label)

        graphs = VGroup()
        for n in np.arange(1, 20 +0.5, 0.5):
            graphs += grid.plot(lambda x: x ** n, color= WHITE)
            graphs += grid.plot(
                lambda x: x ** (1 / n), color=WHITE, use_smoothing=False
            )

        #extra lines and labels for point (1, 1)
        graphs += grid.get_horizontal_line(grid @ (1, 1, 0), color = BLUE)
        graphs += grid.get_vertical_line(grid @ (1, 1, 0), color = BLUE)
        graphs += Dot(point= grid @ (1, 1, 0), color = YELLOW)
        graphs += Tex("1, 1").scale(0.75).next_to(grid @ (1, 1, 0))
        title = Title(
            #spaces b2n braces to prevent SyntaxError
            r"Graphs of $y=x^{ {1}\over{n} }$ and $y=x^n (n=1,2,3,...,20)$",
            include_underline=False,
            font_size = 40
        )
        self.add(title, graphs, grid, grid_labels)

    #EX2. TLabelExample

class TLabelEx(Scene):
    def construct(self):
        #defines the axes and linear function
        axes = Axes(x_range=[-1, 10], y_range=[-1, 10], x_length=9, y_length=6)
        funct = axes.plot(lambda x: x, color= BLUE)
        #creates the T_label
        t_label = axes.get_T_label(x_val=4, graph=funct, label=Tex("x-value"))
        self.add(axes, funct, t_label)

    #Ex3. Get Area Example

class GetAreaEx(Scene):
    def construct(self):
        ax = Axes().add_coordinates()
        curve = ax.plot(lambda x : 2 * np.sin(x), color=DARK_BLUE)
        area = ax.get_area(
            curve,
            x_range=(PI / 2, 3 * PI / 2),
            color= (GREEN_B, GREEN_D),
            opacity=1,
        )
        self.add(ax, curve, area)

 #Ex4. Get graph label Example

class GetGraphLabelEx(Scene):
    def construct(self):
       ax= Axes()
       sin = ax.plot(lambda x: np.sin(x), color=PURPLE_B)
       label = ax.get_graph_label(
           graph = sin,
           label= MathTex(r"\frac{\pi}{2}"),
           x_val=PI / 2,
           dot= True,
           direction=UR,
       )
       self.add(ax, sin, label)

#Ex5. Get horizontal Line

class GetHorizontalLine(Scene):
    def construct(self):
        ax = Axes().add_coordinates()
        point = ax @ (-4, 1.5)

        dot = Dot(point)
        line = ax.get_horizontal_line(point, line_func=Line)

        self.add(ax, line, dot)

  #Ex6. Get lines to point

class GetLinesToPointEx(Scene):
    def construct(self):
        ax = Axes()
        circ = Circle(radius=0.5).move_to([-4, -1.5, 0])

        lines_1 = ax.get_lines_to_point(circ.get_right(), color = GREEN_B)
        lines_2 = ax.get_lines_to_point(circ.get_corner(DL), color = BLUE_B)

        self.add(ax, lines_1, lines_2, circ)

  #x7. GetRiemannRectangles Ex

class GetRiemannRectanglesExample(Scene): 
    def construct(self): 
        ax = Axes(y_range=[-2, 10])
        quadratic = ax.plot(lambda x: 0.5 * x ** 2 - 0.5)

        #the rectangles are constructed from their top right corner.
        #passing an iterable to color produces a gradient
        rects_right = ax.get_riemann_rectangles( 
            quadratic, 
            x_range=[-4, -3], 
            dx=0.25, 
            color=(TEAL, BLUE_B, DARK_BLUE), 
            input_sample_type="right", 
        )

        #the colour of rectangles below the x-axis is inverted due to show_signed_area
        rects_left = ax.get_riemann_rectangles( 
            quadratic, 
            x_range=[-1.5, 1.5], 
            dx=0.15, 
            color=YELLOW 
        )

        bounding_line = ax.plot( 
            lambda x: 1.5 * x, color=BLUE_B, x_range=[3.3, 6] 
        ) 
        bounded_rects = ax.get_riemann_rectangles( 
            bounding_line, 
            bounded_graph=quadratic, 
            dx=0.15, x_range=[4, 5], 
            show_signed_area=False, 
            color=(MAROON_A, RED_B, PURPLE_D), 
        )

        self.add( 
            ax, bounding_line, quadratic, rects_right, rects_left, bounded_rects 
        )

    #Ex8. Get Secant Slope Group

class GetSecantSlopeGroupExample(Scene):
    def construct(self):
        ax = Axes(y_range=[-1, 7])
        graph = ax.plot(lambda x: 1 / 4 * x ** 2, color=BLUE)
        slopes = ax.get_secant_slope_group(
            x=2.0,
            graph=graph,
            dx=1.0,
            dx_label=Tex("dx = 1.0"),
            dy_label="dy",
            dx_line_color=GREEN_B,
            secant_line_length=4,
            secant_line_color=RED_D,
        )

        self.add(ax, graph, slopes)

 #Ex9. Get Vertical Line

class GetVerticalLineExample(Scene):
    def construct(self): 
        ax = Axes().add_coordinates()
        point = ax.coords_to_point(-3.5, 2)

        dot = Dot(point) 
        line = ax.get_vertical_line(point, line_config={"dashed_ratio": 0.85})

        self.add(ax, line, dot)

#Ex10. Get Vertical Lines to graph
class GetVerticalLinesToGraph(Scene): 
    def construct(self): 
        ax = Axes( 
            x_range=[0, 8.0, 1], 
            y_range=[-1, 1, 0.2], 
            axis_config={"font_size": 24}, 
        ).add_coordinates()

        curve = ax.plot(lambda x: np.sin(x) / np.e ** 2 * x)

        lines = ax.get_vertical_lines_to_graph( 
            curve, x_range=[0, 4], num_lines=30, color=BLUE 
        )

        self.add(ax, curve, lines)

    #Ex11. Get Axes Labels

class GetAxisLabelsExample(Scene): 
        def construct(self): 
            ax = Axes(x_range=(0, 8), y_range=(0, 5), x_length=8, y_length=5)
            # x axis label

            x_label = ax.get_x_axis_label( 
                Tex("x-axis").scale(0.7), edge=DOWN, direction=DOWN, buff=0.5
            ) 

            # y axis label

            y_label = ax.get_y_axis_label(
                Tex("y-axis").scale(0.65).rotate(90 * DEGREES),
                edge=LEFT,
                direction=LEFT,
                buff=0.3
            )
            self.add(ax, x_label, y_label)

    #Ex12. Input to Graph point

class InputToGraphPointExample(Scene): 
    def construct(self): 
        ax = Axes() 
        curve = ax.plot(lambda x : np.cos(x))

        #move a square to PI on the cosine curve.
        position = ax.input_to_graph_point(x=PI, graph=curve) 
        sq = Square(side_length=1, color=YELLOW).move_to(position)

        self.add(ax, curve, sq)

    #Ex13. PlotExample

class PlotExample(Scene): 
    def construct(self):

        #construct the axes
        ax_1 = Axes( 
            x_range=[0.001, 6], 
            y_range=[-8, 2], 
            x_length=5, 
            y_length=3, 
            tips=False, 
        )
        ax_2 = ax_1.copy() 
        ax_3 = ax_1.copy()

        #position the axes
        ax_1.to_corner(UL) 
        ax_2.to_corner(UR) 
        ax_3.to_edge(DOWN) 
        axes = VGroup(ax_1, ax_2, ax_3)

        #create the logarithmic curves
        def log_func(x): 
            return np.log(x)

        #a curve without adjustments; poor interpolation.
        curve_1 = ax_1.plot(log_func, color=PURE_RED)

        #disabling interpolation makes the graph look choppy as not enough inputs are available
        curve_2 = ax_2.plot(log_func, use_smoothing=False, color=ORANGE)

        #taking more inputs of the curve by specifying a step for the x_range yields expected results, but increases rendering time.
        curve_3 = ax_3.plot( 
            log_func, x_range=(0.001, 6, 0.001), color=PURE_GREEN 
        )

        curves = VGroup(curve_1, curve_2, curve_3)

        self.add(axes, curves)

    #Ex14. Antiderivative Ex

class AntiderivativeExample(Scene): 
    def construct(self): 
        ax = Axes() 
        graph1 = ax.plot( 
            lambda x: (x ** 2 - 2) / 3, 
            color=RED, 
        )
        graph2 = ax.plot_antiderivative_graph(graph1, color=BLUE) 
        self.add(ax, graph1, graph2)

    #Ex15. Derivative Graph Ex

class DerivativeGraphExample(Scene): 
    def construct(self):
        ax = NumberPlane(y_range=[-1, 7], background_line_style={"stroke_opacity": 0.4})

        curve_1 = ax.plot(lambda x: x ** 2, color=PURPLE_B) 
        curve_2 = ax.plot_derivative_graph(curve_1) 
        curves = VGroup(curve_1, curve_2)

        label_1 = ax.get_graph_label(curve_1, "x^2", x_val=-2, direction=DL) 
        label_2 = ax.get_graph_label(curve_2, "2x", x_val=3, direction=RIGHT) 
        labels = VGroup(label_1, label_2)

        self.add(ax, curves, labels)

    #EX16. Implicit Ex

class ImplicitExample(Scene): 
    def construct(self): 
        ax = Axes() 
        a = ax.plot_implicit_curve( 
            lambda x, y: y * (x - y) ** 2 - 4 * x - 8, color=BLUE 
        ) 
        self.add(ax, a)

    #Ex17. Parametric Curve Ex

class ParametricCurveExample(Scene): 
    def construct(self): 
        ax = Axes()
        cardioid = ax.plot_parametric_curve( 
            lambda t: np.array( 
                [ 
                    np.exp(1) * np.cos(t) * (1 - np.cos(t)), 
                    np.exp(1) * np.sin(t) * (1 - np.cos(t)), 
                    0, 
                ] 
            ), 
            t_range=[0, 2 * PI], 
            color="#0FF1CE", 
        ) 
        self.add(ax, cardioid)

    #18. PolarGraph Ex

class PolarGraphExample(Scene): 
    def construct(self): 
        plane = PolarPlane() 
        r = lambda theta: 2 * np.sin(theta * 5) 
        graph = plane.plot_polar_graph(r, [0, 2 * PI], color=ORANGE) 
        self.add(plane, graph)

    #19.Plot Surface Example

class PlotSurfaceExample(ThreeDScene): 
    def construct(self): 
        resolution_fa = 16 
        self.set_camera_orientation(phi=75 * DEGREES, theta=-60 * DEGREES) 
        axes = ThreeDAxes(x_range=(-3, 3, 1), y_range=(-3, 3, 1), z_range=(-5, 5, 1)) 
        def param_trig(u, v): 
            x = u 
            y = v 
            z = 2 * np.sin(x) + 2 * np.cos(y) 
            return z 
        trig_plane = axes.plot_surface( 
            param_trig, 
            resolution=(resolution_fa, resolution_fa), 
            u_range = (-3, 3), 
            v_range = (-3, 3), 
            colorscale = [BLUE, GREEN, YELLOW, ORANGE, RED], 
        ) 
        self.add(axes, trig_plane)

    #20.Polar to Point

class PolarToPointExample(Scene): 
    def construct(self): 
        polarplane_pi = PolarPlane(azimuth_units="PI radians", size=6) 
        polartopoint_vector = Vector(polarplane_pi.polar_to_point(3, PI/4)) 
        self.add(polarplane_pi) 
        self.add(polartopoint_vector)


#iv. NUmberPLane - Crates a cartesian plane with background lines

      #Ex1. NumberPlaneExample

class NumberPlaneExample(Scene):
    def construct(self): 
        number_plane = NumberPlane( 
            background_line_style={ 
                "stroke_color": TEAL, 
                "stroke_width": 4, 
                "stroke_opacity": 0.6 
            } 
        ) 
        self.add(number_plane)



        #Ex2. NumberPlaneScaled 

class NumberPlaneScaled(Scene): 
    def construct(self): 
        number_plane = NumberPlane( 
            x_range=(-4, 11, 1), 
            y_range=(-3, 3, 1), 
            x_length=5, 
            y_length=2, 
        ).move_to(LEFT*3)

        number_plane_scaled_y = NumberPlane( 
            x_range=(-4, 11, 1), 
            x_length=5, 
            y_length=4, 
        ).move_to(RIGHT*3)

        self.add(number_plane) 
        self.add(number_plane_scaled_y)

#v. PolarPLane - Creates a polar plane with background lines

    #PolarPlaneExample 

class PolarPlaneExample(Scene): 
    def construct(self): 
        polarplane_pi = PolarPlane( 
            azimuth_units="PI radians", 
            size=6, 
            azimuth_label_font_size=33.6, 
            radius_config={"font_size": 33.6}, 
        ).add_coordinates() 
        self.add(polarplane_pi)

#vi. ThreeDAxes - A 3D set of Axes

#a. Get axis Example

class GetAxisLabelsEx(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=2*PI/5, theta=PI/5)
        axes = ThreeDAxes()
        labels = axes.get_axis_labels(
            Text("x-axis").scale(0.7), Text("y-axis").scale(0.45), Text("z-axis").scale(0.45)
        )
        self.add(axes, labels)

#b. Get Y axis label

class GetYAxisLabelsEx(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes()
        lab = ax.get_y_axis_label(Tex("$y$-label"))
        self.set_camera_orientation(phi=2*PI/5, theta=PI/5)
        self.add(ax, lab)

#c. Get Z axis label

class GetYAxisLabelsEx(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes()
        lab = ax.get_z_axis_label(Tex("$z$-label"))
        self.set_camera_orientation(phi=2*PI/5, theta=PI/5)
        self.add(ax, lab)




#B. FUNCTIONS - Mobjects representing function graphs

#i. FunctionGraph - a parametricFunction that spans the length of the scene by default

class ExampleFunctionGraph(Scene): 
    def construct(self): 
        cos_func = FunctionGraph( 
            lambda t: np.cos(t) + 0.5 * np.cos(7 * t) + (1 / 7) * np.cos(14 * t), 
            color=RED, 
        )

        sin_func_1 = FunctionGraph( 
            lambda t: np.sin(t) + 0.5 * np.sin(7 * t) + (1 / 7) * np.sin(14 * t), 
            color=BLUE, 
        )

        sin_func_2 = FunctionGraph( 
            lambda t: np.sin(t) + 0.5 * np.sin(7 * t) + (1 / 7) * np.sin(14 * t), x_range=[-4, 4], 
            color=GREEN, 
        ).move_to([0, 1, 0])

        self.add(cos_func, sin_func_1, sin_func_2)


#ii. ImplicitFunction - An implicit function


#Ex1. 
class ImplicitFunctionExample(Scene): 
    def construct(self): 
        graph = ImplicitFunction( 
            lambda x, y: x * y ** 2 - x ** 2 * y - 2, 
            color=YELLOW 
        ) 
        self.add(NumberPlane(), graph)

#iii. ParametricFunction - A parametric function

     #Ex1. PlotParametricFunction

class PlotParametricFunction(Scene): 
    def func(self, t): 
        return (np.sin(2 * t), np.sin(3 * t), 0)

    def construct(self): 
        func = ParametricFunction(self.func, t_range = (0, TAU), fill_opacity=0).set_color(RED) 
        self.add(func.scale(3))

        #Ex2.ThreeDParametricSpring 

class ThreeDParametricSpring(ThreeDScene): 
    def construct(self): 
        curve1 = ParametricFunction( 
            lambda u: ( 
                1.2 * np.cos(u), 
                1.2 * np.sin(u), 
                u * 0.05 
            ), color=RED, t_range = (-3*TAU, 5*TAU, 0.01)
         ).set_shade_in_3d(True) 
        axes = ThreeDAxes() 
        self.add(axes, curve1) 
        self.set_camera_orientation(phi=80 * DEGREES, theta=-60 * DEGREES) 
        self.wait()

        #Ex3. DiscontinuousExample 

class DiscontinuousExample(Scene): 
    def construct(self): 
        ax1 = NumberPlane((-3, 3), (-4, 4)) 
        ax2 = NumberPlane((-3, 3), (-4, 4)) 
        VGroup(ax1, ax2).arrange() 
        discontinuous_function = lambda x: (x ** 2 - 2) / (x ** 2 - 4) 
        incorrect = ax1.plot(discontinuous_function, color=RED) 
        correct = ax2.plot( 
            discontinuous_function, 
            discontinuities=[-2, 2], # discontinuous points 
            dt=0.1, # left and right tolerance of discontinuity 
            color=GREEN, 
        ) 
        self.add(ax1, ax2, incorrect, correct)


#C. NUMBERLINE - MObjects representing a number line

#a. NumberLine - Creates a number line with tick marks

        #NumberLineExample 

class NumberLineExample(Scene): 
    def construct(self): 
        l0 = NumberLine( 
            x_range=[-10, 10, 2], 
            length=10, 
            color=BLUE, 
            include_numbers=True, 
            label_direction=UP,
         )

        l1 = NumberLine( 
            x_range=[-10, 10, 2], 
            unit_size=0.5, 
            numbers_with_elongated_ticks=[-2, 4], 
            include_numbers=True, font_size=24, 
        ) 
        num6 = l1.numbers[8] 
        num6.set_color(RED)

        l2 = NumberLine( 
            x_range=[-2.5, 2.5 + 0.5, 0.5], 
            length=12, 
            decimal_number_config={"num_decimal_places": 2}, 
            include_numbers=True, 
        )

        l3 = NumberLine( 
            x_range=[-5, 5 + 1, 1], 
            length=6, 
            include_tip=True, 
            include_numbers=True, 
            rotation=10 * DEGREES, 
        )

        line_group = VGroup(l0, l1, l2, l3).arrange(DOWN, buff=1) 
        self.add(line_group)

#b. UnitInterval


#D. PROBABILITY - Mobjects representing objects from probability theory and statistics

#i. BarChart - creates a bar chart

        #BarChartExample

class BarChartExample(Scene): 
    def construct(self): 
        chart = BarChart( 
            values=[-5, 40, -10, 20, -3], 
            bar_names=["one", "two", "three", "four", "five"], 
            y_range=[-20, 50, 10], 
            y_length=6, 
            x_length=10, 
            x_axis_config={"font_size": 36}, 
        )

        c_bar_lbls = chart.get_bar_labels(font_size=48)

        self.add(chart, c_bar_lbls)


            #Ex2.ChangeBarValuesExample

class ChangeBarValuesExample(Scene):
    def construct(self): 
        values=[-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]

        chart = BarChart( 
            values, 
            y_range=[-10, 10, 2],
            y_axis_config={"font_size": 24}, 
        ) 
        self.add(chart)

        chart.change_bar_values(list(reversed(values))) 
        self.add(chart.get_bar_labels(font_size=24))

        #Ex3. GetBarLabelsExample

class GetBarLabelsExample(Scene):
    def construct(self): 
        chart = BarChart(values=[10, 9, 8, 7, 6, 5, 4, 3, 2, 1], y_range=[0, 10, 1])

        c_bar_lbls = chart.get_bar_labels( 
            color=WHITE, label_constructor=MathTex, font_size=36 
        )

        self.add(chart, c_bar_lbls)

#ii. SampleSpace - A Mobject representing a 2d rectangular sampling space

class ExampleSampleSpace(Scene): 
    def construct(self): 
        poly1 = SampleSpace(stroke_width=15, fill_opacity=1) 
        poly2 = SampleSpace(width=5, height=3, stroke_width=5, fill_opacity=0.5) 
        poly3 = SampleSpace(width=2, height=2, stroke_width=5, fill_opacity=0.1) 
        poly3.divide_vertically(p_list=np.array([0.37, 0.13, 0.5]), colors=[BLACK, WHITE, GRAY], vect=RIGHT) 
        poly_group = VGroup(poly1, poly2, poly3).arrange() 
        self.add(poly_group)


#E. SCALE

#i. LinearBase - The default scaling class
#ii. LogBase - Scale for logarithmic graphs/ functions

    #5. logo - Utilities for Manim's logo and banner
#i. ManimBanner - Convenience class representing Manim's banner

      #Ex1. DarkThemeBanner

class DarkThemeBanner(Scene): 
    def construct(self): 
        banner = ManimBanner() 
        self.play(banner.create()) 
        self.play(banner.expand()) 
        self.wait() 
        self.play(Unwrite(banner))


        #Ex2. LightThemeBanner

class LightThemeBanner(Scene): 
    def construct(self): 
        self.camera.background_color = "#ece6e2" 
        banner = ManimBanner(dark_theme=False) 
        self.play(banner.create()) 
        self.play(banner.expand()) 
        self.wait() 
        self.play(Unwrite(banner))

        #Ex3. ExpandDirections

class ExpandDirections(Scene): 
    def construct(self): 
        banners = [ManimBanner().scale(0.5).shift(UP*x) for x in [-2, 0, 2]] 
        self.play( 
            banners[0].expand(direction="right"), 
            banners[1].expand(direction="center"), 
            banners[2].expand(direction="left"),
         )

    #6. MATRIX - Mobjects representing matrices

#EX1. MatrixExample
 
class MatrixExamples(Scene): 
    def construct(self): 
        m0 = Matrix([["\\pi", 0], [-1, 1]]) 

        m1 = IntegerMatrix([[1.5, 0.3], [12, 1.3]],  
                    left_bracket="(", 
                    right_bracket=")"
            ) 
 
        m2 = DecimalMatrix(
            [[3.456, 2.122], [33.2244, 12.33]], 
                    element_to_mobject_config={"num_decimal_places": 2}, 
                    left_bracket=r"\{", 
                    right_bracket=r"\}"
            )
         
        m3 = MobjectMatrix(
            [[Circle().scale(0.3), Square().scale(0.3)], 
             [MathTex("\\pi").scale(2), Star().scale(0.3)]], 
                    left_bracket=r"\langle",
                    right_bracket=r"\rangle"
            ) 
        m4 = Matrix([[2, 1], [-1, 3]], ).set_column_colors(RED, GREEN) 
        m5 = Matrix([[2, 1], [-1, 3]], ).set_row_colors(RED, GREEN) 
        g = Group( m0,m1,m2,m3,m4,m5 ).arrange_in_grid(buff=2) 
        self.add(g)


        #classes

#i. DecimalMatrix - A mobject that displays a matrix with decimal entries on the screen

#DecimalMatrixExample 

class DecimalMatrixExample(Scene): 
    def construct(self): 
        m0 = DecimalMatrix( 
            [[3.456, 2.122], [33.2244, 12]], 
            element_to_mobject_config={"num_decimal_places": 2}, 
            left_bracket="\{", right_bracket="\}") 
        self.add(m0)


#ii. IntegerMatrix - A mobject that displays a matrix with integer entries on the screen

class IntegerMatrixExample(Scene): 
    def construct(self): 
        m0 = IntegerMatrix( 
            [[3.7, 2], [42.2, 12]], 
            left_bracket="(", 
            right_bracket=")") 
        self.add(m0)

#iii. Matrix - A mobject that displays a matrix on the screen

#MatrixExample 1

class MatrixExamples(Scene): 
    def construct(self): 
        m0 = Matrix([[2, r"\pi"], [-1, 1]]) 
        m1 = Matrix([[2, 0, 4], [-1, 1, 5]], 
                    v_buff=1.3, 
                    h_buff=0.8, 
                    bracket_h_buff=SMALL_BUFF, 
                    bracket_v_buff=SMALL_BUFF, 
                    left_bracket=r"{", 
                    right_bracket=r"}") 
        m1.add(SurroundingRectangle(m1.get_columns()[1])) 
        m2 = Matrix([[2, 1], [-1, 3]], 
                    element_alignment_corner=UL, 
                    left_bracket="(", 
                    right_bracket=")") 
        m3 = Matrix([[2, 1], [-1, 3]], 
                    left_bracket=r"\langle", 
                    right_bracket=r"\rangle") 
        m4 = Matrix([[2, 1], [-1, 3]], 
                    ).set_column_colors(RED, GREEN) 
        m5 = Matrix([[2, 1], [-1, 3]], 
                    ).set_row_colors(RED, GREEN) 
        g = Group( m0,m1,m2,m3,m4,m5 
                  ).arrange_in_grid(buff=2) 
        self.add(g)

#BackgroundRectanglesExample, 2

class BackgroundRectanglesExample(Scene): 
    def construct(self): 
        background= Rectangle().scale(3.2) 
        background.set_fill(opacity=.5) 
        background.set_color([TEAL, RED, YELLOW]) 
        self.add(background) 
        m0 = Matrix([[12, -30], [-1, 15]], 
                    add_background_rectangles_to_entries=True) 
        m1 = Matrix([[2, 0], [-1, 1]], 
                    include_background_rectangle=True) 
        m2 = Matrix([[12, -30], [-1, 15]]) 
        g = Group(m0, m1, m2).arrange(buff=2) 
        self.add(g)

#GetBracketsExample, 3

class GetBracketsExample(Scene): 
    def construct(self): 
        m0 = Matrix([["\pi", 3], [1, 5]]) 
        bra = m0.get_brackets() 
        colors = [BLUE, GREEN] 
        for k in range(len(colors)): 
            bra[k].set_color(colors[k]) 
            self.add(m0)


#GetColumnsExample, 4 

class GetColumnsExample(Scene): 
    def construct(self): 
        m0 = Matrix([[r"\pi", 3], [1, 5]]) 
        m0.add(SurroundingRectangle(m0.get_columns()[1])) 
        self.add(m0)
    
#GetEntriesExample, 5

class GetEntriesExample(Scene): 
    def construct(self): 
        m0 = Matrix([[2, 3], [1, 5]]) 
        ent = m0.get_entries() 
        colors = [BLUE, GREEN, YELLOW, RED] 
        for k in range(len(colors)): 
            ent[k].set_color(colors[k]) 
            self.add(m0)  

#GetRowsExample, 6

class GetRowsExample(Scene): 
    def construct(self): 
        m0 = Matrix([["\pi", 3], [1, 5]]) 
        m0.add(SurroundingRectangle(m0.get_rows()[1])) 
        self.add(m0) 

#SetColumnColorsExample, 7

class SetColumnColorsExample(Scene): 
    def construct(self): 
        m0 = Matrix([["\pi", 1], [-1, 3]], 
                    ).set_column_colors([RED,BLUE], GREEN) 
        self.add(m0)

#SetRowColorsExample, 8

class SetRowColorsExample(Scene): 
    def construct(self): 
        m0 = Matrix([["\pi", 1], [-1, 3]], 
                    ).set_row_colors([RED,BLUE], GREEN) 
        self.add(m0)



#iv. MobjectMatrix - A mobject that displays a matrix of mobject entries on the screen

class MobjectMatrixExample(Scene): 
    def construct(self): 
        a = Circle().scale(0.3) 
        b = Square().scale(0.3) 
        c = MathTex("\pi").scale(2) 
        d = Star().scale(0.3) 
        m0 = MobjectMatrix([[a, b], [c, d]]) 
        self.add(m0)

# Determinant of a matrix

class DeterminantOfAMatrix(Scene):
    def construct(self): 
        matrix = Matrix([ 
            [2, 0], 
            [-1, 1]
        ])

        #scaling down the det string
        det = get_det_text(matrix, determinant=3, initial_scale_factor=1)

        #must add the matrix
        self.add(matrix) 
        self.add(det)



    #7. MOBJECT - Base classes for objects that can be displayed

    #Animation override example
#----------------------

#classes

#i. Group - Groups 2gether multiple Mobjects

 
#ii. Mobject - Mathematical Object: base class for objects that can be displayed on screen

#Example1. Next_to Updater

class NextToUpdater(Scene):
    def construct(self):
        def update_label(mobject):
            mobject.set_value(dot.get_center()[0])
            mobject.next_ro(dot)

            dot = Dot(RIGHT*3)
            label = DecimalNumber()
            label.add_updater(update_label)
            self.add(dot, label)

            self.play(dot, angle=TAU, about_point=ORIGIN, run_time=TAU, rate_func=linear)

#example2. DtUpdater

class DtUpdater(Scene):
    def construct(self):
        square = Square()

        #let the square rotate 90 deg per second
        square.add_updater(lambda mobject, dt: mobject.rotate(dt*90*DEGREES))
        self.add(square)
        self.wait(2)

#Example3: Animate Example

class AnimateExample(Scene):
    def construct(self):
        s = Square()
        self.play(Create(s))
        self.play(s.animate.shift(RIGHT))
        self.play(s.animate.scale(2))
        self.play(s.animate.rotate(PI / 2))
        self.play(Uncreate(s))

#Ex4. AnimateChain  
class AnimateChainEx(Scene):
    def construct(self):
        s = Square()
        self.play(Create(s))
        self.play(s.animate.shift(RIGHT).scale(2).rotate(PI / 2))
        self.play(Uncreate(s))

#Ex5. AnimateWithArguments

class AnimateWithArguments(Scene):
    def construct(self):
        s = Square()
        c = Circle()

        VGroup(s, c).arrange(RIGHT, buff=2)
        self.add(s, c)

        self.play(
            s.animate(run_time=2).rotate(PI / 2),
            c.animate(rate_func = there_and_back).shift(RIGHT),
        )

#Ex6. ApplyFunc Example
class ApplyFunc(Scene):
    def construct(self):
        c = Circle().scale(1.5)
        c_ref = c.copy()
        c.apply_complex_function(
            lambda x: np.exp(x*1j)
        )
        t = ValueTracker(0)
        c.add_updater(
            lambda x: x.become(c_ref.copy().apply_complex_function(
                lambda x: np.exp(x+t.get_value()*1j)
            )).set_color(BLUE)
        )
        self.add(c_ref)
        self.play(TransformFromCopy(c_ref, c))
        self.play(t.animate.set_value(TAU), run_time=3)

#Ex7. Arrange Example

class Arrange(Scene):
    def construct(self):
        s1 = Square()
        s2 = Square()
        s3 = Square()
        s4 = Square()
        x = VGroup(s1, s2, s3, s4).set_x(0).arrange(buff=1)
        self.add(x)

#Ex8. ExampleBoxes

class ExampleBoxes(Scene):
    def construct(self):
        boxes = VGroup(*[Square()for s in range (0, 6)])
        boxes.arrange_in_grid(rows=2, buff=0.1)
        self.add(boxes)

#Ex9. Arrange in Grid

class ArrangeInGrid(Scene): 
    def construct(self): 
        boxes = VGroup(*[ 
            Rectangle(WHITE, 0.5, 0.5).add(Text(str(i+1)).scale(0.5)) 
            for i in range(24) 
        ]) 
        self.add(boxes)

        boxes.arrange_in_grid( 
            buff=(0.25,0.5), 
            col_alignments="lccccr", 
            row_alignments="uccd", 
            col_widths=[1, *[None]*4, 1], 
            row_heights=[1, None, None, 1], 
            flow_order="dr" 
            )
        
#Ex10. ArrangeSumobjectsExample
class ArrangeSumobjectsExample(Scene): 
    def construct(self): 
        s= VGroup(*[Dot().shift(i*0.1*RIGHT*np.random.uniform(-1,1)+UP*np.random.uniform(-1,1)) for i in range(0,15)]) 
        s.shift(UP).set_color(BLUE) 
        s2= s.copy().set_color(RED) 
        s2.arrange_submobjects() 
        s2.shift(DOWN) 
        self.add(s,s2)

#Ex11. BecomeScene

class BecomeScene(Scene): 
    def construct(self): 
        circ = Circle(fill_color=RED, fill_opacity=0.8) 
        square = Square(fill_color=BLUE, fill_opacity=0.2) 
        self.add(circ) 
        self.wait(0.5) 
        circ.become(square) 
        self.wait(0.5)

#Ex12. Flip Example

class FlipEx(Scene):
    def construct(self):
        s = Line(len, RIGHT+UP).shift(4*LEFT)
        self.add(s)
        s2= s.copy().flip()
        self.add(s2)

#Ex13. AngleMidPoint

class AngleMidPoint(Scene):
    def construct(self):
        line1 = Line(ORIGIN, 2*RIGHT)
        line2 = Line(ORIGIN, 2*RIGHT).rotate_about_origin(80*DEGREES)

        a = Angle(line1, line2, radius=1.5, other_angle=False)
        d = Dot(a.get_midpoint()).set_color(RED)

        self.add(line1, line2, a, d)
        self.wait()

#Ex14. Height Example

class HeightEx(Scene):
    def construct(self):
        decimal = DecimalNumber().to_edge(UP).interpolate
        rect= Rectangle(color=BLUE)
        rect_copy = rect.copy().set_stroke(GREY, opacity=0.5)

        decimal.add_updater(lambda d: d.set_value(rect.height))

        self.add(rect_copy, rect, decimal)
        self.play(rect.animate.set(height=5))
        self.wait()

#Ex15. Interpolate Example

class InterpolateExample(Scene): 
    def construct(self):

        #No need for point alignment:
        dotL = Dot(color=DARK_GREY).to_edge(LEFT) 
        dotR = Dot(color=YELLOW).scale(10).to_edge(RIGHT) 
        dotMid1 = VMobject().interpolate(dotL, dotR, alpha=0.1) 
        dotMid2 = VMobject().interpolate(dotL, dotR, alpha=0.25) 
        dotMid3 = VMobject().interpolate(dotL, dotR, alpha=0.5) 
        dotMid4 = VMobject().interpolate(dotL, dotR, alpha=0.75) 
        dots = VGroup(dotL, dotR, dotMid1, dotMid2, dotMid3, dotMid4)

        #Needs point alignment:
        line = Line(ORIGIN, UP).to_edge(LEFT) 
        sq = Square(color=RED, fill_opacity=1, stroke_color=BLUE).to_edge(RIGHT) 
        line.align_points(sq) 
        mid1 = VMobject().interpolate(line, sq, alpha=0.1) 
        mid2 = VMobject().interpolate(line, sq, alpha=0.25) 
        mid3 = VMobject().interpolate(line, sq, alpha=0.5) 
        mid4 = VMobject().interpolate(line, sq, alpha=0.75) 
        linesquares = VGroup(line, sq, mid1, mid2, mid3, mid4)

        self.add(VGroup(dots, linesquares).arrange(DOWN, buff=1))

#Ex16. InvertSumobjectsExample

class InvertSumobjectsExample(Scene): 
    def construct(self): 
        s = VGroup(*[Dot().shift(i*0.1*RIGHT) for i in range(-20,20)]) 
        s2 = s.copy() 
        s2.invert() 
        s2.shift(DOWN) 
        self.play(Write(s), Write(s2))

#Ex17. MatchPOintsScene

class MatchPoints(Scene):
    def construct(self):
        circ = Circle(fill_color = RED, fill_opacity= 0.8)
        square = Square(fill_color = BLUE, fill_opacity = 0.2)
        self.add(circ)
        self.wait(0.5)
        self.play(circ.animate.match_points(square))
        self.wait(0.5)

#Ex18. Geometric Shapes

class GeometricShapes(Scene):
    def construct(self):
        d = Dot()
        c = Circle()
        s = Square()
        t = Triangle()
        d.next_to(c, RIGHT)
        s.next_to(c, LEFT)
        t.next_to(c, DOWN)
        self.add(d, c, s, t)

#Ex19. Rotate Method Ex

class RotateMethodEx(Scene):
    def construct(self):
        circ = Circle(radius=1, color=BLUE)
        line = Line(start = ORIGIN, end= RIGHT)
        arrow1 = Arrow(staet= ORIGIN, end = RIGHT, buff = 0, color=GOLD)
        group1 = VGroup(circ, line, arrow1)

        group2 = group1.copy()
        arrow2 = group2[2]
        arrow2.rotate(angle=PI / 4, about_point=arrow2.get_start())

        group3 = group1.copy()
        arrow3 = group3[2]
        arrow3.rotate(angle=120 * DEGREES, about_point=arrow3.get_start())
        
        self.add(VGroup(group1, group2, group3).arrange(RIGHT, buff=1))

#Ex20. MobjectScaleEx

class MobjectScale(Scene):
    def construct(self):
        f1= Text("F")
        f2= Text("F").scale(2)
        f3= Tex("F").scale(0.5)
        f4= Text("F").scale(-1)

        vgroup = VGroup(f1, f2, f3, f4).arrange(6 *RIGHT)
        self.add(vgroup)

#Ex21. Change Default Text color

config.background_color = WHITE

class ChangeDefaultTextColor(Scene):
    def construct(self):
        Text.set_default(color=BLACK)
        self.add(Text("Changing default values is easy!"))

        #we revert the color back to prevent a bug in the docs

        Text.set_default(color=WHITE)

#Ex22. SetZIndex

class SetZIndex(Scene): 
    def construct(self): 
        text = Text('z_index = 3', color = PURE_RED).shift(UP).set_z_index(3) 
        square = Square(2, fill_opacity=1).set_z_index(2) 
        tex = Tex(r'zIndex = 1', color = PURE_BLUE).shift(DOWN).set_z_index(1) 
        circle = Circle(radius = 1.7, color = GREEN, fill_opacity = 1) # z_index = 0

        #Displaying order is now defined by z_index values
        self.add(text) 
        self.add(square) 
        self.add(tex) 
        self.add(circle)

#Ex23. ShuffleSubmobjectsExample

class ShuffleSubmobjectsExample(Scene): 
    def construct(self): 
        s= VGroup(*[Dot().shift(i*0.1*RIGHT) for i in range(-20,20)]) 
        s2= s.copy() 
        s2.shuffle_submobjects() 
        s2.shift(DOWN)
        self.play(Write(s), Write(s2))

#Ex24. ToCornerExample

class ToCornerExample(Scene): 
    def construct(self): 
        c = Circle()
        c.to_corner(UR) 
        t = Tex("To the corner!") 
        t2 = MathTex("x^3").shift(DOWN) 
        self.add(c,t,t2) 
        t.to_corner(DL, buff=0) 
        t2.to_corner(UL, buff=1.5)

#Ex25. ToEdgeExample

class ToEdgeExample(Scene): 
    def construct(self): 
        tex_top = Tex("I am at the top!") 
        tex_top.to_edge(UP) 
        tex_side = Tex("I am moving to the side!") 
        c = Circle().shift(2*DOWN) 
        self.add(tex_top, tex_side, c) 
        tex_side.to_edge(LEFT) 
        c.to_edge(RIGHT, buff=0)

#Ex26. Width Example

class WidthEx(Scene):
    def construct(self):
        decimal = DecimalNumber().to_edge(UP)
        rect = Rectangle(color=BLUE)
        rect_copy = rect.copy().set_stroke(GRAY, opacity=0.5)

        decimal.add_updater(lambda d: d.set_value(rect.width))

        self.add(rect_copy, rect, decimal)
        self.play(rect.animate.set(width=7))
        self.wait()



#8. ------------ SVG - mobjects related to SVG images --------
#---------------  #modules --------------

#i. brace - Mobject representing curly braces

#Classes

#a. ArcBrace - Creates a brace that wraps around an arc

class ArcBraceExample(Scene): 
    def construct(self): 
        arc_1 = Arc(radius=1.5,start_angle=0,angle=2*PI/3).set_color(RED) 
        brace_1 = ArcBrace(arc_1,LEFT) 
        group_1 = VGroup(arc_1,brace_1)

        arc_2 = Arc(radius=3,start_angle=0,angle=5*PI/6).set_color(YELLOW) 
        brace_2 = ArcBrace(arc_2) 
        group_2 = VGroup(arc_2,brace_2)

        arc_3 = Arc(radius=0.5,start_angle=-0,angle=PI).set_color(BLUE) 
        brace_3 = ArcBrace(arc_3) 
        group_3 = VGroup(arc_3,brace_3)

        arc_4 = Arc(radius=0.2,start_angle=0,angle=3*PI/2).set_color(GREEN) 
        brace_4 = ArcBrace(arc_4) 
        group_4 = VGroup(arc_4,brace_4)
        
        arc_group = VGroup(group_1, group_2, group_3, group_4).arrange_in_grid(buff=1.5) 
        self.add(arc_group.center())


#b. Brace - Takes a mobjext and draws a brace adjacent to it

class BraceExample(Scene): 
    def construct(self): 
        s = Square() 
        self.add(s) 
        for i in np.linspace(0.1,1.0,4): 
            br = Brace(s, sharpness=i) 
            t = Text(f"sharpness= {i}").next_to(br, RIGHT) 
            self.add(t) 
            self.add(br) 
        VGroup(*self.mobjects).arrange(DOWN, buff=0.2)


#c. BraceBetweenPOints - Similar to brace, but instead of taking a mobject, it uses 2 points to place the brace

class BraceBPExample(Scene): 
    def construct(self): 
        p1 = [0,0,0] 
        p2 = [1,2,0] 
        brace = BraceBetweenPoints(p1,p2) 
        self.play(Create(NumberPlane())) 
        self.play(Create(brace)) 
        self.wait(2)

#d. BraceLabel - Creates a brace with a label attached

#e. BraceText - Create a brace with a text label attached

class BraceTextExample(Scene): 
    def construct(self): 
        s1 = Square().move_to(2*LEFT) 
        self.add(s1) 
        br1 = BraceText(s1, "Label") 
        self.add(br1)

        s2 = Square().move_to(2*RIGHT) 
        self.add(s2) 
        br2 = BraceText(s2, "Label")

        br2.change_label("new") 
        self.add(br2) 
        self.wait(0.1)

#ii. svg_mobject - MObjects generated from an svg file

   #Classes

#a. SVGMobject - A vetorized mobject created from importing an SVG file


#b. VMobjectFromSVGPath - A vectorized mobject representing an SVG path


    #9. ----------TABLE - Mobjects representing tables ----------

    #Ex. Table Example

class TableEx2 (Scene):
    def construct(self):
        t0 = Table(
            [["First", "Second"],
            ["Third", "Fourth"]],
            row_labels=[Text("R1"), Text("R2")],
            col_labels=[Text("C1"), Text("C2")],
            top_left_entry=Text("TOP")
        )
        t0.add_highlighted_cell((2,2), color=GREEN)
        x_vals = np.linspace(-2, 2, 5)
        y_vals = np.exp(x_vals)

        t1 = DecimalTable(
            [x_vals, y_vals],
            row_labels=[MathTex("x"), MathTex("f(x)")],
            include_outer_lines=True
        )
        t1.add(t1.get_cell((2,2), color=RED))

        t2 = MathTable(
            [
                ["+", 0, 5, 10],
                [0, 0, 5, 10],
                [2, 2, 7, 12],
                [4, 4, 9, 14]
            ],
             include_outer_lines=True
        )
        t2.get_horizontal_lines()[:3].set_color(BLUE)
        t2.get_vertical_lines()[:3].set_color(BLUE)
        t2.get_horizontal_lines()[:3].set_z_index(1)
        cross = VGroup(
            Line(UP + LEFT, DOWN + RIGHT),
            Line(UP + RIGHT, DOWN + LEFT)
        )

        a = Circle().set_color(RED).scale(0.5)
        b = cross.set_color(BLUE).scale(0.5)

        t3 = MobjectTable(
            [[a.copy(), b.copy(), a.copy()],
             [b.copy(), a.copy(), a.copy()],
             [a.copy(), b.copy(), b.copy()]]
        )
        t3.add(Line(
            t3.get_corner(DL), t3.get_corner(UR)
        ).set_color(RED))
        vals = np.arange(1, 21).reshape(5, 4)

        t4 = IntegerTable(
            vals,
            include_outer_lines= True
        )

        g1 = Group(t0, t1).scale(0.5).arrange(buff=1).to_edge(UP, buff=1)
        g2 = Group(t2, t3, t4).scale(0.5).arrange(buff=1).to_edge(DOWN, buff=1)

        self.add(g1, g2)

    #======  classes  =====

#i. DecimalTable - A specialized Table mobject for use with DecimalNumber to display decimal entries

class DecimalTableExample(Scene): 
    def construct(self): 
        x_vals = [-2,-1,0,1,2]
        y_vals = np.exp(x_vals) 
        t0 = DecimalTable( 
            [x_vals, y_vals], 
            row_labels=[MathTex("x"), MathTex("f(x)=e^{x}")], 
            h_buff=1, 
            element_to_mobject_config={"num_decimal_places": 2})
        self.add(t0)
    
#ii. IntegerTable - A specialized Table mobject for use with Integer

class IntegerTableExample(Scene): 
    def construct(self): 
        t0 = IntegerTable( 
            [[0,30,45,60,90], 
             [90,60,45,30,0]], 
             col_labels=[ 
                 MathTex(r"\frac{\sqrt{0}}{2}"), 
                 MathTex(r"\frac{\sqrt{1}}{2}"), 
                 MathTex(r"\frac{\sqrt{2}}{2}"), 
                 MathTex(r"\frac{\sqrt{3}}{2}"), 
                 MathTex(r"\frac{\sqrt{4}}{2}")], 
            row_labels=[MathTex(r"\sin"), MathTex(r"\cos")], 
            h_buff=1, 
            element_to_mobject_config={"unit": r"^{\circ}"}) 
        self.add(t0)

#iii. MathTable - A specialized Table mobject for use with LaTex

class MathTableExample(Scene): 
    def construct(self): 
        t0 = MathTable( 
            [["+", 0, 5, 10], 
             [0, 0, 5, 10], 
             [2, 2, 7, 12], 
             [4, 4, 9, 14]], 
             include_outer_lines=True) 
        self.add(t0)

#iv. MobjectTable - A specialized Table mobject for use with Mobject

class MobjectTableExample(Scene): 
    def construct(self): 
        cross = VGroup( 
            Line(UP + LEFT, DOWN + RIGHT), 
            Line(UP + RIGHT, DOWN + LEFT), 
        ) 
        a = Circle().set_color(RED).scale(0.5) 
        b = cross.set_color(BLUE).scale(0.5) 
        t0 = MobjectTable( 
            [[a.copy(),b.copy(),a.copy()], 
             [b.copy(),a.copy(),a.copy()], 
             [a.copy(),b.copy(),b.copy()]] 
        ) 
        line = Line( 
            t0.get_corner(DL), 
            t0.get_corner(UR) 
        ).set_color(RED) 
        
        self.add(t0, line)

        #v.==== Table - A mobject that displays a table on the screen  ====

#Ex1. TableExamples 

class TableExamples(Scene): 
    def construct(self): 
        t0 = Table( 
            [["This", "is a"], 
             ["simple", "Table in \n Manim."]]
        ) 
        t1 = Table( 
            [["This", "is a"], 
             ["simple", "Table."]], 
             row_labels=[Text("R1"), 
                         Text("R2")], 
                         col_labels=[Text("C1"), Text("C2")]
        ) 
        t1.add_highlighted_cell((2,2), color=YELLOW) 
        t2 = Table( 
            [["This", "is a"], 
             ["simple", "Table."]], 
             row_labels=[Text("R1"), 
                         Text("R2")], 
                         col_labels=[Text("C1"), Text("C2")], 
                         top_left_entry=Star().scale(0.3), 
                         include_outer_lines=True, 
                         arrange_in_grid_config={"cell_alignment": RIGHT}
        ) 
        t2.add(t2.get_cell((2,2), color=RED)) 
        t3 = Table( 
            [["This", "is a"], 
             ["simple", "Table."]], 
             row_labels=[Text("R1"), 
                         Text("R2")], 
                         col_labels=[Text("C1"), 
                                     Text("C2")], 
                                     top_left_entry=Star().scale(0.3), 
                                     include_outer_lines=True, 
                                     line_config={"stroke_width": 1, "color": YELLOW}
        ) 
        t3.remove(*t3.get_vertical_lines()) 
        g = Group( t0,t1,t2,t3 ).scale(0.7).arrange_in_grid(buff=1) 
        self.add(g)

#Ex2. BackgroundRectanglesExample

class BackgroundRectanglesExample(Scene): 
    def construct(self): 
        background = Rectangle(height=6.5, width=13) 
        background.set_fill(opacity=.5) 
        background.set_color([TEAL, RED, YELLOW]) 
        self.add(background) 
        t0 = Table( 
            [["This", "is a"], 
             ["simple", "Table."]], 
             add_background_rectangles_to_entries=True) 
        t1 = Table( 
            [["This", "is a"], 
             ["simple", "Table."]], 
             include_background_rectangle=True) 
        g = Group(t0, t1).scale(0.7).arrange(buff=0.5) 
        self.add(g)

#Ex3. AddHighlightedCellExample 

class AddHighlightedCellExample(Scene): 
    def construct(self): 
        table = Table( 
            [["First", "Second"], 
             ["Third","Fourth"]], 
             row_labels=[Text("R1"), Text("R2")], 
             col_labels=[Text("C1"), Text("C2")]) 
        table.add_highlighted_cell((2,2), color=GREEN) 
        self.add(table)

#Ex4. CreateTableEx

class CreateTableEx(Scene):
    def construct(self):
        table = Table(
            [["First", "Second"],
             ["Third", "Fourth"]],
             row_labels=[Text("R1"), Text("R2")],
             col_labels=[Text("C1"), Text("C2")],
             include_outer_lines=True)
        self.play(table.create())
        self.wait()
        

#Ex5. GetCellExample 

class GetCellExample(Scene): 
    def construct(self): 
        table = Table( 
            [["First", "Second"], 
             ["Third","Fourth"]], 
             row_labels=[Text("R1"), Text("R2")], 
             col_labels=[Text("C1"), Text("C2")]) 
        cell = table.get_cell((2,2), color=RED) 
        self.add(table, cell)

#Ex6. GetColLabelsExample

class GetColLabelsExample(Scene): 
    def construct(self): 
        table = Table( 
            [["First", "Second"], 
             ["Third","Fourth"]], 
             row_labels=[Text("R1"), Text("R2")], 
             col_labels=[Text("C1"), Text("C2")]) 
        lab = table.get_col_labels() 
        for item in lab: 
            item.set_color(random_bright_color()) 
            self.add(table)

#Ex7. GetColumnsExample

class GetColumnsExample(Scene): 
    def construct(self): 
        
        table = Table( [["First", "Second"], 
                        ["Third","Fourth"]], 
                        row_labels=[Text("R1"), Text("R2")], 
                        col_labels=[Text("C1"), Text("C2")]) 
        table.add(SurroundingRectangle(table.get_columns()[1])) 
        self.add(table)

#Ex8. GetEntriesExample

class GetEntriesExample(Scene): 
    def construct(self): 
        table = Table( 
            [["First", "Second"], 
             ["Third","Fourth"]], 
             row_labels=[Text("R1"), Text("R2")], 
             col_labels=[Text("C1"), Text("C2")]) 
        ent = table.get_entries() 
        for item in ent: 
            item.set_color(random_bright_color()) 
        table.get_entries((2,2)).rotate(PI) 
        self.add(table)

#Ex9. GetEntriesWithoutLabelsExample

class GetEntriesWithoutLabelsExample(Scene): 
    def construct(self): 
        table = Table( 
            [["First", "Second"], 
             ["Third","Fourth"]], 
             row_labels=[Text("R1"), Text("R2")], 
             col_labels=[Text("C1"), Text("C2")]) 
        ent = table.get_entries_without_labels() 
        colors = [BLUE, GREEN, YELLOW, RED] 
        for k in range(len(colors)): 
            ent[k].set_color(colors[k]) 
        table.get_entries_without_labels((2,2)).rotate(PI) 
        self.add(table)

#Ex10. GetHighlightedCellExample 

class GetHighlightedCellExample(Scene): 
    def construct(self): 
        table = Table( 
            [["First", "Second"], 
             ["Third","Fourth"]], 
             row_labels=[Text("R1"), Text("R2")], 
             col_labels=[Text("C1"), Text("C2")]) 
        highlight = table.get_highlighted_cell((2,2), color=GREEN) 
        table.add_to_back(highlight) 
        self.add(table)

#Ex11. GetHorizontalLinesExample

class GetHorizontalLinesExample(Scene): 
    def construct(self): 
        table = Table( 
            [["First", "Second"], 
             ["Third","Fourth"]], 
            row_labels=[Text("R1"), Text("R2")], 
            col_labels=[Text("C1"), Text("C2")]) 
        table.get_horizontal_lines().set_color(RED) 
        self.add(table)

#Ex12. GetLabelsExample

class GetLabelsExample(Scene):
    def construct(self): 
        table = Table( 
            [["First", "Second"], 
             ["Third","Fourth"]], 
             row_labels=[Text("R1"), Text("R2")], 
             col_labels=[Text("C1"), Text("C2")]) 
        lab = table.get_labels() 
        colors = [BLUE, GREEN, YELLOW, RED] 
        for k in range(len(colors)): 
            lab[k].set_color(colors[k]) 
        self.add(table)

#Ex13. GetRowLabelsExample

class GetRowLabelsExample(Scene): 
    def construct(self): 
        table = Table( 
            [["First", "Second"], 
             ["Third","Fourth"]], 
             row_labels=[Text("R1"), Text("R2")], 
             col_labels=[Text("C1"), Text("C2")]) 
        lab = table.get_row_labels() 
        for item in lab: 
            item.set_color(random_bright_color()) 
        self.add(table)

#Ex13. GetRowsExample save_last_frame :

class GetRowsExample(Scene): 
    def construct(self): 
        table = Table( 
            [["First", "Second"], 
             ["Third","Fourth"]], 
             row_labels=[Text("R1"), Text("R2")], 
             col_labels=[Text("C1"), Text("C2")]) 
        table.add(SurroundingRectangle(table.get_rows()[1])) 
        self.add(table)
    
#Ex14. GetVerticalLinesExample 

class GetVerticalLinesExample(Scene): 
    def construct(self): 
        table = Table( 
            [["First", "Second"], 
             ["Third","Fourth"]], 
             row_labels=[Text("R1"), Text("R2")], 
             col_labels=[Text("C1"), Text("C2")]) 
        table.get_vertical_lines()[0].set_color(RED) 
        self.add(table)

#Ex15. MobjectScaleExample

class MobjectScaleExample(Scene): 
    def construct(self): 
        c1 = Circle(1, RED).set_x(-1) 
        c2 = Circle(1, GREEN).set_x(1)

        vg = VGroup(c1, c2) 
        vg.set_stroke(width=50) 
        self.add(vg)

        self.play( 
            c1.animate.scale(.25), 
            c2.animate.scale(.25, 
                             scale_stroke=True) 
        )


#Ex16. SetColumnColorsExample 

class SetColumnColorsExample(Scene): 
    def construct(self): 
        table = Table( 
            [["First", "Second"], 
             ["Third","Fourth"]], 
             row_labels=[Text("R1"), Text("R2")], 
             col_labels=[Text("C1"), Text("C2")] 
        ).set_column_colors([RED,BLUE], GREEN) 
        self.add(table)

#Ex17. SetRowColorsExample 

class SetRowColorsExample(Scene): 
    def construct(self): 
        table = Table( 
            [["First", "Second"], 
             ["Third","Fourth"]], 
             row_labels=[Text("R1"), Text("R2")], 
             col_labels=[Text("C1"), Text("C2")] 
        ).set_row_colors([RED,BLUE], GREEN) 
        self.add(table)


    #10. --------TEXT - Mobjects used to display Text using Pango or Latex -------------

#Modules

#i. code_mobject - Mobject representing highlighted source code listings

#classes 

#a. Code - a highlighted source code listing (We can also render code passed as a string. As the automatic language detection can be a bit flaky, it's recommended to specify the language explicitly)

class CodeFromString(Scene): 
    def construct(self): 
        code = '''from manim import Scene, Square

class FadeInSquare(Scene): 
    def construct(self): 
        s = Square() 
        self.play(FadeIn(s)) 
        self.play(s.animate.scale(2)) 
        self.wait()'''

        rendered_code = Code( 
            code_string=code, 
            language="python", 
            background="window", 
            background_config={"stroke_color": "maroon"}, 
        ) 
        self.add(rendered_code)


#ii. --------NUMBERS - Mobjects representing numbers --------

#classes

#a. DecimalNumber - A mobject representing a decimal number

class MovingSquareWithUpdaters(Scene):
    def construct(self):
       decimal = DecimalNumber(
           0,
           show_ellipsis=True,
           num_decimal_places=3,
           include_sign=True,
           unit=r"\text{M-Units}",
           unit_buff_per_font_unit=0.003
       )
       square = Square().to_edge(UP)

       decimal.add_updater(lambda d: d.next_to(square, RIGHT))
       decimal.add_updater(lambda d: d.set_value(square.get_center()[1]))
       self.add(square, decimal)
       self.play(
           square.animate.to_edge(DOWN),
           rate_func=there_and_back,
           run_time=5,
       )
       self.wait()


#b. Integer - A class for displaying integers
class IntegerExample(Scene): 
    def construct(self):
        self.add(Integer(number=2.5).set_color(ORANGE).scale(2.5).set_x(-0.5).set_y(0.8)) 
        self.add(Integer(number=3.14159, show_ellipsis=True).set_x(3).set_y(3.3).scale(3.14159)) 
        self.add(Integer(number=42).set_x(2.5).set_y(-2.3).set_color_by_gradient(BLUE, TEAL).scale(1.7)) 
        self.add(Integer(number=6.28).set_x(-1.5).set_y(-2).set_color(YELLOW).scale(1.4))


#c. Variable - A class for displaying text that shows "label=value" with the value continuously updated from a ValueTracker

class VariablesWithValueTracker(Scene): 
    def construct(self): 
        var = 0.5 
        on_screen_var = Variable(var, Text("var"), num_decimal_places=3)

        #You can also change the colours for the label and value
        on_screen_var.label.set_color(RED) 
        on_screen_var.value.set_color(GREEN)

        self.play(Write(on_screen_var))
        #The above line will just display the variable with its initial value on the screen. If you also wish to update it, you can do so by accessing the tracker attribute
        self.wait() 
        var_tracker = on_screen_var.tracker 
        var = 10.5 
        self.play(var_tracker.animate.set_value(var)) 
        self.wait()

        int_var = 0 
        on_screen_int_var = Variable( 
            int_var, Text("int_var"), var_type=Integer 
        ).next_to(on_screen_var, DOWN) 
        on_screen_int_var.label.set_color(RED) 
        on_screen_int_var.value.set_color(GREEN)

        self.play(Write(on_screen_int_var)) 
        self.wait() 
        var_tracker = on_screen_int_var.tracker 
        var = 10.5 
        self.play(var_tracker.animate.set_value(var)) 
        self.wait()

        #If you wish to have a somewhat more complicated label for your variable with subscripts, superscripts, etc. the default class for the label is MathTex
        subscript_label_var = 10 
        on_screen_subscript_var = Variable(subscript_label_var, "{a}_{i}").next_to( 
            on_screen_int_var, DOWN 
        ) 
        self.play(Write(on_screen_subscript_var)) 
        self.wait()

    #Ex2 VariableExample

class VariableExample(Scene): 
    def construct(self): 
        start = 2.0

        x_var = Variable(start, 'x', num_decimal_places=3) 
        sqr_var = Variable(start**2, 'x^2', num_decimal_places=3) 
        Group(x_var, sqr_var).arrange(DOWN)

        sqr_var.add_updater(lambda v: v.tracker.set_value(x_var.tracker.get_value()**2))

        self.add(x_var, sqr_var) 
        self.play(x_var.tracker.animate.set_value(5), run_time=2, rate_func=linear) 
        self.wait(0.1)


#iii. tex_mobject - Mobjects representing text rendered using LaTex

#classes

#a. BulletList - A bulleted list

class BulletedListExample(Scene): 
    def construct(self): 
        blist = BulletedList("Item 1", "Item 2", "Item 3", height=2, width=2) 
        blist.set_color_by_tex("Item 1", RED) 
        blist.set_color_by_tex("Item 2", GREEN) 
        blist.set_color_by_tex("Item 3", BLUE) 
        self.add(blist)

#b. MathTex - A string compiled with LaTex in math mode

class Formula(Scene): 
    def construct(self): 
        t = MathTex(r"\int_a^b f'(x) dx = f(b)- f(a)") 
        self.add(t)


#c. SingleStringMAthTex -Elementary building block for rendering text with LaTex


#d. Tex - A string compiled with LaTex in normal mode

#e. Tiltle - A mobject representing an underlined title

import manim

class TitleExample(Scene): 
    def construct(self): 
        banner = ManimBanner() 
        title = Title(f"Manim version {manim.__version__}") 
        self.add(banner, title)


#text_mobject - Mobjects used for displaying (non-LaTex)text

#Ex1. Example1Text

class Example1Text(Scene): 
    def construct(self): 
        text = Text('Hello world').scale(3) 
        self.add(text)

#TextAlighnmentExample

class TextAlignmentEx(Scene):
    def construct(self):
       title = Text("K-means clustering and Logistic Regression", color = WHITE)
       title.scale(0.75)
       self.add(title.to_edge(UP))

       t1 = Text("1. Measuring").set_color(WHITE)
       t2 =Text("2. Clustering").set_color(WHITE)
       t3 = Text("3. Regression").set_color(WHITE)
       t4 = Text("4. Prediction").set_color(WHITE)

       x= VGroup(t1, t2, t3, t4).arrange(direction=DOWN, aligned_edge=LEFT).scale(0.7).next_to(ORIGIN, DR)
       x.set_opacity(0.5)
       x.submobjects[1].set_opacity(1)
       self.add(x)

       #classes

#i. MarkUpText - Display(non-LaTex) text rendered using Pango

      #Ex1. MarkupExample 

class MarkupExample(Scene): 
    def construct(self): 
        text = MarkupText('<span foreground="blue" size="x-large"> Blue text</span> is <i>cool</i>!"') 
        self.add(text)

    #Ex2. BasicMarkupExample 

class BasicMarkupExample(Scene): 
    def construct(self): 
        text1 = MarkupText("<b>foo</b> <i>bar</i> <b><i>foobar</i></b>") 
        text2 = MarkupText("<s>foo</s> <u>bar</u> <big>big</big> <small>small</small>") 
        text3 = MarkupText("H<sub>2</sub>O and H<sub>3</sub>O<sup>+</sup>") 
        text4 = MarkupText("type <tt>help</tt> for help") 
        text5 = MarkupText( 
            '<span underline="double">foo</span> <span underline="error">bar</span>' 
        ) 
        group = VGroup(text1, text2, text3, text4, text5).arrange(DOWN) 
        self.add(group)

    #Ex3. Color Example

class ColorEx(Scene):
    def construct(self):
        text1 = MarkupText(
            f'all in red <span fgcolor="{YELLOW}">except this</span>', color=RED
        )
        text2 = MarkupText("nice gradient", gradient=(BLUE, GREEN))
        text3 = MarkupText(
            'nice <gradient from="RED" to="YELLOW">intermediate</gradient> gradient',
            gradient=(BLUE, GREEN),
        )
        text4 = MarkupText(
            'fl ligature <gradient from="RED" to="YELLOW">causing trouble</gradient> here'
        )
        text5 = MarkupText(
            'fl ligature <gradient from="RED" to="YELLOW" offset="1">defeated</gradient> with offset'
        )
        text6 = MarkupText(
            'fl ligature <gradient from="RED" to="YELLOW" offset="1">floating</gradient> inside'
        )
        text7 = MarkupText(
            'fl ligature <gradient from="RED" to="YELLOW" offset="1,1">floating</gradient> inside'
        )
        group = VGroup(text1, text2, text3, text4, text5, text6, text7).arrange(DOWN)
        self.add(group)

        #Ex4. Underline Example

class UnderlineExample(Scene):
    def construct(self):
        text1 = MarkupText(
            '<span underline="double" underline_color="green">bla</span>'
        )
        text2 = MarkupText(
            '<span underline="single" underline_color="green">xxx</span><gradient from="#ffff00" to="RED">aabb</gradient>y'
        )
        text3 = MarkupText(
            '<span underline="double" underline_color="green">xxx</span><gradient from="#ffff00" to="RED offset="-1">aabb</gradient>y'
        )
        text4 = MarkupText(
            '<span underline="double" underline_color="green">xxx</span><gradient from="#ffff00" to="RED">aabb</gradient>y'
        )
        text5 = MarkupText(
            '<span underline="double" underline_color="green">xxx</span><gradient from="#ffff00" to="RED" offset="-2">aabb</gradient>y'
        )
        group = VGroup(text1, text2, text3, text4, text5).arrange(DOWN)
        self.add(group)

    #Ex5. FontExample

class FontEx(Scene):
    def construct(self):
        text1 = MarkupText(
            'all in sans <span font_family="serif">except this</span>', font="sans"
        )
        text2 = MarkupText(
            '<span font_family="serif">mixing</span> <span font_family="sans">fonts</span> <span font_family="monospace">is ugly</span>'
        )
        text3 = MarkupText("special char > or &gt;")
        text4 = MarkupText("special char &lt; and &amp;")
        group = VGroup(text1, text2, text3, text4).arrange(DOWN)
        self.add(group)

    #Ex6. Newline Example

class NewlineExample(Scene):
    def construct(self):
        text = MarkupText('foooo<span foreground="red">oo\nbaa</span>aar')
        self.add(text)

    #Ex7. No Ligatures Example

class NoLigaturesEx(Scene):
    def construct(self):
        text1 = MarkupText('fl<gradient from="RED" to="GREEN">oat</gradient>ing')
        text2 =MarkupText('fl<gradient from="RED" to="GREEN">oat</gradient>ing', disable_ligatures=True)
        group = VGroup(text1, text2).arrange(DOWN)
        self.add(group)

    #Ex8. Justify Text

class JustifyText(Scene):
    def construct(self):
        ipsum_text = (
            "Lorem ipsum dolor sit amet, consectetur adirtsng alit,"
            "skhf kjahf ajhfak kahjdf kahjdf. akhfka akjfa Fiuajaeiakla"
            "RThjbakfke THGT jew  wkqaiwk kehek kljsekr"
            "Tksf kjreg kerhiur khr, ieuirth qajkeh i irwriwrhs"
            "Yeljkr thskr kerut kwrtwitr rjturw kwrhtr."
        )
        justified_text = MarkupText(ipsum_text, justify=True).scale(0.4)
        not_justified_text = MarkupText(ipsum_text, justify=False).scale(0.4)
        just_title = Title("Justified")
        njust_title = Title("Not Justified")
        self.add(njust_title, not_justified_text)
        self.play(
            FadeOut(not_justified_text),
            FadeIn(justified_text),
            FadeOut(njust_title),
            FadeIn(just_title)
        )
        self.wait(1)

  
   #ii. Paragraph - Display a paragraph of text

   #iii. --------- Text ---------

       #Ex1. Example1 Text

class Example1Text(Scene): 
    def construct(self): 
        text = Text('Hello world').scale(3) 
        self.add(text)

       #Ex2. TextColorExample 

class TextColorExample(Scene):
    def construct(self): 
        text1 = Text('Hello world', color=BLUE).scale(3) 
        text2 = Text('Hello world', gradient=(BLUE, GREEN)).scale(3).next_to(text1, DOWN) 
        self.add(text1, text2)

       # Ex3. TextItalicAndBoldExample 

class TextItalicAndBoldExample(Scene): 
    def construct(self): 
        text1 = Text("Hello world", slant=ITALIC) 
        text2 = Text("Hello world", t2s={'world':ITALIC}) 
        text3 = Text("Hello world", weight=BOLD) 
        text4 = Text("Hello world", t2w={'world':BOLD}) 
        text5 = Text("Hello world", t2c={'o':YELLOW}, disable_ligatures=True) 
        text6 = Text( 
            "Visit us at docs.manim.community", 
            t2c={"docs.manim.community": YELLOW}, 
            disable_ligatures=True, 
        ) 
        text6.scale(1.3).shift(DOWN) 
        self.add(text1, text2, text3, text4, text5 , text6) 
        Group(*self.mobjects).arrange(DOWN, buff=.8).set(height=config.frame_height-LARGE_BUFF)

        
        #Ex4. TextMoreCustomization 

class TextMoreCustomization(Scene): 
    def construct(self): 
        text1 = Text( 
            'Google', 
            t2c={'[:1]': '#3174f0', '[1:2]': '#e53125', '[2:3]': '#fbb003', '[3:4]': '#3174f0', '[4:5]': '#269a43', '[5:]': '#e53125'}, 
            font_size=58
        ).scale(3) 
        self.add(text1) 
        

         #Ex5. MultipleFonts

class MultipleFonts(Scene): 
    def construct(self): 
        morning = Text("வணக்கம்", font="sans-serif") 
        japanese = Text( "日本へようこそ", t2c={"日本": BLUE} ) # works same as Text. 
        mess = Text("Multi-Language", weight=BOLD) 
        russ = Text("Здравствуйте मस नम म ", font="sans-serif") 
        hin = Text("नमस्ते", font="sans-serif") 
        arb = Text( "صباح الخير \n تشرفت بمقابلتك", font="sans-serif" ) # don't mix RTL and LTR languages nothing shows up then ;-) 
        chinese = Text("臂猿「黛比」帶著孩子", font="sans-serif") 
        self.add(morning, japanese, mess, russ, hin, arb, chinese) 
        for i,mobj in enumerate(self.mobjects): mobj.shift(DOWN*(i-3))

          
          #Ex6. PangoRender 

class PangoRender(Scene):
    def construct(self): 
        morning = Text("வணக்கம்", font="sans-serif") 
        self.play(Write(morning)) 
        self.wait(2)




    #11. ============= THREE_D - 3d mobjects =========

        #------  MODULES ------

        #i. ------POLYHEDRA - General polyhedral class and platonic solids----

  #classes

  #a. ConvexHull3D - A convex hull for a set of points
  
class ConvexHull3DEx(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        points = [
            [ 1.93192752, 0.44134585, -1.52407061],
            [-0.93302521, 1.23206983, 0.64117067],
            [-0.44350918, -1.61043677, 0.21723705],
            [-0.42640268, -1.05260843, 1.61266094],
            [-1.84449637, 0.91238739, -1.85172623],
            [1.72068132, -0.11880457, 0.51881751],
            [0.41904805, 0.44938012, -1.86440686],
            [0.83864666, 1.66653337, 1.88960123],
            [0.22240514, -0.80986286, 1.34249326],
            [-1.29585759, 1.01516189, 0.46187522],
            [1.7776499, -1.59550796, -1.70240747],
            [0.80065226, -0.12530398, 1.70063977],
            [1.28960948, -1.44158255, 1.39938582],
            [-0.93588943, 1.33617705, -0.24852643],
            [-1.54868271, 1.7444399, -0.46170734]
        ]
        hull = ConvexHull3D(
            *points,
            faces_config = {"stroke_opacity": 0},
            graph_config = {
                "vertex_type": Dot3D,
                "edge_config": {
                    "stroke_color": BLUE,
                    "stroke_width": 2,
                    "stroke_opacity": 0.05,
                }
            }
        )
        dots = VGroup(*[Dot3D(point) for point in points])
        self.add(hull)
        self.add(dots) 


  #b. Dodecahedron - one of the 5 platonic solids(has 12 faces, 30 edges and 20 vertices)

class DodecahedronScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        obj = Dodecahedron()
        self.add(obj)

  #c. Icosahedron - one of the 5 platonic solids (Has 20 faces, 30 edgesand 12 vertices)

class IcosahedronScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        obj = Icosahedron()
        self.add(obj)

  #d. Octahedron - one of the 5 platonic solids (Has 8 faces, 12 edges, and 6 vertices)

class OctahedronScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        obj = Octahedron()
        self.add(obj)  

  #e. Polyhedron - abstract polyhedra class (In this implementation, polyhedra are defined with a list of vertex coordinates in space, and a list of faces.)

class SquarePyramidScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta= 30 * DEGREES)
        vertex_coords = [
            [1, 1, 0],
            [1, -1, 0],
            [-1, -1, 0],
            [-1, 1, 0],
            [0, 0, 2]
        ]
        faces_list = [
            [0, 1, 4],
            [1, 2, 4],
            [2, 3, 4],
            [3, 0, 4],
            [0, 1, 2, 3]
        ]
        pyramid = Polyhedron(vertex_coords, faces_list)
        self.add(pyramid)

#PolyhedronSubmobjects Example

class PolyhedronSubmobjects(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta= 30 * DEGREES)
        octahedron = Octahedron(edge_length=3)
        octahedron.graph[0].set_color(RED)
        octahedron.faces[2].set_color(YELLOW)
        self.add(octahedron)

  #f. Tetrahedron - one of the 5 platonic solids (It has 4 faces, 6 edges and 4 vertices)

class TetrahedronScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        obj = Tetrahedron()
        self.add(obj)  


#ii. >>>>>>>>three_d_utils - Utility functions for 3 dimensional objects


     #iii. >>>>>>>>>>>> THREE_DIMENSIONS - 3D mobjects >>>>>>>>>>>>>

#classes

#a. Arrow3D - An arrow made out of a cylindrical line and a conical tip

class Arrow3DEx(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        arrow = Arrow3D(
            start=np.array([0, 0, 0]),
            end=np.array([2, 2, 2]),
            resolution=8
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(axes, arrow)


#b. Cone - A circular cone

class ConeEx(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        cone = Cone(direction=X_AXIS + Y_AXIS + 2 * Z_AXIS, resolution = 8)
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(axes, cone)  
      
#c. Cube - A 3d cube

class CubeEx(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        axes = ThreeDAxes()
        cube = Cube(side_length=3, fill_opacity=0.7, fill_color=BLUE)
        
        self.add(axes, cube)

#d Cylinder - A cylinder, defined by its height, radius and direction

class CylinderEx(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        cylinder = Cylinder(radius=2, height=3)
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(axes, cylinder) 

#e. Dot3D - A spherical dot

class Dot3DEx(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)

        axes = ThreeDAxes()
        dot_1 = Dot3D(point=axes.coords_to_point(0, 0, 1), color=RED)
        dot_2 = Dot3D(point=axes.coords_to_point(2, 0, 0), radius=0.1, color=BLUE)
        dot_3 = Dot3D(point=[0, 0, 0], radius=0.1, color=ORANGE)
        
        self.add(axes, dot_1, dot_2, dot_3)


#f. Line3D - A cylindrical line, for use in 3DScene

class Line3DEx(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        line = Line3D(start=np.array([0, 0, 0]), end=np.array([2, 2, 2]))
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(axes, line)

    #Parallel line Example2

class Line3DEx(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(PI / 3, -PI / 4)

        axes = ThreeDAxes((-5, 5), (-5, 5), (-5, 5), 10, 10 , 10) 
        line1 = Line3D(RIGHT * 2,UP + OUT, color=RED)
        line2 = Line3D.parallel_to(line1, color=YELLOW)
        self.add(axes, line1, line2)

    #Perpendicular line Example

class PerpLineEx(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(PI / 3, -PI / 4)

        axes = ThreeDAxes((-5, 5), (-5, 5), (-5, 5), 10, 10 , 10) 
        line1 = Line3D(RIGHT * 2,UP + OUT, color=RED)
        line2 = Line3D.perpendicular_to(line1, color=YELLOW)
        self.add(axes, line1, line2)


#g. Prism - A right rectangular prism(or rectangular cuboid)

class PrismEx(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=150 * DEGREES)

        prismSmall = Prism(dimensions=[1, 2, 3]).rotate(PI / 2)
        prismLarge = Prism(dimensions=[1.5, 3, 4.5]).move_to([2, 0, 0])
        self.add(prismSmall, prismLarge)


#h.SPhere - A 3d sphere

class SphereEx(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=PI / 6, theta=PI / 6)
        sphere1 = Sphere(
            center=(3, 0, 0),
            radius=1,
            resolution=(20, 20),
            u_range=[0.001, PI - 0.001],
            v_range=[0, TAU]
        )
        sphere1.set_color(RED)
        self.add(sphere1)

        sphere2 = Sphere(center=(-1, -3, 0), radius=2, resolution=(18, 18))
        sphere2.set_color(GREEN)
        self.add(sphere2)

        sphere3 = Sphere(center=(-1, 2, 0), radius=2, resolution=(16, 16))
        sphere1.set_color(BLUE)
        self.add(sphere3)

#i. Surface - Creates a parametric surface using a chekerboard pattern


class ParaSurface(ThreeDScene):
    def func(self, u, v):
        return np.array([np.cos(u) * np.cos(v), np.cos(u) * np.sin(v), u])
    
    def construct(self):
        axes = ThreeDAxes(x_range=[-4, 4], x_length=8)
        surface = Surface(
            lambda u, v: axes.c2p(*self.func(u, v)),
            u_range=[-PI, PI],
            v_range=[0, TAU],
            resolution=8
        )
        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)
        self.add(axes, surface)

    #Fill By Value Example ...2

class FIllByValue(ThreeDScene):
    def construct(self):
       resolution_fa= 8
       self.set_camera_orientation(phi=75 * DEGREES, theta= 160 * DEGREES)
       axes = ThreeDAxes(x_range=(0, 5, 1), y_range=(0, 5, 1), z_range=(-1, 1, 0.5))
       def param_surface(u, v):
           x = u
           y = v
           z = np.sin(x) * np.cos(y)
           return z
       surface_plane = Surface(
           lambda u, v: axes.c2p(u, v, param_surface(u, v)),
           resolution=(resolution_fa, resolution_fa),
           v_range=[0, 5],
           u_range=[0, 5],
       )
       surface_plane.set_style(fill_opacity=1)
       surface_plane.set_fill_by_value(axes=axes, colorscale=[(RED, 0.5), (YELLOW, 0), (GREEN, 0.5)], axis=2)
       self.add(axes, surface_plane)
        

#j. ThreeDVMobject


#k. Torus - A torus

class TorusEx(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        torus = Torus()
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 *DEGREES)
        self.add(axes, torus)


    #12. >>>>>>>>>>TYPES - Specialized mobject base classes <<<<<<<<<

#Modules

#a. Image_mobject - Mobjects representing raster images

        #------------- Classes ---------

#i. AbstractImageMobject - Automatically filters out black pixels

#ii. ImageMobject - Displays an image from a numpy array or a file

class ImageFromArray(Scene):
    def construct(self):
        image = ImageMobject(np.uint([[0, 100, 30, 200],
                                      [255, 0, 5, 33]])
                )
        image.height=7
        self.add(image)


        #Ex2. Image Interpolation Example

class ImageInterpolation(Scene):
    def construct(self):
        img = ImageMobject(np.uint8([[63, 0, 0, 0],
                                      [0, 127, 0, 0],
                                      [0, 0, 191, 0],
                                      [0, 0, 0, 255]
                                      ]))
        
        img.height=2
        img1 = img.copy()
        img2 = img.copy()
        img3 = img.copy()
        img4 = img.copy()
        img5 = img.copy()

        img1.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        img2.set_resampling_algorithm(RESAMPLING_ALGORITHMS["lanczos"])
        img3.set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
        img4.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
        img5.set_resampling_algorithm(RESAMPLING_ALGORITHMS["box"])

        img1.add(Text("nearest").scale(0.5).next_to(img1, UP))
        img2.add(Text("lanczos").scale(0.5).next_to(img2, UP))
        img3.add(Text("linear").scale(0.5).next_to(img3, UP))
        img4.add(Text("cubic").scale(0.5).next_to(img4, UP))
        img5.add(Text("box").scale(0.5).next_to(img5, UP))

        x = Group(img1, img2, img3, img4, img5)
        x.arrange()
        
        self.add(x)

#iii. ImageMobjectFromCamera


        #b. --------point_cloud mobject - Mobjects representing point clouds 
# classes

#i. Mobject1D

#ii. Mobject2D

#iii. PGroup - a group of several point mobjects

class PGroupEx(Scene):
    def construct(self):
        
        p1 = PointCloudDot(radius=1, density=20, color=BLUE)
        p1.move_to(4.5 * LEFT)

        p2 = PointCloudDot()
        p3 = PointCloudDot(radius=1.5, stroke_width=2.5, color=PINK)
        p3.move_to(4.5 * RIGHT)
        pList = PGroup(p1, p2, p3)

        self.add(pList)

#iv. PMobject - A disc made of a cloud of dots

class PMobjectEx(Scene):
    def construct(self):
        pG = PGroup() #this is just a collection of PMobjects

        #As the scale factor increases, the number of points removed increases

        for sf in range(1, 9 +1):
            p = PointCloudDot(density=20, radius=1).thin_out(sf)

            #PointcloudDot is a type of PMobject and can therefore be added as a PGroup

            pG.add(p)

            #This organizes all the shapes in a grid
        pG.arrange_in_grid()

        self.add(pG)


#v. Point - A mobject representing a point

class PointEx(Scene):
    def construct(self):
        colorList = [RED, GREEN, BLUE, YELLOW]
        for i in range(200):
            point = Point(location=[0.63 * np.random.randint(-4, 4), 0.37 * np.random.randint(-4, 4), 0], color=np.random.choice(colorList))
            self.add(point)

        for i in range(200):
            point = Point(location=[0.37 * np.random.randint(-4, 4), 0.63 * np.random.randint(-4, 4), 0], color=np.random.choice(colorList))
            self.add(point)
        self.add(point)

#vi. PointCLoudDot - A disc made of a cloud of dots

class PointCloudDotEx(Scene):
    def construct(self):
        cloud1 = PointCloudDot(color=RED)
        cloud2 = PointCloudDot(stroke_width=4, radius=1)
        cloud3 = PointCloudDot(density=15)

        group = Group(cloud1, cloud2, cloud3).arrange()
        self.add(group)

        #Point Cloud Example2

class PointCloudExample(Scene):
    def construct(self):
        plane = ComplexPlane()
        cloud = PointCloudDot(color=RED)
        self.add(
            plane, cloud
        )
        self.wait()
        self.play(
            cloud.animate.apply_complex_function(lambda z: np.exp(z))
        )

#c. <<<<<<<<<<<<< vectorized_mobject - Mobjects that use vector graphics >>>>>>>>>>

#classes

#i. CurvesAsSubmobjects - Convert a curve's elements to submobjects

class LineGradientEx(Scene):
    def construct(self):
        curve = ParametricFunction(lambda t: [t, np.sin(t), 0], t_range=[-PI, PI, 0.01], stroke_width=10)
        new_curve = CurvesAsSubmobjects(curve)
        new_curve.set_color_by_gradient(BLUE, RED)
        self.add(new_curve.shift(UP), curve)
    

#ii. DashedVMobjects - A VMobject composed of dashes instead of lines 

class DashedVMobjectEx(Scene):
    def construct(self):
        r = 0.5

        top_row = VGroup() #increasing num_dashes
        for dashes in range(1, 12):
            circ = DashedVMobject(Circle(radius=r, color=WHITE), num_dashes=dashes)
            top_row.add(circ)

        middle_row = VGroup()  # increasing dashed ratio
        for ratio in np.arange(1 / 11, 1, 1 / 11):
            circ = DashedVMobject(
                Circle(radius=r, color=WHITE), dashed_ratio=ratio
            )
            middle_row.add(circ)

        func1 = FunctionGraph(lambda t: t**5, [-1, 1], color=WHITE)
        func_even = DashedVMobject(func1, num_dashes=6, equal_lengths=True)
        func_stretched = DashedVMobject(func1, num_dashes=6, equal_lengths=False)
        bottom_row = VGroup(func_even, func_stretched)

        top_row.arrange(buff=0.3)
        middle_row.arrange()
        bottom_row.arrange(buff=1)
        everything = VGroup(top_row, middle_row, bottom_row).arrange(DOWN, buff=1)
        self.add(everything)


#iii. VDict - A VGroup-like class, also offering submobject access by key, like a python dict

class ShapesWithVDict(Scene):
    def construct(self):
        square = Square().set_color(RED)
        circle = Circle().set_color(YELLOW).next_to(square, UP)

        #create dict from list of tuples each having key-mobject pair
        pairs = [("s", square), ("c", circle)]
        my_dict = VDict(pairs, show_keys=True)

        #display it just like a VGroup
        self.play(Create(my_dict))
        self.wait()

        text = Tex("Some text").set_color(GREEN).next_to(square, DOWN)

        #add a key-value pair by wrapping it in a single-element list of tuple 
        #after attrs branch is merged, it will be easier like '.add(t=text)'

        my_dict.add([("t", text)]) 
        self.wait()

        rect = Rectangle().next_to(text, DOWN)
        #can also do a key assignment like a python dict
        my_dict["r"] = rect

        # access submobjects like a python dict
        my_dict["t"].set_color(PURPLE)
        self.play(my_dict["t"].animate.scale(3))
        self.wait()

        #also supports python dic styled reassignment
        my_dict["t"] = Tex("Somee other text").set_color(BLUE)
        self.wait()

        #remove submobjects by key

        my_dict.remove("t")
        self.wait()

        self.play(Uncreate(my_dict["s"]))
        self.wait()

        self.play(FadeOut(my_dict["c"]))
        self.wait()

        self.play(FadeOut(my_dict["r"], shift=DOWN))
        self.wait()

        #you can also make a VDict from an existing dict of mobjects

        plain_dict = {
            1: Integer(1).shift(DOWN),
            2: Integer(2).shift(2 * DOWN),
            3: Integer(3).shift(3 * DOWN),
        }

        vdict_from_plain_dict = VDict(plain_dict)
        vdict_from_plain_dict.shift(1.5 * (UP + LEFT))
        self.play(Create(vdict_from_plain_dict))

        # you can even use zip

        vdict_using_zip = VDict(zip(["s", "c", "r"], [Square(), Circle(), Rectangle()]))
        vdict_using_zip.shift(1.5 * RIGHT)
        self.play(Create(vdict_using_zip))
        self.wait()


#iv. VGroup - A group of vectrorized mobjects

class ArcShapeIris(Scene):
    def construct(self):
        colors = [DARK_BROWN, BLUE_E, BLUE_D, BLUE_A, TEAL_A, GREEN_B, YELLOW_E]
        radius = [1 + rad * 0.1 for rad in range(len(colors))]

        circles_group = VGroup()

        #zip (radius, color) makes the iterator [(radius[i], color[i]) for i in range (radius)]

        circles_group.add(*[Circle(radius=rad, stroke_width = 10, color = col)
                            for rad, col in zip(radius, colors)])
    
        self.add(circles_group)


    #Ex2. AddToVGroup Example

class AddToVGroup(Scene):
    def construct(self):
        circle_red = Circle(color=RED)
        circle_green = Circle(color=GREEN)
        circle_blue = Circle(color = BLUE)
        circle_red.shift(LEFT)
        circle_blue.shift(RIGHT)
        gr = VGroup(circle_red, circle_green)
        gr2 = VGroup(circle_blue) # Constructor uses add directly

        self.add(gr, gr2)
        self.wait()

        gr +=gr2 # add group to another
        self.play(
            gr.animate.shift(DOWN),
        )
        self.play( #Animate group without component
            (gr-circle_red).animate.shift(RIGHT)
        )


        #Ex3. Add Iterable To VGroup

class AddIterableToVGroup(Scene):
    def construct(self):
        v = VGroup(
            Square(),       #Singular VMobject instance
            [Circle(), Triangle()],  # List of VMobject instances
            Dot(),
            (Dot() for _ in range (2)),  # Iterable that generates VMobjects
        )
        v.arrange()
        self.add(v) 

#v. VMobject - A vectorized mobject

class PointFromProportion(Scene):
    def construct(self):
        line = Line(2*DL, 2*UR)
        self.add(line)
        colors = (RED, BLUE, YELLOW)
        proportions = (1/4, 1/2, 3/4)
        for color, proportion in zip(colors, proportions):
            self.add(Dot(color=color).move_to(
                line.point_from_proportion(proportion)
            ))

            #Ex2. Change in Direction

class ChangeInDirection(Scene):
    def construct(self):
        ccw = RegularPolygon(5)
        ccw.shift(LEFT)
        cw = RegularPolygon(5)
        cw.shift(RIGHT).reverse_direction()

        self.play(Create(ccw), Create(cw),
        run_time=4)


        #Ex3. RotateMethodExample

class RotateMethodEx(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        line = Line(start=ORIGIN, end= RIGHT)
        arrow1 = Arrow(start=ORIGIN, end=RIGHT, buff= 0, color=GOLD)
        group1 = VGroup(circle, line, arrow1)

        group2 = group1.copy()
        arrow2 = group2[2]
        arrow2.rotate(angle=PI / 4, about_point=arrow2.get_start())

        group3 = group1.copy()
        arrow3 = group3[2]
        arrow3.rotate(angle=120 * DEGREES, about_point=arrow3.get_start())

        self.add(VGroup(group1, group2, group3).arrange(RIGHT, buff=1))


        #Ex4. Mobject Scale Example

class MObjectScale(Scene):
    def construct(self):
        c1 = Circle(1, RED).set_x(-1)
        c2 = Circle(1, GREEN).set_x(1)

        vg = VGroup(c1, c2)
        vg.set_stroke(width=50)
        self.add(vg)

        self.play(
            c1.animate.scale(.25),
            c2.animate.scale(.25),
            scale_stroke = True
        )

        #Ex5. Cap Style Ex

class CapStyleEx(Scene):
    def construct(self):
        line = Line(LEFT, RIGHT, color=YELLOW, stroke_width=20)
        line.set_cap_style(CapStyleType.ROUND)
        self.add(line)

        #Ex6. Set Fill

class SetFill(Scene):
    def construct(self):
        square = Square().scale(2).set_fill(WHITE, 1)
        circle1 = Circle().set_fill(GREEN, 0.8)
        circle2 = Circle().set_fill(YELLOW)  #No fill opacity
        circle3 = Circle().set_fill(color= '#FF2135', opacity = 0.2)
        group = Group(circle1, circle2, circle3).arrange()
        self.add(square)
        self.add(group)

        #Ex7. Points as Corners Ex
    
class PointsAsCorners(Scene):
    def construct(self):
        corners = (
            #Create square
            UR, UL,
            DL, DR,
            UR,
            # create crosses
            DL, UL,
            DR
        )
        vmob = VMobject(stroke_color=RED)
        vmob.set_points_as_corners(corners).scale(2)
        self.add(vmob)

        #Ex8. SetSheen

class SetSheen(Scene):
    def construct(self):
        circle = Circle(fill_opacity=1).set_sheen(-0.3, DR)
        self.add(circle)


#vi. VectorizedPoint - 

    #Ex1. HeightExample

class HeightExample(Scene):
    def construct(self):
        decimal = DecimalNumber().to_edge(UP)
        rect = Rectangle(color=BLUE)
        rect_copy = rect.copy().set_stroke(GRAY, opacity=0.5)

        decimal.add_updater(lambda d: d.set_value(rect.height))

        self.add(rect_copy, rect, decimal)
        self.play(rect.animate.set(height=5))
        self.wait()

        #Ex2. Width Example

class WidthEx(Scene):
    def construct(self):
        decimal = DecimalNumber().to_edge(UP)
        rect = Rectangle(color=BLUE)
        rect_copy = rect.copy().set_stroke(GRAY, opacity=0.5)

        decimal.add_updater(lambda d: d.set_value(rect.width))

        self.add(rect_copy, rect, decimal)
        self.play(rect.animate.set(width=7))
        self.wait()


    #13. UTILS - Utilities for working with mobjects


    #14. VALUE_TRACKER - Simple mobjects that can be used for storing(and updating) a value

#Classes 

#a. ComplexValueTracker - Tracks a complex-valued parameter

class ComplexValueTracker(Scene):
    def construct(self):
        tracker = ComplexValueTracker(-2+1j)
        dot = Dot().add_updater(
            lambda x: x.move_to(tracker.points)
        )

        self.add(NumberPlane(), dot)

        self.play(tracker.animate.set_value(3+2j))
        self.play(tracker.animate.set_value(tracker.get_value() * 1j))
        self.play(tracker.animate.set_value(tracker.get_value() + 2j))
        self.play(tracker.animate.set_value(tracker.get_value() / (-2 + 3j)))

#b. ValueTracker - A mobject that can be used for traking (real-valued) parameters

#Ex1. ValueTrackerExample

class ValueTrackerEx(Scene):
    def construct(self):
        number_line = NumberLine(include_numbers=True)
        pointer = Vector(DOWN)
        label = MathTex("x").add_updater(lambda m: m.next_to(pointer, UP))

        tracker = ValueTracker(0)
        pointer.add_updater(
            lambda m: m.next_to(
                number_line.n2p(tracker.get_value()),
                UP
            )
        )
        self.add(number_line, pointer, label)
        tracker += 1.5
        self.wait(1)
        tracker -=4
        self.wait(0.5)
        self.play(tracker.animate.set_value(5))
        self.wait(0.5)
        self.play(tracker.animate.set_value(3))
        self.play(tracker.animate.increment_value(-2))
        self.wait(0.5)

        #Ex2. ValueTracker Example2

class ValueTracker(Scene):
    def construct(self):
        tracker = ValueTracker(0)
        label = Dot(radius=3).add_updater(lambda x : x.set_x(tracker.get_value()))
        self.add(label)
        self.add(tracker)
        tracker.add_updater(lambda mobject, dt: mobject.increment_value(dt))
        self.wait(2)

    #15. <<<<<<<<<<<<<VECTOR_FIELD - mobjects representing vector fields >>>>>>>>>

#Classes

#i. ArrowVectorField - A Vectorfield representedby a set of chn=ange vectors

#Ex1. Basic Usage

class BasicUsage(Scene):
    def construct(self):
        func = lambda  pos: ((pos[0] * UR + pos [1] * LEFT) - pos) / 3
        self.add(ArrowVectorField(func))

#Ex2. Sizing and Spacing

class SizingAndSpacing(Scene):
    def construct(self):
        func = lambda pos: np.sin(pos[0] / 2) * UR + np.cos(pos[1] / 2) * LEFT
        vf = ArrowVectorField(func, x_range=[-7, 7, 1])
        self.add(vf)
        self.wait()

        length_func = lambda x: x / 3
        vf2 = ArrowVectorField(func, x_range=[-7, 7, 1], length_func=length_func)
        self.play(vf.animate.become(vf2))
        self.wait()

#Ex3. Coloring

class Coloring(Scene):
    def construct(self):
        func = lambda pos: pos - LEFT * 5
        colors = [RED, YELLOW, BLUE, DARK_GRAY]
        min_radius = Circle(radius=2, color=colors[0]).shift(LEFT*5)
        max_radius = Circle(radius=10, color=colors[-1]).shift(LEFT*5)
        vf = ArrowVectorField(
            func, min_color_scheme_value=2, max_color_scheme_value=10, colors=colors
        )
        self.add(vf, min_radius, max_radius)


#ii. StreamLines - StreamLines represent the flow of a vector field using the trace of moving agents

 #Ex1. Basic Usage

class BasicUsage(Scene):
    def construct(self):
        func = lambda pos: ((pos[0]* UR + pos[1] * LEFT) - pos) / 3
        self.add(StreamLines(func))

 #Ex2. Spawning and Flowing area Example

class SpawningAndFlowingArea(Scene):
    def construct(self):
        func = lambda pos: np.sin(pos[0]) * UR + np.cos(pos[1]) * LEFT + pos / 5
        stream_lines = StreamLines(
            func, x_range=[-3, 3, 0.2], y_range=[-2, 2, 0.2], padding=1
        )
        spawning_area = Rectangle(width=6, height=4)
        flowing_area = Rectangle(width=8, height=6)
        labels = [Tex("Spawning Area"), Tex("Flowing Area").shift(DOWN * 2.5)]
        for lbl in labels:
            lbl.add_background_rectangle(opacity=0.6, buff= 0.05)

        self.add(stream_lines, spawning_area, flowing_area, *labels)

    #Ex3. StreamLine creation

class StreamLineCreation(Scene):
    def construct(self):
        func = lambda pos: (pos[0]* UR + pos[1] * LEFT) - pos
        stream_lines = StreamLines(
            func,
            color=YELLOW,
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            stroke_width=3,
            virtual_time=1,  # use shorter lines
            max_anchors_per_line=5, # better performance with fewer anchors
        )
        self.play(stream_lines.create())  #uses virtual time as run_time
        self.wait()

    #Ex4. EndAnimation

class EndAnimation(Scene):
    def construct(self):
        func = lambda pos: np.sin(pos[0] / 2) * UR + np.cos(pos[1] / 2) * LEFT
        stream_lines = StreamLines(
            func, stroke_width=3, max_anchors_per_line=5, virtual_time=1, color=BLUE
        )
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=False, flow_speed=1.5, time_width=0.5)
        self.wait(1)
        self.play(stream_lines.end_animation())

    #Ex5. Continuous Motion

class ContinuousMotion(Scene):
    def construct(self):
        func = lambda pos: np.sin(pos[0] / 2) * UR + np.cos(pos[1] / 2) * LEFT
        stream_lines = StreamLines(func, stroke_width=3, max_anchors_per_line=30)
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=False, flow_speed=1.5)
        self.wait(stream_lines.virtual_time / stream_lines.flow_speed)
        


#iii. >>>>>>>>>>   VECTORFIELD - A vector field   <<<<<<<<<<<<

       #Ex1. Nudging Example

class Nudging(Scene):
    def construct(self):
        func = lambda pos: np.sin(pos[1] / 2) * RIGHT + np.cos(pos[0] / 2) * UP
        vector_field = ArrowVectorField(
            func, x_range=[-7, 7, 1], y_range=[-4, 4, 1], length_func=lambda x: x / 2
        )
        self.add(vector_field)
        circle = Circle(radius=2).shift(LEFT)
        self.add(circle.copy().set_color(GRAY))
        dot = Dot().move_to(circle)

        vector_field.nudge(circle, -2, 60, True)
        vector_field.nudge(dot, -2, 60)

        circle.add_updater(vector_field.get_nudge_updater(pointwise=True))
        dot.add_updater(vector_field.get_nudge_updater())
        self.add(circle, dot)
        self.wait(6)

        #Ex2. ScaleVectorFieldFunction

class ScaleVectorFieldFunction(Scene):
    def construct(self):
        func = lambda pos: np.sin(pos[1]) * RIGHT + np.cos(pos[0]) * UP
        vector_field = ArrowVectorField(func)
        self.add(vector_field)
        self.wait()

        func = VectorField.scale_func(func, 0.5)
        self.play(vector_field.animate.become(ArrowVectorField(func)))
        self.wait()

        #  <<<<<<<<<<<<<<<<<<<<<< SCENES >>>>>>>>>>>>>>>>>

#1. moving_camera_scene - A scene whose camera can be moved around

  #Ex1. ChangingCameraWidthAndRestore

class ChangingCameraWidthAndRestore(MovingCameraScene):
    def construct(self):
        text = Text("Felix Kibz").set_color(BLUE)
        self.add(text)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=text.width * 1.2))
        self.wait(0.3)
        self.play(Restore(self.camera.frame))

    #Ex2. MovingCameraCenter

class MovingCameraCenter(MovingCameraScene):
    def construct(self):
        s = Square(color=RED, fill_opacity=0.5).move_to(2 * LEFT)
        t = Triangle(color = GREEN, fill_opacity=0.5).move_to(2 * RIGHT)
        self.wait(0.3)
        self.add(s, t)
        self.play(self.camera.frame.animate.move_to(s))
        self.wait(0.3)
        self.play(self.camera.frame.animate.move_to(t))

    #Ex3. MovingAndZoomingCamera

class MovingAndZoomingCamera(MovingCameraScene):
    def construct(self):
        s = Square(color=BLUE, fill_opacity=0.5).move_to(2 * LEFT)
        t = Triangle(color = YELLOW, fill_opacity=0.5).move_to(2 * RIGHT)
        self.add(s, t)
        self.play(self.camera.frame.animate.move_to(s).set(width=s.width*2))
        self.wait(0.3)
        self.play(self.camera.frame.animate.move_to(t).set(width=t.width*2))

        self.play(self.camera.frame.animate.move_to(ORIGIN).set(width=14))

    #Ex4. MovingCameraOnGraph

class MovingCameraOnGraph(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()

        ax = Axes(x_range=[-1, 10], y_range=[-1, 10])
        graph = ax.plot(lambda x: np.sin(x), color=WHITE, x_range=[0, 3 * PI])

        dot1 = Dot(ax.i2gp(graph.t_max, graph))
        dot2 = Dot(ax.i2gp(graph.t_min, graph))
        self.add(ax, graph, dot1, dot2)

        self.play(self.camera.frame.animate.scale(0.5).move_to(dot1))
        self.play(self.camera.frame.animate.move_to(dot2))
        self.play(Restore(self.camera.frame))
        self.wait()

    #Ex.5 SlidingMultipleScenes
    
class SlidingMultipleScenes(MovingCameraScene):
    def construct(self):
        def create_scene(number):
            frame = Rectangle(width=16, height=9)
            circ = Circle().shift(LEFT)
            text = Tex(f"This is Scene {str(number)}").next_to(circ, RIGHT)
            frame.add(circ, text)
            return frame
        group = VGroup(*(create_scene(i) for i in range(4))).arrange_in_grid(buff=1)
        self.add(group)
        self.camera.auto_zoom(group[0], animate=False)
        for scene in group:
            self.play(self.camera.auto_zoom(scene))
            self.wait()

        self.play(self.camera.auto_zoom(group, margin=2))


        # Classes

 #i. MovingCameraScene - This is a Scene, with special configurations and properties that make it suitable for cases where the camera must be mmoved around



         #2. <<<<<<<<<<  section - building block of segmented video API >>>>>>>>

     #classes

     #i. DefaultSectionType - The type of a section can be used for third party applications


     #ii. Section - A Scene can be segmented into multiple Sections


         #3. <<<<<<<<<<<< scene - Basic canvas for animations >>>>>>>>>>

    #classes

        #i. RerunSceneHandler - A class to handle rerunning a scene after the input file is modified

        #ii. Scene - A Scene is the canvas of your animation

        #Ex. SoundExample

class SoundExample(Scene):
    def construct(self):
        #Source of sound under Creative common 0 Licence, ....
        dot = Dot().set_color(GREEN)
        self.add_sound("click.wav")
        self.add(dot)
        self.wait()
        self.add_sound("click.wav")
        dot.set_color(BLUE)
        self.wait()
        self.add_sound("click.wav")
        dot.set_color(RED)
        self.wait()


            #iii. SceneInteractContinue - Object which, when encountered in Scene.interact(), triggers the end of the Scene interaction, continuing with the rest of the aniations, if any
            #iv. SceneInteractRerun - Object which, when encountered in Scene.interact(), triggers the rerun of the scene


        #4. scene_file_writer - The interface b2n scenes and ffmpeg


        #5. <<<<<<<<<<<<<  three_d_scene - A scene suitable for rendering 3-dimentional objects and animations >>>>>>>>>>>>

  #classes

            #i. SpecialThreeDScene - An extension of ThreeDScene with more settings
            #ii. ThreeDScene - This is a Scene, with special configs and properties that make it suitable for Three Dimensional Scenes

            #6. <<<<<<<<<< vector_space_scene - A scene suitable for vector spaces >>>>>>>>>>>>
    #Classes
        #i. LinearTransformationScene - Contains special methods that make it especially suitable for showing linear transformations

class LinearTransformationScene(LinearTransformationScene):
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates= True,
            leave_ghost_vectors= True,
            **kwargs
        )

    def construct(self):
        matrix = [[1, 1], [0, 1]]
        self.apply_matrix(matrix)
        self.wait()


        #ii. VectorScene - 


            #7. zoomed_scene - A scene supporting zooming in on a specific section

#Ex1. UseZoomedScene

class UseZoomedSceneEx(ZoomedScene):
    def construct(self):
        dot = Dot().set_color(GREEN)
        self.add(dot)
        self.wait()
        self.activate_zooming(animate=False)
        self.wait()
        self.play(dot.animate.shift(LEFT))

#Ex2. ChangingZooScale

class ChangingZooScale(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=1,
            zoomed_display_width=3,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
            },
            **kwargs
        )

    def construct(self):
        dot = Dot().set_color(GREEN)
        sq = Circle(fill_opacity=1, radius=0.2).next_to(dot, RIGHT)
        self.add(dot, sq)
        self.wait()
        self.activate_zooming(animate=False)
        self.wait(1)
        self.play(dot.animate.shift(LEFT * 0.3))

        self.play(self.zoomed_camera.frame.animate.scale(4))
        self.play(self.zoomed_camera.frame.animate.shift(0.5 * DOWN))
