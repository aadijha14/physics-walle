from manim import *

class BallThrowMaxHeight(Scene):
    def construct(self):
        # Title
        title = Text("Maximum Height of a Thrown Ball", font_size=60, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        ### 🎬 Scene 1: Introduction – The Throw ###
        ground = Line(LEFT * 4, RIGHT * 4).shift(DOWN * 3)
        person = SVGMobject("manim_graphics/stick_figure.svg").scale(0.5).next_to(ground, UP).shift(LEFT * 2)
        ball = Dot(color=RED).scale(1.5).next_to(person, UP, buff=0.2)

        velocity_arrow = Arrow(start=ball.get_bottom(), end=ball.get_bottom() + UP * 2, color=BLUE)
        velocity_label = MathTex("u = 20\\,\\text{m/s}", font_size=36).next_to(velocity_arrow, RIGHT)

        label1 = Text("Ball is thrown straight up with 20 m/s", font_size=28).to_edge(DOWN, buff=0.5)

        self.play(Create(ground), FadeIn(person), FadeIn(ball))
        self.play(Create(velocity_arrow), Write(velocity_label))
        self.play(Write(label1))
        self.wait(2)
        self.play(FadeOut(label1))

        ### 🎬 Scene 2: Motion Setup ###
        # Show rising motion with velocity vectors decreasing
        ball_path = [ball.get_center() + UP * i for i in range(1, 5)]
        balls = [Dot(point=pos, color=RED).scale(1.2) for pos in ball_path]
        vectors = [Arrow(start=pos + DOWN * 0.3, end=pos + UP * (1.8 - i*0.4), color=BLUE)
                   for i, pos in enumerate(ball_path)]

        gravity_arrow = Arrow(start=ball.get_center() + UP * 4.5, end=ball.get_center() + UP * 3.5, color=GRAY)
        gravity_label = MathTex("a = -9.8\\,\\text{m/s}^2", font_size=36).next_to(gravity_arrow, RIGHT)

        self.play(*[FadeIn(b) for b in balls])
        self.play(*[Create(v) for v in vectors])
        self.play(Create(gravity_arrow), Write(gravity_label))
        self.wait(2)
        self.play(*[FadeOut(m) for m in balls + vectors + [gravity_arrow, gravity_label]])

        ### 🎬 Scene 3: Top of the Trajectory ###
        top_ball = Dot(ball.get_center() + UP * 4, color=RED).scale(1.5)
        stop_label = MathTex("v = 0\\,\\text{m/s}", font_size=36).next_to(top_ball, RIGHT)
        pause_text = Text("Ball stops momentarily", font_size=28).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(top_ball), Write(stop_label), Write(pause_text))
        self.wait(2)
        self.play(FadeOut(pause_text))

        ### 🎬 Scene 4: Equation and Substitution ###
        eq1 = MathTex("v^2 = u^2 + 2as", font_size=48)
        eq2 = MathTex("0 = 20^2 + 2(-9.8)(s)", font_size=48)
        eq3 = MathTex("0 = 400 - 19.6s", font_size=48)
        eq4 = MathTex("19.6s = 400", font_size=48)
        eq5 = MathTex("s = \\frac{400}{19.6} \\approx 20.41\\,\\text{m}", font_size=48)

        equation_group = VGroup(eq1, eq2, eq3, eq4, eq5).arrange(DOWN, buff=0.4)
        equation_group.to_edge(DOWN, buff=0.5)

        self.play(Write(eq1))
        self.wait(1)
        self.play(Transform(eq1, eq2))
        self.wait(1)
        self.play(Transform(eq1, eq3))
        self.wait(1)
        self.play(Transform(eq1, eq4))
        self.wait(1)
        self.play(Transform(eq1, eq5))
        self.wait(2)
        self.play(FadeOut(eq1))

        ### 🎬 Scene 5: Final Answer ###
        final_label = Text("Max height reached: 20.41 m", font_size=32, color=GREEN).to_edge(DOWN, buff=0.5)
        dotted_line = DashedLine(start=top_ball.get_center(), end=ground.get_top(), color=YELLOW)

        height_label = MathTex("s = 20.41\\,\\text{m}", font_size=36).next_to(dotted_line, RIGHT, buff=0.3)

        self.play(Create(dotted_line), Write(height_label), Write(final_label))
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

class BallThrowMaxHeightImproved(Scene):
    def construct(self):
        # Title
        title = Text("Maximum Height of a Thrown Ball", font_size=60, color=YELLOW)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Ground
        ground = Line(LEFT * 4, RIGHT * 4).shift(DOWN * 3.5)
        self.play(Create(ground))

        # Initial ball position
        start_pos = ORIGIN + DOWN * 2.5
        end_pos = start_pos + UP * 4.2  # top of motion
        ball = Dot(start_pos, color=RED).scale(1.4)
        self.play(FadeIn(ball))

        # Initial velocity arrow and label
        velocity_arrow = Arrow(start=start_pos + DOWN * 0.2, end=start_pos + UP * 1.5, color=BLUE)
        velocity_label = MathTex("u = 20\\,\\text{m/s}", font_size=36).next_to(velocity_arrow, RIGHT, buff=0.2)
        self.play(Create(velocity_arrow), Write(velocity_label))
        self.wait(1)

        self.play(FadeOut(velocity_arrow), FadeOut(velocity_label))

        # Animate ball rising
        self.play(ball.animate.move_to(end_pos), run_time=3, rate_func=smooth)
        self.wait(0.5)

        # Label at top
        top_label = MathTex("v = 0\\,\\text{m/s}", font_size=36).next_to(ball, LEFT, buff=0.3)
        self.play(Write(top_label))
        self.wait(1)

        # Draw downward gravity arrow
        gravity_arrow = Arrow(start=end_pos + UP * 1, end=end_pos + DOWN * 0.8, color=GRAY)
        gravity_label = MathTex("a = -9.8\\,\\text{m/s}^2", font_size=36).next_to(gravity_arrow, RIGHT, buff=0.2)
        self.play(Create(gravity_arrow), Write(gravity_label))
        self.wait(1)

        # Fade everything but title and ball
        self.play(FadeOut(gravity_arrow), FadeOut(gravity_label), FadeOut(top_label))

        # Equation and solving animation
        eq1 = MathTex("v^2 = u^2 + 2as", font_size=44)
        eq2 = MathTex("0 = 20^2 + 2(-9.8)(s)", font_size=44)
        eq3 = MathTex("0 = 400 - 19.6s", font_size=44)
        eq4 = MathTex("19.6s = 400", font_size=44)
        eq5 = MathTex("s = \\frac{400}{19.6} \\approx 20.41\\,\\text{m}", font_size=44)

        equation_group = VGroup(eq1, eq2, eq3, eq4, eq5).arrange(DOWN, buff=0.4)
        equation_group.to_corner(DOWN + LEFT, buff=0.7)

        self.play(Write(eq1))
        self.wait(1)
        self.play(Transform(eq1, eq2))
        self.wait(1)
        self.play(Transform(eq1, eq3))
        self.wait(1)
        self.play(Transform(eq1, eq4))
        self.wait(1)
        self.play(Transform(eq1, eq5))
        self.wait(1.5)

        # Final diagram: height
        height_line = DashedLine(start=end_pos, end=start_pos, color=YELLOW)
        height_label = MathTex("s = 20.41\\,\\text{m}", font_size=36).next_to(height_line, RIGHT, buff=0.2)

        self.play(Create(height_line), Write(height_label))
        self.wait(3)

        # Clean exit
        self.play(*[FadeOut(mob) for mob in self.mobjects])
