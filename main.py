import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types
from google.genai.types import Part, Blob
from agents.manim_agent import manim_agent
from dotenv import load_dotenv
import os

load_dotenv()

# Constants
APP_NAME = "manim_app"
USER_ID = "user_manim"
SESSION_ID = "session_001"

# ✅ 1. Setup artifact service and load PDF artifact
artifact_service = InMemoryArtifactService()

with open("merged_manim_docs.pdf", "rb") as f:
    pdf_bytes = f.read()

# ✅ Use correct method to construct Part in latest SDK
pdf_part = Part(
    inline_data=Blob(
        mime_type="application/pdf",
        data=pdf_bytes
    )
)

async def main():
    # ✅ Save as a user-scoped artifact (available across sessions)
    await artifact_service.save_artifact(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=None,
        filename="user:manim_docs.pdf",
        artifact=pdf_part
    )

    # ✅ 2. Create session
    session_service = InMemorySessionService()
    session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    # ✅ 3. Runner setup with artifact service
    runner = Runner(
        agent=manim_agent,
        app_name=APP_NAME,
        session_service=session_service,
        artifact_service=artifact_service
    )

    # ✅ 4. Your scene data input
    scene_data = {
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

    # ✅ 5. Prompt Gemini to use RAG + the input scene_data
    prompt = f"scene_data = {scene_data}\nGenerate the Manim code to render this scene as a video."

    content = types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    )

    # ✅ 6. Run the agent
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
        if event.content and event.content.parts:
            print("\n🎬 Generated Manim Code:\n")
            print(event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())
