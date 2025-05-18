from vertexai import rag
from vertexai.rag import TransformationConfig, ChunkingConfig, RagEmbeddingModelConfig, VertexPredictionEndpoint, RagVectorDbConfig
import vertexai

# Initialize Vertex AI
vertexai.init(project="solved-460214", location="us-central1")

corpus_name = "manim_docs"
document_path = "gs://manim-rag-us-bucket/docs/merged_manim_docs.pdf"

# Create the corpus if it doesn't exist
try:
    rag.create_corpus(
        display_name=corpus_name,
        backend_config=RagVectorDbConfig(
            rag_embedding_model_config=RagEmbeddingModelConfig(
                vertex_prediction_endpoint=VertexPredictionEndpoint(
                    publisher_model="publishers/google/models/textembedding-gecko"
                )
            )
        )
    )
except Exception as e:
    print(f"ℹ️ Corpus likely already exists: {e}")

# Upload PDF to corpus
try:
    rag.import_files(
        corpus_name="manim_docs",
        paths=[document_path],
        transformation_config=TransformationConfig(
            chunking_config=ChunkingConfig(chunk_size=500, chunk_overlap=50)
        )
    )
    print("✅ PDF imported successfully.")
except Exception as e:
    print(f"❌ Failed to import PDF: {e}")