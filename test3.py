from manim import *

class EulerIdentityGraph(Scene):
    def construct(self):
        # Title
        title = Text("Euler's Identity", font_size=60, color=YELLOW, font="Arial")
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        # Euler's Identity
        identity = MathTex("e^{i\\pi} + 1 = 0", font_size=72)
        identity.set_color_by_tex_to_color_map({
            "e": BLUE, "i": GREEN, "\\pi": RED, "1": ORANGE, "0": PURPLE
        })
        identity.next_to(title, DOWN, buff=0.5)
        self.play(Write(identity))
        self.wait(1)

        # Narration 1
        narration1 = Text(
            "Euler's identity is a special case of Euler's formula:",
            font_size=28, font="Arial"
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(narration1))
        self.wait(2)

        # Euler's Formula
        formula = MathTex("e^{ix} = \\cos x + i\\sin x", font_size=60)
        formula.set_color_by_tex_to_color_map({
            "e": BLUE, "i": GREEN, "x": WHITE, "\\cos": TEAL, "\\sin": ORANGE
        })
        formula.next_to(identity, DOWN, buff=0.75)
        self.play(Write(formula))
        self.wait(2)

        self.play(FadeOut(narration1))

        # Narration 2
        narration2 = Text(
            "This describes a point rotating on the unit circle.",
            font_size=28, font="Arial"
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(narration2))

        # Complex Plane
        plane = ComplexPlane(
            x_range=[-2, 2], y_range=[-2, 2],
            background_line_style={"stroke_opacity": 0.4}
        ).add_coordinates()
        plane.scale(0.8)
        plane.shift(DOWN * 0.5)
        self.play(Create(plane))
        self.wait(1)

        # Unit Circle
        circle = Circle(radius=1, color=WHITE).move_to(plane.c2p(0, 0))
        self.play(Create(circle))

        # Dot on circle
        dot = Dot(point=plane.c2p(1, 0), color=BLUE)
        radius_line = always_redraw(
            lambda: Line(plane.c2p(0, 0), dot.get_center(), color=YELLOW)
        )
        self.play(FadeIn(dot), Create(radius_line))
        self.wait(0.5)

        # Animate rotation 0 to π
        self.play(Rotate(dot, angle=PI, about_point=plane.c2p(0, 0), run_time=4))
        self.wait(1)

        self.play(FadeOut(narration2))

        # Narration 3
        narration3 = Text(
            "At x = pi, the point reaches -1 on the real axis:",
            font_size=28, font="Arial"
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(narration3))

        # Highlight -1
        minus_one = Dot(point=plane.c2p(-1, 0), color=RED)
        label_minus_one = MathTex("-1", font_size=36, color=RED).next_to(minus_one, DOWN, buff=0.1)
        self.play(FadeIn(minus_one), Write(label_minus_one))
        self.wait(2)

        self.play(FadeOut(narration3))

        # Narration 4
        narration4 = Text(
            "So, e^{iπ} = -1. Add 1 to get 0 — Euler's identity!",
            font_size=28, font="Arial"
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(narration4))

        final_eq = MathTex("e^{i\\pi} = -1", font_size=60, color=WHITE)
        final_eq.next_to(formula, DOWN, buff=0.75)
        self.play(Write(final_eq))
        self.wait(1)

        # Highlight main identity again
        boxed = SurroundingRectangle(identity, color=YELLOW)
        self.play(Create(boxed))
        self.wait(3)

        # Outro
        self.play(*[FadeOut(mob) for mob in self.mobjects])
