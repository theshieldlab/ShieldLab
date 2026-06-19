"""
Cultural aesthetic: Maasai-inspired shield geometry

Usage:
    from shield_creatures import TeacherCreature, StudentCreature, CreatureScene
"""

from manim import *
import numpy as np
import random


# PALETTE

SHIELD_BLACK      = "#1a1a1a"
SHIELD_WHITE      = "#f5f0e8"
TEACHER_COLOR     = "#c0432a"   #warm terracotta/sienna red
STUDENT_BLUE      = "#2d5f8a"   #deep Maasai blue
STUDENT_GREEN     = "#4a7c45"   #savanna green
STUDENT_YELLOW    = "#c9982a"   #warm ochre/golden
MARKING_COLOR     = "#f5f0e8"   #off white for body markings



# SHIELD BODY SHAPE

def shield_body_path(height=2.6, width=1.3, stroke_width=4):
    """
    Creates a tall pointed-oval (lens / shield) shape
    Pointed at top and bottom like a Maasai shield
    """
    # A lens shape: two circular arcs meeting at top/bottom points
    # We build it as a custom VMobject using cubic bezier
    body = VMobject(stroke_width=stroke_width, stroke_color=SHIELD_BLACK)
    
    h = height / 2
    w = width / 2
    ctrl = w * 1.35  # control point spread for bulge

    # Top point → right bulge → bottom point → left bulge → close
    body.set_points_as_corners([
        [0,  h,  0],  # top point
    ])
    body.set_points([
        # top point
        np.array([0,   h,    0]),
        np.array([ctrl, h*0.4, 0]),
        np.array([w,    h*0.1, 0]),
        # right equator
        np.array([w,    0,    0]),
        np.array([w,   -h*0.1, 0]),
        np.array([ctrl,-h*0.4, 0]),
        # bottom point
        np.array([0,  -h,    0]),
        np.array([-ctrl,-h*0.4, 0]),
        np.array([-w,  -h*0.1, 0]),
        # left equator
        np.array([-w,   0,    0]),
        np.array([-w,   h*0.1, 0]),
        np.array([-ctrl, h*0.4, 0]),
        # back to top
        np.array([0,   h,    0]),
    ])
    return body


def make_shield_body(height=2.6, width=1.3, fill_color=TEACHER_COLOR, stroke_width=4):

    """Returns a filled shield body VMobject"""
    #ellipse as base and warp it with custom path for pointed ends
    #I will use a polygon approximation for reliability
    body = Polygon(
        *_shield_points(height, width),
        stroke_color=SHIELD_BLACK,
        stroke_width=stroke_width,
        fill_color=fill_color,
        fill_opacity=1.0,
    )
    return body


def _shield_points(height=2.6, width=1.3, n=40):
    """Generate polygon points approximating a pointed oval (lens/shield shape)"""
    h = height / 2
    w = width / 2
    points = []
    for i in range(n):
        t = i / n * TAU

        # parametric lens: squeeze horizontally, keep vertical range full
        # Use sin^(1/p) shaping to create pointed ends

        angle = t
        # vertical component: full sine sweep from -h to h
        
        y = -np.cos(angle) * h

        # horizontal: sinusoidal but tapered near poles
        # taper = sin(angle) gives zero at top/bottom naturally
        x = np.sin(angle) * w * (np.abs(np.sin(angle)) ** 0.3)
        points.append([x, y, 0])
    return points


