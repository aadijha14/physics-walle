import numpy as np
from manim import *

class ProjectileStory(Scene):
    v0_val = 30.0
    angle_deg_val = 45.0
    m_val = 1.0
    g_val = 9.8
    k_val = 0.05

    angle_rad_val = np.deg2rad(angle_deg_val)
    vx0_val = v0_val * np.cos(angle_rad_val)
    vy0_val = v0_val * np.sin(angle_rad_val)

    simulation_dt = 0.005
    time_dilation_factor = 1.0

    def initialize_simulation_state(self):
        self.x = 0.0
        self.y = 0.0
        self.vx = self.vx0_val
        self.vy = self.vy0_val
        self.t = 0.0
        if hasattr(self, 'axes'):
            self.path_drag_points = [self.axes.c2p(self.x, self.y)]
            self.path_ideal_points = [self.axes.c2p(self.x, self.y)]
        else:
            self.path_drag_points = [ORIGIN]
            self.path_ideal_points = [ORIGIN]

    def setup_scene_elements(self):
        self.initialize_simulation_state()
        self.title_text = Tex("Projectile Motion with Quadratic Air Resistance").to_edge(UP)
        self.axes = Axes(
            x_range=[0, 40, 5],
            y_range=[0, 15, 3],
            x_length=9,
            y_length=5,
            axis_config={"include_numbers": True, "tip_shape": StealthTip},
            x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
            y_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
        ).add_coordinates()
        self.axes_labels = self.axes.get_axis_labels(x_label="x (m)", y_label="y (m)")

        self.dot = Dot(self.axes.c2p(self.x, self.y), color=YELLOW, radius=0.08)
        self.path_drag = VMobject().set_style(stroke_color=ManimColor("#58C4DD"), stroke_width=4)
        self.path_drag.set_points_as_corners([self.axes.c2p(self.x, self.y)])
        self.path_ideal = VMobject().set_style(stroke_color=GREEN, stroke_width=4, stroke_opacity=0.6)
        self.path_ideal.set_points_as_corners([self.axes.c2p(self.x, self.y)])

        self.vel_arrow_scale = 0.07
        self.vx_vector_vis = Arrow(
            self.dot.get_center(), 
            self.dot.get_center() + RIGHT * self.vx * self.vel_arrow_scale,
            buff=0, color=RED_B, stroke_width=5
        )
        self.vy_vector_vis = Arrow(
            self.dot.get_center(), 
            self.dot.get_center() + UP * self.vy * self.vel_arrow_scale,
            buff=0, color=ManimColor("#9CDCEB"), stroke_width=5
        )

        # Velocity displays
        self.vx_display_text = MathTex("v_x(t) = ", font_size=30)
        self.vx_display_val = DecimalNumber(self.vx, num_decimal_places=1, font_size=30)
        self.vy_display_text = MathTex("v_y(t) = ", font_size=30)
        self.vy_display_val = DecimalNumber(self.vy, num_decimal_places=1, font_size=30)
        vx_display_elements = VGroup(self.vx_display_text, self.vx_display_val).arrange(RIGHT, buff=0.1)
        vy_display_elements = VGroup(self.vy_display_text, self.vy_display_val).arrange(RIGHT, buff=0.1)
        self.vel_display_group = VGroup(vx_display_elements, vy_display_elements).arrange(DOWN, buff=0.15).to_corner(DOWN + LEFT)
        self.vx_display_val.add_updater(lambda d: d.set_value(self.vx))
        self.vy_display_val.add_updater(lambda d: d.set_value(self.vy))

    def show_initial_setup_animation(self):
        self.play(Write(self.title_text))
        self.play(Create(self.axes), Write(self.axes_labels))
        self.play(FadeIn(self.dot, scale=0.5))
        self.wait(0.2)

    def run_projectile_animation(self):
        self.add(self.path_drag, self.path_ideal)
        self.add(self.vx_vector_vis, self.vy_vector_vis)
        self.add(self.vel_display_group)
        self.dot.add_updater(self.projectile_updater)
        self.vx_vector_vis.add_updater(self.vx_vector_updater)
        self.vy_vector_vis.add_updater(self.vy_vector_updater)

        max_simulation_time = (self.vy0_val / self.g_val) * 2.5
        while (self.y >= 0 or self.t <= 0.01) and (self.t <= max_simulation_time):
            self.wait(0.03)

        self.dot.clear_updaters()
        self.vx_vector_vis.clear_updaters()
        self.vy_vector_vis.clear_updaters()
        self.vx_display_val.clear_updaters()
        self.vy_display_val.clear_updaters()

    def projectile_updater(self, mob, dt):
        if self.y < 0 and self.t > 0.01:
            return
        dt_sim = dt * self.time_dilation_factor
        for _ in range(max(1, int(dt_sim / self.simulation_dt))):
            if self.y < 0 and self.t > 0.01:
                break
            ax = -(self.k_val / self.m_val) * self.vx**2
            ay = -self.g_val - (self.k_val / self.m_val) * self.vy**2
            self.vx += ax * self.simulation_dt
            self.vy += ay * self.simulation_dt
            self.x += self.vx * self.simulation_dt
            self.y += self.vy * self.simulation_dt
            self.t += self.simulation_dt
            self.path_drag_points.append(self.axes.c2p(self.x, self.y))
            self.path_drag.add_points_as_corners([self.axes.c2p(self.x, self.y)])
            x_ideal = self.vx0_val * self.t
            y_ideal = self.vy0_val * self.t - 0.5 * self.g_val * self.t**2
            if y_ideal >= 0:
                self.path_ideal_points.append(self.axes.c2p(x_ideal, y_ideal))
                self.path_ideal.add_points_as_corners([self.axes.c2p(x_ideal, y_ideal)])
            mob.move_to(self.axes.c2p(self.x, self.y))

    def vx_vector_updater(self, mob):
        start = self.dot.get_center()
        end = start + RIGHT * self.vx * self.vel_arrow_scale
        mob.put_start_and_end_on(start, end)

    def vy_vector_updater(self, mob):
        start = self.dot.get_center()
        end = start + UP * self.vy * self.vel_arrow_scale
        mob.put_start_and_end_on(start, end)

    def show_summary_statement(self):
        summary_statement_text = Tex(
            "Air resistance, modeled here with quadratic drag, \\"\
            "significantly alters the projectile's path, \\"\
            "reducing both its range and maximum height.",
            font_size=36
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeOut(self.vx_vector_vis), FadeOut(self.vy_vector_vis))
        self.play(Write(summary_statement_text))
        self.wait(2)

    def construct(self):
        self.setup_scene_elements()
        self.show_initial_setup_animation()
        self.run_projectile_animation()
        self.show_summary_statement()
        self.wait(0.5)
