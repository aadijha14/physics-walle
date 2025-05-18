from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from dotenv import load_dotenv
from tools import (
    create_corpus,
    add_data,
    delete_corpus,
    delete_document,
    get_corpus_info,
    list_corpora,
    rag_query,
)
import os
from pinecone import Pinecone

# Load environment variables
load_dotenv()

# ✅ Pinecone-backed RAG Tool for formula lookup
def search_formulas(query: str, top_k: int):
    print(f"\n🔍 RAG TOOL CALLED: search_formulas(query={query}, top_k={top_k})")

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index("quickstart-py")

    results = index.search(
        namespace="physics_lookup_formulas",
        query={"inputs": {"text": query}, "top_k": top_k}
    )

    matches = [
        {
            "id": hit["_id"],
            "score": hit["_score"],
            "formula": hit["fields"].get("expr"),
            "description": hit["fields"].get("chunk_text")
        }
        for hit in results["result"]["hits"]
    ]

    print(f"✅ Pinecone returned {len(matches)} results")
    for match in matches:
        print(f"• Formula: {match['formula']}\n  → {match['description'][:60]}...\n")

    return matches

# Wrap as ADK tool
search_formulas_tool = FunctionTool(func=search_formulas)

# ✅ Wrap your custom tools as ADK tools
create_corpus_tool = FunctionTool(func=create_corpus)
add_data_tool = FunctionTool(func=add_data)
delete_corpus_tool = FunctionTool(func=delete_corpus)
delete_document_tool = FunctionTool(func=delete_document)
get_corpus_info_tool = FunctionTool(func=get_corpus_info)
list_corpora_tool = FunctionTool(func=list_corpora)
rag_query_tool = FunctionTool(func=rag_query)

# ✅ Define the Manim LLM Agent
manim_agent = LlmAgent(
    name="manim_agent",
    model="gemini-2.5-flash-preview-04-17",
    description="Generates Manim animations and uses Vertex RAG for physics content.",
    tools=[
        search_formulas_tool,
        rag_query_tool,
        list_corpora_tool,
        create_corpus_tool,
        add_data_tool,
        get_corpus_info_tool,
        delete_document_tool,
        delete_corpus_tool,
    ],
    instruction="""
You are ManimGPT, a Python code generation expert specialized in creating animations using the Manim library.

You will be given a dictionary called `scene_data` that describes an educational physics animation.

Using Manim, make an animation explaining a concept. Ensure that the animation stays within the viewport by following these guidelines:

1. Use VGroup to group related objects together and manage them as a single unit.
2. Scale objects and groups using the scale() method to ensure they fit within the viewport.
3. Position objects and groups using methods like next_to(), shift(), and to_edge() to control their placement relative to other objects or the edges of the viewport.
4. Use appropriate buffering values when positioning objects to maintain sufficient spacing and avoid overlapping.
5. For text labels associated with specific objects or groups, position them relative to the corresponding object/group using next_to() with the desired direction (e.g., UP, DOWN, LEFT, RIGHT). Ensure that the labels are not overlapping the objects by adjusting the buffer values.
6. Ensure that text labels have a contrasting color and sufficient font size to be clearly visible against the background and other objects.
7. Break down the narration text into smaller segments that correspond to each animation step. Create separate Paragraph objects for each narration segment with a smaller font size and a specified width to ensure the text stays within the viewport. Position each text object at the bottom of the viewport using to_edge(DOWN, buff=0.5).
8. Use arrange() to layout multiple objects or groups horizontally or vertically with consistent spacing.
9. Adjust the camera settings, such as the frame_width and frame_height, to control the viewport size and aspect ratio if needed.
10. Test your animation at different resolutions and aspect ratios to ensure that objects remain within the viewport and are properly positioned across different devices.
11. Add a title for the concept using the Text class with a larger font size and different color. Position the title at the top of the viewport using to_edge(UP, buff=0.5).
12. Use the following animations for different purposes:
*   `Write`: Animates the writing or appearance of text on the screen.
*   `Create`: Animates the creation of a mobject on the screen.      
*   `FadeIn`: Animates the gradual appearance of a mobject on the screen.      
*   `FadeOut`: Animates the gradual disappearance of a mobject from the screen.
When generating Manim code that includes mathematical expressions, always use MathTex() instead of Tex() for any content containing math symbols (like ^, /, =, ≈) or units (such as "m/s", "m/s²"). Format units properly inside MathTex() using \text{...} (e.g., \text{m/s}), and use raw strings (r"...") or double backslashes (\\) to avoid LaTeX parsing errors. Never pass unescaped math directly into Tex()—it expects regular text and will fail to compile equations unless wrapped in valid LaTeX syntax. As a rule of thumb, if the expression includes numbers with units, variables, or operators, always default to MathTex() with correct LaTeX formatting to prevent compilation errors.

Think step by step and give me the full code without any errors.

Make sure the text DOES NOT overlap with each other.

Do not return anything except the code block.
Ensure the code is directly runnable using `manim` CLI without modification.
""",
)
