# runner.py
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from manim_agent import manim_agent

# Constants
APP_NAME = "manim_rag_app"
USER_ID = "manim_user"
SESSION_ID = "session_001"

async def main():
    # 1) Initialize the session service & create a session
    session_service = InMemorySessionService()
    session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    # 2) Initialize Runner with your Manim agent
    runner = Runner(
        agent=manim_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    # 3) Build the user prompt
    prompt = """Animate this solution to a problem
        {
            "title": "Ball Thrown Upward – Max Height",
            "global_settings": {
                "ball_color": "RED",
                "initial_velocity": "20 m/s",
                "acceleration": "-9.8 m/s^2",
                "final_velocity": "0 m/s",
                "max_height": "20.41 m"
            },
            "scenes": [
                {
                    "name": "Scene 1: Introduction",
                    "objects": [
                        {"type": "ground", "position": "BOTTOM"},
                        {"type": "person", "asset": "stick_figure.svg", "position": "LEFT"},
                        {"type": "ball", "position": "above_person"},
                        {"type": "arrow", "label": "u = 20 m/s", "direction": "UP", "from": "ball"}
                    ],
                    "narration": "A ball is thrown straight up with 20 m/s."
                },
                {
                    "name": "Scene 2: Ball Motion",
                    "animations": [
                        {"type": "move_ball", "path": "upward", "distance": "4.2"},
                        {"type": "velocity_arrow", "sizes": [2, 1.5, 1.0, 0.5]},
                        {"type": "gravity_arrow", "direction": "DOWN", "label": "a = -9.8 m/s^2"}
                    ],
                    "narration": "The ball slows down as it rises, due to gravity acting downward."
                },
                {
                    "name": "Scene 3: Top Point",
                    "objects": [
                        {"type": "dot", "position": "top", "label": "v = 0 m/s"},
                        {"type": "pause_label", "text": "Ball stops momentarily"}
                    ],
                    "narration": "At the top, the velocity becomes zero."
                },
                {
                    "name": "Scene 4: Equation",
                    "math_steps": [
                        "v^2 = u^2 + 2as",
                        "0 = 20^2 + 2(-9.8)s",
                        "0 = 400 - 19.6s",
                        "19.6s = 400",
                        "s = 400 / 19.6 ≈ 20.41 m"
                    ],
                    "narration": "Using the kinematic equation, we solve for maximum height."
                },
                {
                    "name": "Scene 5: Final Result",
                    "objects": [
                        {"type": "ball", "position": "top"},
                        {"type": "dashed_line", "from": "top", "to": "ground"},
                        {"type": "label", "text": "s = 20.41 m"}
                    ],
                    "narration": "The ball reaches a maximum height of approximately 20.41 meters."
                }
            ]
        }
        """
    content = types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    )

    # 4) Run the agent asynchronously and print its responses
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content
    ):
        if event.content and event.content.parts:
            print(event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())
