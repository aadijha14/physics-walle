from manim import *

class BallThrowAnimation(Scene):
    def construct(self):
        # Scene 1: Introduction - The Throw
        ground = Line(LEFT*5, RIGHT*5, color=GREEN)
        ball = Dot(color=BLUE).move_to(ground.get_start()).shift(UP*0.5)
        velocity_arrow = Arrow(ball.get_center(), ball.get_center()+UP*2, color=YELLOW)
        velocity_label = Tex("$u = 20\\, \\text{m/s}$").next_to(velocity_arrow, RIGHT)

        self.play(Create(ground), Create(ball))
        self.play(GrowArrow(velocity_arrow), Write(velocity_label))
        self.play(ball.animate.shift(UP*3), run_time=2)
        self.wait()

        # Scene 2: Motion Setup
        positions = [UP*3, UP*4.5, UP*5.5]
        velocity_arrows = VGroup()
        velocity_labels = VGroup()
        gravity_arrows = VGroup()
        gravity_labels = VGroup()

        for i, pos in enumerate(positions):
            va = Arrow(pos, pos+UP*(2-0.7*i), color=YELLOW)
            vl = Tex(f"$v = {20-7*(i+1)}\\, \\text{{m}}/s$").scale(0.8).next_to(va, RIGHT)
            ga = Arrow(pos, pos+DOWN*0.5, color=RED)
            gl = Tex("$a = -9.8\\, \\text{m/s}^2$").scale(0.8).next_to(ga, LEFT)
            
            velocity_arrows.add(va)
            velocity_labels.add(vl)
            gravity_arrows.add(ga)
            gravity_labels.add(gl)

        self.play(
            ball.animate.move_to(positions[0]),
            LaggedStart(
                GrowArrow(velocity_arrows[0]),
                Write(velocity_labels[0]),
                GrowArrow(gravity_arrows[0]),
                Write(gravity_labels[0]),
                lag_ratio=0.5
            )
        )
        for i in range(1, len(positions)):
            self.play(
                ball.animate.move_to(positions[i]),
                LaggedStart(
                    ReplacementTransform(velocity_arrows[i-1], velocity_arrows[i]),
                    ReplacementTransform(velocity_labels[i-1], velocity_labels[i]),
                    ReplacementTransform(gravity_arrows[i-1], gravity_arrows[i]),
                    ReplacementTransform(gravity_labels[i-1], gravity_labels[i]),
                    lag_ratio=0.5
                )
            )
        self.wait()

        # Scene 3: Top of Trajectory
        top_label = Tex("$v = 0\\, \\text{m/s}$").next_to(ball, UP)
        self.play(
            ball.animate.set_color(RED),
            ReplacementTransform(velocity_arrows[-1], top_label),
            FadeOut(velocity_labels[-1]),
            FadeOut(gravity_arrows[-1]),
            FadeOut(gravity_labels[-1]),
        )
        self.wait()

        # Scene 4: Equation and Substitution
        equation = MathTex("v^2 = u^2 + 2as").to_edge(UP)
        substituted = MathTex("0^2 = (20)^2 + 2(-9.8)s").next_to(equation, DOWN, buff=0.5)
        simplified = MathTex("0 = 400 - 19.6s").next_to(substituted, DOWN, buff=0.5)
        solved = MathTex("s = \\frac{400}{19.6} \\approx 20.41\\, \\text{m}").next_to(simplified, DOWN, buff=0.5)

        self.play(Write(equation))
        self.wait()
        self.play(Write(substituted))
        self.wait()
        self.play(Write(simplified))
        self.wait()
        self.play(Write(solved))
        self.wait()

        # Scene 5: Final Answer
        dotted_line = DashedLine(ground.get_start()+UP*0.5, ball.get_center(), color=WHITE)
        height_label = Tex("20.41\\, \\text{m}").next_to(dotted_line, RIGHT)
        caption = Tex("Maximum height reached: 20.41 meters").to_edge(DOWN)

        self.play(
            Create(dotted_line),
            Write(height_label),
            Write(caption)
        )
        self.wait(3)