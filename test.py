from tools.create_corpus import create_corpus
from tools.add_data import add_data
from tools.get_corpus_info import get_corpus_info
from google.adk.tools import InMemoryToolContext

ctx = InMemoryToolContext()

# Step 1: Create corpus
resp1 = create_corpus("manim_docs", tool_context=ctx)
print("📁 Corpus creation result:", resp1)

# Step 2: Add file
resp2 = add_data(
    corpus_name="manim_docs",
    paths=["gs://manim-rag-us-bucket/docs/merged_manim_docs.pdf"],
    tool_context=ctx
)
print("📄 File upload result:", resp2)

# Step 3: Get corpus info
resp3 = get_corpus_info("manim_docs", tool_context=ctx)
print("📑 Corpus info:", resp3)
