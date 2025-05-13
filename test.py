import numpy as np
from manim import *

class ProjectileStory(Scene):
    """
    Visualizes projectile motion with quadratic air resistance versus ideal motion.
    """
    def construct(self):
        # Physics parameters
        v0 = 30.0                    # initial speed (m/s)
        angle = 45 * DEGREES         # launch angle
        m = 1.0                      # mass (kg)
        g = 9.8                      # gravity (m/s^2)
        k = 0.05                     # drag coefficient
        dt = 0.01                    # time step

        # Initial velocity components
        vx0 = v0 * np.cos(angle)
        vy0 = v0 * np.sin(angle)

        # Precompute trajectories
        drag_positions = []
        x, y = 0.0, 0.0
        vx, vy = vx0, vy0
        # Simulate until projectile hits the ground
        while y >= 0:
            drag_positions.append((x, y))
            # Quadratic drag accelerations
            ax = - (k / m) * vx * abs(vx)
            ay = -g - (k / m) * vy * abs(vy)
            # Euler integration
            vx += ax * dt
            vy += ay * dt
            x += vx * dt
            y += vy * dt

        # Ideal (no drag) trajectory
        ideal_positions = []
        t = 0.0
        while True:
            x_i = vx0 * t
            y_i = vy0 * t - 0.5 * g * t ** 2
            if y_i < 0:
                break
            ideal_positions.append((x_i, y_i))
            t += dt

        # Determine axis limits
        max_x = max(p[0] for p in drag_positions + ideal_positions)
        max_y = max(p[1] for p in drag_positions + ideal_positions)

        # Create axes
        axes = Axes(
            x_range=[0, max_x * 1.1, max_x / 5],
            y_range=[0, max_y * 1.1, max_y / 5],
            axis_config={"include_numbers": True}
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes), Write(axes_labels))
        self.wait(1)

        # Display force and motion equations
        eq1 = MathTex(
            "F_d = -k v^2",
            font_size=36
        ).to_corner(UR)
        eq2 = MathTex(
            "m \, d v_x/dt = -k v_x^2",
            font_size=36
        ).next_to(eq1, DOWN, aligned_edge=LEFT)
        eq3 = MathTex(
            "m \, d v_y/dt = -m g - k v_y^2",
            font_size=36
        ).next_to(eq2, DOWN, aligned_edge=LEFT)
        self.play(Write(eq1), Write(eq2), Write(eq3))
        self.wait(1)

        # Show velocity components
        vel_eq = MathTex(
            "v_x = v_0 \cos \theta,",
            "v_y = v_0 \sin \theta",
            font_size=36
        ).to_corner(UL)
        self.play(Write(vel_eq))
        self.wait(1)

        # Create trajectory VMobjects
        drag_path = VMobject(color=RED)
        drag_path.set_points_as_corners([axes.c2p(x, y) for x, y in drag_positions])
        ideal_path = VMobject(color=GREEN)
        ideal_path.set_points_as_corners([axes.c2p(x, y) for x, y in ideal_positions])

        # Animate drawing of paths
        self.play(Create(ideal_path), Create(drag_path), run_time=4)
        self.wait(0.5)

        # Dots moving along paths
        dot_ideal = Dot(point=axes.c2p(*ideal_positions[0]), color=GREEN)
        dot_drag = Dot(point=axes.c2p(*drag_positions[0]), color=RED)
        self.add(dot_ideal, dot_drag)

        self.play(
            MoveAlongPath(dot_ideal, ideal_path),
            MoveAlongPath(dot_drag, drag_path),
            run_time=4,
            rate_func=linear
        )

        # Final summary
        summary = Tex(
            "With air resistance, the projectile has a lower maximum height",
            "and shorter range compared to the ideal case.",
            font_size=32
        ).next_to(axes, DOWN)
        self.play(Write(summary))
        self.wait(2)
