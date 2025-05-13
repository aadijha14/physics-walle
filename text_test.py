from manim import *

class FontCheck(Scene):
    def construct(self):
        t = Text("Test Text", font_size=48, font="Arial")
        self.add(t)
        self.wait()
