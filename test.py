from manim import *
from manim import color
import numpy as np

# Helper to get Manim color from string
def get_manim_color(color_name_str):
    try:
        return globals()[color_name_str.upper()]
    except KeyError:
        try:
            return Color(color_name_str)
        except Exception:
            return WHITE  # fallback

class MaxHeight(Scene):
    def construct(self):
        # Read scene dimensions for positioning and clamping
        frame_width = self.camera.frame_width
        frame_height = self.camera.frame_height
        
        # Global settings from the problem description (normally from JSON input)
        gs = {
            "ball_color": "RED",
            "initial_velocity": "20 m/s",
            "acceleration": "-9.8 m/s^2",
            "final_velocity": "0 m/s",
            "max_height": "20.41 m"
        }

        # Parse global settings
        BALL_COLOR = get_manim_color(gs["ball_color"])
        ARROW_COLOR = WHITE # Default arrow color as it's not specified in JSON
        u_val_str = gs["initial_velocity"].split(" ")[0] # "20"
        u_val = float(u_val_str) # 20.0
        a_val_str = gs["acceleration"].split(" ")[0] # "-9.8"
        a_val = float(a_val_str) # -9.8
        s_max_val_str = gs["max_height"].split(" ")[0] # "20.41" (string for display)

        # --- Define Mobjects (created once and reused/modified) ---

        # Ground line
        ground_y_level = -frame_height / 2 + 0.5 # Position ground slightly up from bottom edge
        ground = Line(
            start=np.array([-frame_width / 2, ground_y_level, 0]),
            end=np.array([frame_width / 2, ground_y_level, 0]),
            color=BLUE_D, stroke_width=6
        )

        # Person (simplified as a Rectangle)
        person_height_val = 1.5
        person_width_val = 0.6
        person = Rectangle(
            width=person_width_val, height=person_height_val, color=GREEN_C, fill_opacity=0.8
        ).move_to(np.array([-frame_width / 3, ground_y_level + person_height_val / 2, 0]))
        # Note: For an SVG asset: person = SVGMobject("stick_figure.svg").scale(desired_scale).move_to(desired_pos)

        # Ball
        ball_radius_val = 0.15
        ball_initial_pos_np = person.get_top() + UP * (ball_radius_val + 0.1) # Ball starts above person
        ball = Dot(point=ball_initial_pos_np, color=BALL_COLOR, radius=ball_radius_val)

        # Initial velocity arrow (u_arrow)
        initial_screen_arrow_len = 1.5 # Visual length on screen for the arrow shaft
        u_arrow = Arrow(
            start=ball.get_bottom(),
            end=ball.get_bottom() + UP * initial_screen_arrow_len,
            buff=0, color=ARROW_COLOR, stroke_width=5, max_tip_length_to_length_ratio=0.25
        )
        u_label = MathTex(f"u = {gs['initial_velocity']}", font_size=30).next_to(u_arrow, RIGHT, buff=0.15)

        # Gravity arrow (g_arrow) - defined here, animated in Scene 2
        g_arrow_screen_len = 1.2 # Visual length on screen
        g_arrow = Arrow( # Initial dummy position, will be updated
            start=ORIGIN, end=DOWN * g_arrow_screen_len,
            buff=0.1, color=RED_C, stroke_width=5, max_tip_length_to_length_ratio=0.25
        )
        g_label = MathTex(f"a = {gs['acceleration']}", font_size=30) # Positioned by updater

        # --- Scene 1: Introduction ---
        scene1_title = Text("Scene 1: Introduction", font_size=28).to_edge(UP, buff=0.3)
        scene1_narration = Text("A ball is thrown straight up with 20 m/s.", font_size=22).next_to(scene1_title, DOWN, buff=0.25)

        self.add(ground, person, ball, u_arrow, u_label) # Add physical objects
        self.play(Write(scene1_title), Write(scene1_narration)) # Animate text
        self.wait(2.5)
        self.play(FadeOut(scene1_title), FadeOut(scene1_narration)) # Clear text for next scene

        # --- Scene 2: Ball Motion ---
        scene2_title = Text("Scene 2: Ball Motion", font_size=28).to_edge(UP, buff=0.3)
        scene2_narration = Text("The ball slows down as it rises, due to gravity acting downward.", font_size=22).next_to(scene2_title, DOWN, buff=0.25)
        self.play(Write(scene2_title), Write(scene2_narration))

        # Setup gravity arrow and its label with updaters
        g_arrow.add_updater(lambda m: m.become(Arrow( # Use .become for robust updates
            start=ball.get_center() + RIGHT * (ball_radius_val + 0.2), # Position to the right of ball
            end=ball.get_center() + RIGHT * (ball_radius_val + 0.2) + DOWN * g_arrow_screen_len,
            buff=0.1, color=RED_C, stroke_width=5, max_tip_length_to_length_ratio=0.25
        )))
        g_label.add_updater(lambda m: m.next_to(g_arrow, RIGHT, buff=0.15))

        self.play(Create(g_arrow), Write(g_label)) # Animate creation of gravity indicators
        self.wait(0.5)

        # Ball motion animation using ValueTracker for synchronization
        ball_initial_y_for_anim = ball.get_y()
        # Calculate peak Y position on screen, ensuring it's within frame bounds
        ball_peak_y_on_screen = frame_height / 2 - ball_radius_val - 0.3
        if ball_peak_y_on_screen <= ball_initial_y_for_anim: # Defensive check
            ball_peak_y_on_screen = ball_initial_y_for_anim + 0.1 # Ensure some upward motion if already high

        u_label.add_updater(lambda m: m.next_to(u_arrow, RIGHT, buff=0.15)) # u_label follows u_arrow

        animation_progress = ValueTracker(0) # Controls animation from 0 (start) to 1 (peak)

        # Store u_arrow's initial length for interpolation
        u_arrow_initial_length = u_arrow.get_length()

        # Updater for ball's vertical motion
        ball.add_updater(lambda mob: mob.set_y(
            interpolate(ball_initial_y_for_anim, ball_peak_y_on_screen, animation_progress.get_value())
        ))
        # Updater for u_arrow: move with ball and shrink
        u_arrow.add_updater(lambda mob: mob.become(Arrow(
            start=ball.get_bottom(), # Arrow base stays at ball's bottom
            end=ball.get_bottom() + UP * interpolate(u_arrow_initial_length, 0.01, animation_progress.get_value()), # Length shrinks
            buff=0, color=ARROW_COLOR, stroke_width=5, max_tip_length_to_length_ratio=0.25
        )))

        animation_duration = 2.5 # Seconds for ball to reach peak
        self.play(animation_progress.animate.set_value(1), run_time=animation_duration)

        # Clear all updaters after animation
        ball.clear_updaters()
        u_arrow.clear_updaters()
        u_label.clear_updaters()
        g_arrow.clear_updaters()
        g_label.clear_updaters()

        self.play(FadeOut(u_arrow), FadeOut(u_label)) # Remove velocity indicators
        self.wait(1)
        self.play(FadeOut(scene2_title), FadeOut(scene2_narration)) # Clear Scene 2 text

        # --- Scene 3: Top Point ---
        scene3_title = Text("Scene 3: Top Point", font_size=28).to_edge(UP, buff=0.3)
        scene3_narration = Text("At the top, the velocity becomes zero.", font_size=22).next_to(scene3_title, DOWN, buff=0.25)
        self.play(Write(scene3_title), Write(scene3_narration))

        v_zero_label = MathTex(f"v = {gs['final_velocity']}", font_size=30).next_to(ball, UP, buff=0.3)
        pause_message = Text("Ball stops momentarily", font_size=26).next_to(v_zero_label, UP, buff=0.2)

        self.play(Write(v_zero_label), Write(pause_message))
        self.wait(2)

        # Fade out elements not needed for Scene 4 (equations)
        elements_to_remove_s3 = VGroup(person, g_arrow, g_label, v_zero_label, pause_message, scene3_title, scene3_narration)
        self.play(FadeOut(elements_to_remove_s3))

        # --- Scene 4: Equation ---
        scene4_title = Text("Scene 4: Equation", font_size=28).to_edge(UP, buff=0.3)
        scene4_narration = Text("Using the kinematic equation, we solve for maximum height.", font_size=22).next_to(scene4_title, DOWN, buff=0.25)
        self.play(Write(scene4_title), Write(scene4_narration))

        # Prepare values for kinematic equation display
        u_squared_val = u_val**2
        two_times_a_val = 2 * a_val

        equation_steps_str = [
            "v^2 = u^2 + 2as",
            f"0^2 = ({u_val_str})^2 + 2({a_val_str})s",
            f"0 = {u_squared_val:.0f} {two_times_a_val:+.1f}s", # e.g., 0 = 400 -19.6s
            f"{-two_times_a_val:.1f}s = {u_squared_val:.0f}",   # e.g., 19.6s = 400
            f"s = \\frac{{{u_squared_val:.0f}}}{{{-two_times_a_val:.1f}}} \\approx {s_max_val_str}\\text{{ m}}"
        ]

        equations_vgroup = VGroup(*[MathTex(s, font_size=36) for s in equation_steps_str])
        equations_vgroup.arrange(DOWN, buff=0.3).next_to(scene4_narration, DOWN, buff=0.3)

        # Ensure equations fit on screen (clamp)
        if equations_vgroup.get_bottom()[1] < (-frame_height / 2 + 0.5): # Check bottom edge
            equations_vgroup.scale_to_fit_height(frame_height - scene4_narration.height - 1.5)
            equations_vgroup.next_to(scene4_narration, DOWN, buff=0.3)
        if equations_vgroup.get_left()[0] < (-frame_width / 2 + 0.5) or \
           equations_vgroup.get_right()[0] > (frame_width / 2 - 0.5): # Check side edges
            equations_vgroup.scale_to_fit_width(frame_width - 1.0)
            equations_vgroup.next_to(scene4_narration, DOWN, buff=0.3)

        # Animate each equation step
        for i, eq_tex in enumerate(equations_vgroup):
            self.play(Write(eq_tex))
            self.wait(1.8 if i < len(equations_vgroup) - 1 else 2.5) # Longer pause for final step

        self.wait(2.5)
        elements_to_remove_s4 = VGroup(equations_vgroup, scene4_title, scene4_narration)
        self.play(FadeOut(elements_to_remove_s4)) # Clear for final scene

        # --- Scene 5: Final Result ---
        scene5_title = Text("Scene 5: Final Result", font_size=28).to_edge(UP, buff=0.3)
        scene5_narration = Text(f"The ball reaches a maximum height of approximately {gs['max_height']}.", font_size=22).next_to(scene5_title, DOWN, buff=0.25)
        self.play(Write(scene5_title), Write(scene5_narration))

        # Ball is at its peak position. Ground is visible.
        # Dashed line from ground level (at ball's x-pos) to ball's bottom
        height_line_start_pt = np.array([ball.get_x(), ground.get_top()[1], 0])
        height_line_end_pt = ball.get_bottom() # Connects to the bottom of the ball

        max_height_line = DashedLine(start=height_line_start_pt, end=height_line_end_pt, color=YELLOW_C, stroke_width=4)

        max_height_label = MathTex(f"s = {gs['max_height']}", font_size=32).next_to(max_height_line, RIGHT, buff=0.2)

        # Adjust label position if it's off-screen (clamp)
        if max_height_label.get_right()[0] > frame_width / 2 - 0.2: # Too far right
            max_height_label.next_to(max_height_line, LEFT, buff=0.2)
        elif max_height_label.get_left()[0] < -frame_width / 2 + 0.2: # Too far left (if initially placed left)
             max_height_label.next_to(max_height_line, RIGHT, buff=0.2) # Fallback to right

        self.play(Create(max_height_line), Write(max_height_label))
        self.wait(3)

        # Final fade out of all remaining elements for a clean end
        self.play(
            FadeOut(ball), FadeOut(ground), FadeOut(max_height_line), FadeOut(max_height_label),
            FadeOut(scene5_title), FadeOut(scene5_narration)
        )
        self.wait(1)