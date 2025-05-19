from tools.create_corpus import create_corpus
from tools.add_data import add_data
# A minimal fake context just for testing
class DummyContext:
    def __init__(self):
        self.state = {}

tool_context = DummyContext()
# Step 1: Create corpus
create_result = create_corpus("manim_docs", tool_context=tool_context)
print(create_result)

# Step 2: Add PDF to corpus
add_result = add_data(
    corpus_name="manim_docs",
    paths=["gs://manim-rag-us-bucket/docs/merged_manim_docs.pdf"],
    tool_context=tool_context
)
print(add_result)
