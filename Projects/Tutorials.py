from manim import *

from scipy.integrate import odeint
from scipy.integrate import solve_ivp
import networkx as nx                


            #1. Vectors Tutorial

class Vectors(VectorScene):
    def construct(self):
        plane = self.add_plane(animate=True).add_coordinates()
        vector = self.add_vector([-3, -2], color=YELLOW)

        basis = self.get_basis_vectors(i_hat_color=BLUE, j_hat_color=RED)
        self.add(basis)
        self.vector_to_coords(vector=vector)

        vector2 = self.add_vector([2,2])
        self.write_vector_coordinates(vector=vector2)


        #2. Faces and solids Tutorial

class Cuboid(ThreeDScene):
    def construct(self):
        l= 2
        w=4
        h=1

        rec_prism = Prism(dimensions=[l, w, h]).to_edge(LEFT, buff=1)

        kwargs = {"stroke_color": BLUE_D, "fill_color": BLUE_B, "fill_opacity": 0.6}

        bottom = Rectangle(width=w, height=l, **kwargs)
        s1 = Rectangle(height=h, width=w, **kwargs).next_to(bottom, UP, buff=0)
        s2 = Rectangle(height=h, width=w, **kwargs).next_to(bottom, DOWN, buff=0)
        l1 = Rectangle(height=l, width=h, **kwargs).next_to(bottom, LEFT, buff=0)
        l2 = Rectangle(height=l, width=h, **kwargs).next_to(bottom, RIGHT, buff=0)
        top = Rectangle(width=w, height=l, **kwargs).next_to(s1, UP, buff=0)

        net = VGroup(top, bottom, s1, s2, l1, l2).rotate(-PI / 2).to_edge(RIGHT, buff=1)

        arrow = Line(
            start=rec_prism.get_right(), end=net.get_left(), buff=0.2
            ).add_tip()
        
        self.begin_ambient_camera_rotation()
        self.set_camera_orientation(phi=45 * DEGREES, theta=-45 * DEGREES)
        self.play(Create(rec_prism))
        self.play(
            LaggedStart(Create(arrow), Transform(rec_prism.copy(), net)),
            run_time = 1,
            lag_ratio = 0.5,
        )

        self.wait()
        self.play(FadeOut(Group(*self.mobjects)))
        self.stop_ambient_camera_rotation()