# ─────────────────────────────────────────────
# MAASAI MARKINGS
# ─────────────────────────────────────────────
def make_body_markings(height=2.6, width=1.3):
    """
    Creates Maasai-inspired white markings on the shield body:
    - Central vertical black strip with white dots
    - Side chevron/arrow marks
    - A central eye-like almond shape
    """
    markings = VGroup()

    h = height / 2
    w = width / 2
    strip_w = w * 0.22

    # ── Central black strip ──
    strip = Polygon(
        [-strip_w,  h*0.62, 0],
        [ strip_w,  h*0.62, 0],
        [ strip_w, -h*0.62, 0],
        [-strip_w, -h*0.62, 0],
        fill_color=SHIELD_BLACK,
        fill_opacity=1.0,
        stroke_width=0,
    )
    markings.add(strip)

    # ── Central almond / eye shape on strip ──
    almond = Ellipse(
        width=strip_w * 2.8,
        height=h * 0.64,
        fill_color=SHIELD_BLACK,
        fill_opacity=1.0,
        stroke_color=SHIELD_BLACK,
        stroke_width=2,
    )
    markings.add(almond)

    # ── White dots inside the almond ──

    dot_r = strip_w * 0.38
    for dy in [-h*0.11, 0, h*0.11]:
        dot = Circle(
            radius=dot_r,
            fill_color=SHIELD_WHITE,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0, dy, 0])
        markings.add(dot)

    # ── Side chevron marks (left and right) ──
    for side in [-1, 1]:
        cx = side * w * 0.65 
        for cy in [h * -0.07, -h * 0.35]:
            chev = _make_chevron(
                center=[cx, cy, 0],
                size=w * 0.28,
                pointing=-side,  
            )
            markings.add(chev)

    return markings


def _make_chevron(center, size, pointing=1):
    """Small angular chevron / arrow mark for body decoration"""
    cx, cy, _ = center
    s = size
    # pointing: 1 = right-facing (>), -1 = left-facing (<)
    pts = [
        [cx + pointing * s * 0.2,  cy,        0],
        [cx - pointing * s * 1,  cy + s,    0],
        [cx - pointing * s * 1,  cy,        0],
        [cx - pointing * s * 0.6,  cy - s,    0],
    ]
    chev = Polygon(
        *pts,
        fill_color=MARKING_COLOR,
        fill_opacity=1.0,
        stroke_width=0,
    )
    return chev


# ─────────────────────────────────────────────
# EYES
# ─────────────────────────────────────────────
def make_eye_pair(body_height=2.6, body_width=1.3, eye_radius=0.21):
    """
    Returns (left_eye_group, right_eye_group)
    Each eye_group = VGroup(sclera, pupil)
    Eyes positioned in upper body
    """
    h = body_height / 2
    eye_y = h * 0.38
    eye_x = body_width * 0.28

    eyes = VGroup()
    for side, label in [(-1, "left"), (1, "right")]:
        sclera = Circle(
            radius=eye_radius,
            fill_color=SHIELD_WHITE,
            fill_opacity=1.0,
            stroke_color=SHIELD_BLACK,
            stroke_width=2.5,
        ).move_to([side * eye_x, eye_y, 0])

        pupil = Circle(
            radius=eye_radius * 0.52,
            fill_color=SHIELD_BLACK,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([side * eye_x + side * eye_radius * 0.2, eye_y - eye_radius * 0.1, 0])

        eye_group = VGroup(sclera, pupil)
        eye_group.sclera = sclera
        eye_group.pupil = pupil
        eyes.add(eye_group)

    eyes.left_eye = eyes[0]
    eyes.right_eye = eyes[1]
    return eyes


# ─────────────────────────────────────────────
# ARMS
# ─────────────────────────────────────────────
def make_arm(side=1, body_width=1.3, body_height=2.6, arm_length=0.85):
    """
    Two-segment arm with elbow: upper arm + forearm, each as a Line.
    The shoulder is the rotation pivot for all arm poses.
    The elbow connects upper arm to forearm.
    The hand circle sits at the forearm tip.

    Default pose: arm hangs at ~45 degrees outward/down, elbow bent slightly.

    Exposed attributes on the returned VGroup:
        .shoulder   — np.array, world attach point (pivot for rotations)
        .elbow_dot  — small Circle at the elbow joint
        .upper      — Line from shoulder to elbow
        .forearm    — Line from elbow to wrist
        .hand       — Circle at wrist/hand
    """
    seg = arm_length * 0.52          # each segment length
    attach_x = side * body_width * 0.46
    attach_y = 0.05                  # slightly above body midpoint

    # Default relaxed pose angles (in radians from positive-x axis)
    # Upper arm goes outward+down; forearm continues down with a slight bend
    upper_angle  = -PI / 2 + side * 0.45   # ~hanging with slight outward flare
    forearm_bend = -0.35 * side             # forearm bends further outward

    shoulder = np.array([attach_x, attach_y, 0])
    elbow    = shoulder + seg * np.array([np.cos(upper_angle), np.sin(upper_angle), 0])
    wrist    = elbow + seg * np.array([
        np.cos(upper_angle + forearm_bend),
        np.sin(upper_angle + forearm_bend),
        0
    ])

    upper = Line(
        shoulder, elbow,
        stroke_color=SHIELD_WHITE,
        stroke_width=5,
    )
    forearm = Line(
        elbow, wrist,
        stroke_color=SHIELD_WHITE,
        stroke_width=4,
    )
    elbow_dot = Circle(
        radius=0,
        fill_color=SHIELD_WHITE,
        fill_opacity=1.0,
        stroke_width=0,
    ).move_to(elbow)
    hand = Circle(
        radius=0.10,
        fill_color=SHIELD_WHITE,
        fill_opacity=1.0,
        stroke_width=0,
    ).move_to(wrist)

    arm_group = VGroup(upper, forearm, elbow_dot, hand)
    # Store named refs
    arm_group.upper      = upper
    arm_group.forearm    = forearm
    arm_group.elbow_dot  = elbow_dot
    arm_group.hand       = hand
    arm_group.shoulder   = shoulder   # fixed world position — pivot point
    return arm_group


def make_arm_pair(body_width=1.3, body_height=2.6):
    arms = VGroup(
        make_arm(-1, body_width, body_height),
        make_arm( 1, body_width, body_height),
    )
    arms.left  = arms[0]
    arms.right = arms[1]
    return arms

# ─────────────────────────────────────────────
# LEGS
# ─────────────────────────────────────────────
def make_leg(side=1, body_height=2.6, body_width=1.3, leg_length=0.75):
    """Single leg: thin line + L-shaped foot."""
    foot_x = side * body_width * 0.22
    attach_y = -body_height / 2 + 0.05
    ankle_y = attach_y - leg_length

    leg_line = Line(
        [foot_x * 0.5, attach_y, 0],
        [foot_x, ankle_y, 0],
        stroke_color=SHIELD_WHITE,
        stroke_width=4,
    )

    # L-shape: vertical ankle stub + horizontal toe bar
    ankle_stub = Line(
        [foot_x, ankle_y, 0],
        [foot_x, ankle_y - 0.15, 0],
        stroke_color=SHIELD_WHITE,
        stroke_width=4,
    )
    toe_bar = Line(
        [foot_x, ankle_y - 0.15, 0],
        [foot_x + side * 0.28, ankle_y - 0.15, 0],
        stroke_color=SHIELD_WHITE,
        stroke_width=4,
    )

    foot = VGroup(ankle_stub, toe_bar)
    leg_group = VGroup(leg_line, foot)
    leg_group.foot = foot
    return leg_group


def make_leg_pair(body_height=2.6, body_width=1.3):
    legs = VGroup(
        make_leg(-1, body_height, body_width),
        make_leg( 1, body_height, body_width),
    )
    legs.left  = legs[0]
    legs.right = legs[1]
    return legs


# ─────────────────────────────────────────────
# POINTING STICK (Teacher only)
# ─────────────────────────────────────────────
def make_pointing_stick(hand_pos=None):
    """
    Creates a pointing stick with a visible grip-node at the creature's hand
    The node visually separates arm from stick
    """
    if hand_pos is None:
        hand_pos = np.array([0.9, -0.5, 0])

    #grip node
    grip = Circle(
        radius=0.10,
        fill_color="#2a1a0a",
        fill_opacity=1.0,
        stroke_color=SHIELD_WHITE,
        stroke_width=1.5,
    ).move_to(hand_pos)

    # Stick extends from grip upward and to the right
    stick_end = hand_pos + np.array([1.4, 1.3, 0])
    stick = Line(
        hand_pos,
        stick_end,
        stroke_color="#8b6914",
        stroke_width=4.5,
    )

    stick_group = VGroup(stick, grip)
    stick_group.grip = grip
    stick_group.stick = stick
    stick_group.tip = stick_end
    return stick_group


# ─────────────────────────────────────────────
# BASE SHIELD CREATURE
# ─────────────────────────────────────────────
class ShieldCreature(VGroup):
    """
    Base class for all Shield Creatures
    
    VGroup hierarchy:
        self → body_group, markings, eyes, arms, legs
    
    Exposed attributes:
        self.body       — the shield shape
        self.markings   — Maasai decoration VGroup
        self.eyes       — VGroup with .left_eye and .right_eye
        self.pupils     — convenience list [left_pupil, right_pupil]
        self.arms       — VGroup with .left and .right
        self.legs       — VGroup with .left and .right
        self.fill_color — creature color
    """

    CONFIG = {
        "body_height":   2.6,
        "body_width":    1.3,
        "fill_color":    TEACHER_COLOR,
        "stroke_width":  4,
        "eye_radius":    0.21,
    }

    def __init__(self, fill_color=TEACHER_COLOR, height=2.6, width=1.3, eye_radius=0.21, **kwargs):
        super().__init__(**kwargs)
        self.fill_color   = fill_color
        self.body_height  = height
        self.body_width   = width
        self.eye_radius   = eye_radius

        self._build()
        self._mood = "neutral"
        self._idle_phase = random.uniform(0, TAU)

    def _build(self):

        """Assemble all creature parts"""

        # Body
        self.body = make_shield_body(
            height=self.body_height,
            width=self.body_width,
            fill_color=self.fill_color,
            stroke_width=4,
        )

        # Maasai markings
        self.markings = make_body_markings(self.body_height, self.body_width)

        # Eyes
        self.eyes = make_eye_pair(self.body_height, self.body_width, self.eye_radius)
        self.pupils = [
            self.eyes.left_eye.pupil,
            self.eyes.right_eye.pupil,
        ]

        # Arms
        self.arms = make_arm_pair(self.body_width, self.body_height)

        # Legs
        self.legs = make_leg_pair(self.body_height, self.body_width)

        # Compose
        self.add(self.legs, self.body, self.markings, self.arms, self.eyes)

    # ── Eye / Look Methods ───────────────────

    def look(self, direction: np.ndarray):
        """Move pupils in the given direction (normalized)"""
        direction = normalize(direction)
        max_offset = self.eye_radius * 0.45
        offset = direction * max_offset

        anims = []
        for i, eye in enumerate([self.eyes.left_eye, self.eyes.right_eye]):
            target = eye.sclera.get_center() + offset
            anims.append(eye.pupil.animate.move_to(target))
        return AnimationGroup(*anims, lag_ratio=0)

    def look_at(self, target_mobject):
        """Look at another mobject (creature, equation...)"""
        target_pos = target_mobject.get_center()
        my_pos = self.get_center()
        direction = target_pos - my_pos
        return self.look(direction)

    def look_at_point(self, point: np.ndarray):
        """Look toward a 3D point"""
        direction = point - self.get_center()
        return self.look(direction)

    def look_right(self):
        return self.look(RIGHT)

    def look_left(self):
        return self.look(LEFT)

    def look_up(self):
        return self.look(UP)

    def look_down(self):
        return self.look(DOWN)

    def look_forward(self):
        """Reset pupils to center"""
        anims = []
        for eye in [self.eyes.left_eye, self.eyes.right_eye]:
            anims.append(eye.pupil.animate.move_to(eye.sclera.get_center()))
        return AnimationGroup(*anims, lag_ratio=0)

    def blink(self):
        """
        Quick blink: squish each eye VGroup to a thin line then restore
        Strategy: save_state ONLY for the blink open phase (the target is
        the pre-squish state captured right now), then animate close → open
        Two-step Succession ensures eyes always reopen to exactly their
        current natural size regardless of prior transforms
        """
        eyes = [self.eyes.left_eye, self.eyes.right_eye]
        # Capture open targets BEFORE any squish
        for eye in eyes:
            eye.save_state()

        close_anims = [
            ApplyMethod(eye.scale, np.array([1, 0.05, 1])).set_rate_func(rush_into)
            for eye in eyes
        ]
        open_anims = [
            Restore(eye).set_rate_func(rush_from)
            for eye in eyes
        ]
        return Succession(
            AnimationGroup(*close_anims, run_time=0.10),
            AnimationGroup(*open_anims,  run_time=0.14),
        )

    def cross_eyes(self):
        """Cross pupils toward nose"""
        nose_x = self.get_center()[0]
        anims = []
        for eye in [self.eyes.left_eye, self.eyes.right_eye]:
            cx = eye.sclera.get_center()
            # Move each pupil inward
            target = np.array([nose_x, cx[1], cx[2]])
            anims.append(eye.pupil.animate.move_to(target))
        return AnimationGroup(*anims)

    def confused_eyes(self):
        """One eye up, one eye down"""
        le = self.eyes.left_eye
        re = self.eyes.right_eye
        offset = self.eye_radius * 0.4
        return AnimationGroup(
            le.pupil.animate.move_to(le.sclera.get_center() + UP * offset),
            re.pupil.animate.move_to(re.sclera.get_center() + DOWN * offset),
        )

    def thinking_eyes(self):
        """Both pupils look up-right (thinking)"""
        return self.look(UP * 0.7 + RIGHT * 0.7)

    # ── Emotional States ─────────────────────

    def be_happy(self):
        """Slightly upright, pupils looking slightly up"""
        anims = [
            self.animate.rotate(0),  # ensure upright
            *[eye.pupil.animate.move_to(
                eye.sclera.get_center() + UP * self.eye_radius * 0.2
            ) for eye in [self.eyes.left_eye, self.eyes.right_eye]],
        ]
        self._mood = "happy"
        return AnimationGroup(*anims)

    def be_confused(self):
        """Slight tilt + crossed/uneven eyes"""
        self._mood = "confused"
        return AnimationGroup(
            self.animate.rotate(0.15),
            self.confused_eyes(),
        )

    def be_thinking(self):
        """Slight rotation + pupils up-right"""
        self._mood = "thinking"
        return AnimationGroup(
            self.animate.rotate(-0.08),
            self.thinking_eyes(),
        )

    def be_excited(self):
        """Upright + pupils looking up"""
        self._mood = "excited"
        return AnimationGroup(
            self.animate.rotate(0),
            self.look(UP * 0.5 + RIGHT * 0.3),
        )

    def be_tired(self):
        """Slumped rotate + drooping pupils"""
        self._mood = "tired"
        return AnimationGroup(
            self.animate.rotate(0.25),
            self.look(DOWN * 0.5),
        )

    def be_suspicious(self):
        """Side-eye"""
        self._mood = "suspicious"
        return AnimationGroup(
            self.animate.rotate(0.05),
            self.look(RIGHT * 0.9),
        )

    def be_attentive(self):
        """Upright, pupils looking slightly right (at board)"""
        self._mood = "attentive"
        return AnimationGroup(
            self.animate.rotate(0),
            self.look(RIGHT * 0.6 + UP * 0.1),
        )

     # ── Arm Poses ────────────────────────────
    # All rotations pivot at the LIVE shoulder point (arm.upper.get_start()),
    # which is always accurate regardless of prior moves/rotations — unlike
    # a cached local offset combined with get_center().
 
    def _rotate_arm(self, arm, angle):
        """Rotate entire arm about its shoulder point."""
        pivot = arm.upper.get_start()
        return arm.animate.rotate(angle, about_point=pivot)
 
    def arm_raise(self, side="right"):
        """Raise one arm straight up — pivot at shoulder."""
        arm = self.arms.right if side == "right" else self.arms.left
        pivot = arm.upper.get_start()
        return arm.animate.rotate(PI * 0.72, about_point=pivot)
 
    def arm_point_right(self):
        pivot = self.arms.right.upper.get_start()
        return self.arms.right.animate.rotate(-PI / 5, about_point=pivot)
 
    def arm_wave(self):
        """Wiggle right arm — rotates about shoulder."""
        arm = self.arms.right
        pivot = arm.upper.get_start()
        return Wiggle(arm, scale_value=1.0, rotation_angle=0.3,
                      n_wiggles=4, rotate_about_point=pivot,
                      scale_about_point=pivot)
 
    def shrug(self):
        """Both arms rotate upward/outward from shoulders."""
        lp = self.arms.left.upper.get_start()
        rp = self.arms.right.upper.get_start()
        return AnimationGroup(
            self.arms.left.animate.rotate( PI * 0.18, about_point=lp),
            self.arms.right.animate.rotate(-PI * 0.18, about_point=rp),
        )
 
    def thinking_pose(self):
        """Right arm rotates up so forearm is near chin area."""
        pivot = self.arms.right.upper.get_start()
        return self.arms.right.animate.rotate(PI * 0.55, about_point=pivot)
 
    def relax_arms(self):
        """Return arms to saved default pose."""
        return AnimationGroup(
            Restore(self.arms.left),
            Restore(self.arms.right),
        )
 
    # ── Idle Animation ───────────────────────
 
    def idle_updater(self, dt):
        """
        Call this in scene with:
            creature.add_updater(creature.idle_updater)
        Provides subtle breathing + micro-bob.
        """
        self._idle_phase += dt * 1.2
        offset = np.sin(self._idle_phase) * 0.012
        self.body.set_height(self.body_height + offset * 0.3, stretch=True)
 
    def get_blink_animation(self, run_time=0.22):
        return self.blink()
 
    # ── Save state for restoration ────────────
    def save_pose(self):
        self.arms.left.save_state()
        self.arms.right.save_state()
 
    # ── Color ────────────────────────────────
    def set_color(self, color):
        self.body.set_fill(color)
        self.fill_color = color
        return self
 

# ─────────────────────────────────────────────
# TEACHER CREATURE
# ─────────────────────────────────────────────
class TeacherCreature(ShieldCreature):
    """
    Teacher: slightly taller, warm terracotta color, carries a pointing stick.
    The stick has a visible grip-node to visually separate it from the arm.
    """
 
    def __init__(self, fill_color=TEACHER_COLOR, height=2.7, width=1.38, **kwargs):
        super().__init__(fill_color=fill_color, height=height, width=width, **kwargs)
        self._add_stick()
        self.save_pose()
 
    def _add_stick(self):
        """Add the pointing stick with grip node."""
        hand_pos = self.arms.right.hand.get_center()
        self.stick = make_pointing_stick(hand_pos)
        # Place stick behind arms in draw order
        self.add(self.stick)
 
    def point_to(self, target):
        """
        Animate stick tip toward a target mobject or point.
        """
        if isinstance(target, np.ndarray):
            target_pos = target
        else:
            target_pos = target.get_center()
 
        stick_base = self.stick.grip.get_center()
        direction = target_pos - stick_base
        angle = np.arctan2(direction[1], direction[0])
        new_tip = stick_base + np.array([np.cos(angle), np.sin(angle), 0]) * 1.6
 
        new_line = Line(stick_base, new_tip,
                        stroke_color="#8b6914", stroke_width=4.5)
        return AnimationGroup(
            Transform(self.stick.stick, new_line),
            self.look_at_point(target_pos),
        )
 
    def lecture_pose(self):
        """Standard upright lecture stance."""
        return AnimationGroup(
            self.animate.rotate(0),
            self.look(RIGHT * 0.4 + UP * 0.05),
        )
 
    def explain(self):
        """Slight lean forward + look at equation area."""
        return AnimationGroup(
            self.animate.rotate(-0.05),
            self.look(RIGHT * 0.5 + UP * 0.2),
        )
 
    def look_at_student(self, student):
        return self.look_at(student)
 
    def pace(self, scene, distance=1.0, run_time=2.0):
        """Pace left and right once."""
        scene.play(self.animate.shift(LEFT * distance), run_time=run_time / 2)
        scene.play(self.animate.shift(RIGHT * distance), run_time=run_time / 2)
 
 
# ─────────────────────────────────────────────
# STUDENT CREATURE
# ─────────────────────────────────────────────
class StudentCreature(ShieldCreature):
    """
    Student: slightly shorter, one of three colors (blue/green/yellow).
    personality: "curious" | "calm" | "energetic"
    """
 
    PERSONALITIES = {
        "curious":   STUDENT_BLUE,
        "calm":      STUDENT_GREEN,
        "energetic": STUDENT_YELLOW,
    }
 
    def __init__(self, personality="curious", height=1.7, width=1.1, **kwargs):
        color = self.PERSONALITIES.get(personality, STUDENT_BLUE)
        super().__init__(fill_color=color, height=height, width=width, **kwargs)
        self.personality = personality
        self.save_pose()
 
    def attentive(self):
        """Look toward teacher/board."""
        return self.be_attentive()
 
    def raise_hand(self):
        """Raise right arm straight up, pivoting at the shoulder."""
        pivot = self.arms.right.upper.get_start()
        return AnimationGroup(
            self.arms.right.animate.rotate(PI * 0.75, about_point=pivot),
            self.look(UP * 0.5 + RIGHT * 0.15),
        )
 
    def lower_hand(self):
        """Lower previously raised hand back to resting pose."""
        return Restore(self.arms.right)
 
    def glance_at(self, other_student):
        """Quick look at another student."""
        return self.look_at(other_student)
 
    def look_at_equation(self, equation):
        return self.look_at(equation)
 
    def nod(self, scene, n_nods=2, run_time=0.6):
        """Bob up and down to indicate nodding."""
        for _ in range(n_nods):
            scene.play(self.animate.shift(UP * 0.08), run_time=run_time / (n_nods * 2))
            scene.play(self.animate.shift(DOWN * 0.08), run_time=run_time / (n_nods * 2))
 
    def tiny_hop(self, scene):
        """Excitement hop."""
        scene.play(self.animate.shift(UP * 0.25), run_time=0.15)
        scene.play(self.animate.shift(DOWN * 0.25), run_time=0.15)
 
    def personality_idle(self):
        """Default mood based on personality."""
        if self.personality == "curious":
            return self.be_attentive()
        elif self.personality == "calm":
            return self.look(RIGHT * 0.3)
        elif self.personality == "energetic":
            return self.be_excited()
 
 

# ─────────────────────────────────────────────
# CLASSROOM LAYOUT HELPER
# ─────────────────────────────────────────────
def create_classroom():
    """
    Returns (teacher, students) pre-positioned for a classroom scene
    teacher: TeacherCreature on the left
    students: StudentCreature [Akinyi, Brian, Kamau]
    """
    teacher = TeacherCreature().shift(LEFT * 4.5 + DOWN * 0.3)

    students = [
        StudentCreature("Akinyi").shift(RIGHT * 1.2 + DOWN * 0.8), #curious and thoughtful
        StudentCreature("Brian").shift(RIGHT * 3.0 + DOWN * 0.8),  # Quiet engineering kid
        StudentCreature("Kamau").shift(RIGHT * 4.8 + DOWN * 0.8),  #class clown/ GoonZ
    ]

    return teacher, students


# ─────────────────────────────────────────────
# REUSABLE SCENE FUNCTIONS
# ─────────────────────────────────────────────
def all_look_at_equation(scene, teacher, students, equation, run_time=0.8):
    """Everyone looks at the equation"""
    anims = [teacher.look_at(equation)]
    anims += [s.look_at(equation) for s in students]
    scene.play(*anims, run_time=run_time)


def all_look_at_teacher(scene, teacher, students, run_time=0.8):
    """Students look at teacher, teacher looks at students"""
    anims = [teacher.look(RIGHT * 0.3)]
    anims += [s.look_at(teacher) for s in students]
    scene.play(*anims, run_time=run_time)


def students_confused(scene, students, run_time=0.8):
    """All students enter confused state"""
    scene.play(*[s.be_confused() for s in students], run_time=run_time)


def students_react(scene, teacher, students, equation):
    """
    Standard sequence: teacher explains → students look → students react
    """
    scene.play(teacher.explain())
    all_look_at_equation(scene, teacher, students, equation)
    scene.wait(0.5)


def teacher_teaches(scene, teacher, equation):
    """Teacher looks at equation, points to it, explains"""
    scene.play(teacher.look_at(equation))
    scene.play(teacher.point_to(equation))
    scene.wait(0.5)
    scene.play(teacher.explain())


def student_raises_hand(scene, student, run_time=0.6):
    """Student raises hand animation"""
    scene.play(student.raise_hand(), run_time=run_time)


def teacher_points_to(scene, teacher, target, run_time=0.8):
    """Teacher points stick to a target"""
    scene.play(teacher.point_to(target), run_time=run_time)


def blink_staggered(scene, creatures, run_time=0.25):
    """
    Make creatures blink with staggered timing (async feel).
    """
    anims = []
    for i, c in enumerate(creatures):
        anims.append(AnimationGroup(c.blink(), lag_ratio=0))
    scene.play(LaggedStart(*anims, lag_ratio=0.3, run_time=run_time * 2))


def classroom_idle_blinks(scene, teacher, students, n=3):
    """
    Staggered random blinks across the class
    Each blink is separated by a random wait of 10-15 seconds
    Creatures never blink at the same time
    n = number of individual blink events
    """
    all_creatures = [teacher] + students
    last_blinker = None
    for _ in range(n):
        # Wait 10-15 seconds before next blink

        scene.wait(random.uniform(10.0, 15.0))
        # Pick a random creature, avoid repeating the same one twice in a row

        choices = [c for c in all_creatures if c is not last_blinker]
        blinker = random.choice(choices)
        last_blinker = blinker
        scene.play(blinker.blink(), run_time=0.25)


# ─────────────────────────────────────────────
# BASE SCENE CLASS
# ─────────────────────────────────────────────
class CreatureScene(Scene):
    """
    Convenience base class for Shield Creature STEM scenes
    Sets dark background and provides helpers
    """

    def setup(self):
        self.camera.background_color = "#111111"
        config.background_color = "#111111"
        config.frame_width = 14.22   # 16:9 at default height
        config.frame_height = 8.0

    def add_creatures(self):
        """Override in subclass to place creatures"""
        pass

    def play_blink(self, creature):
        self.play(creature.blink(), run_time=0.22)

    def play_look_at(self, creature, target):
        self.play(creature.look_at(target))

    def setup_classroom(self):
        teacher, students = create_classroom()
        self.teacher = teacher
        self.students = students
        self.all_creatures = [teacher] + students
        return teacher, students