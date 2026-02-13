from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from agents.client import get_embedding
import uuid
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

client = QdrantClient(
    path=os.path.join(BASE_DIR, "qdrant_data")  # ✅ EMBEDDED MODE
)

COLLECTION_NAME = "agent_memory"
VECTOR_SIZE = 3072  # Gemini embedding size

# -----------------------------------
# Ensure collection exists
# -----------------------------------
def ensure_collection():
    existing = client.get_collections().collections
    names = [c.name for c in existing]

    if COLLECTION_NAME not in names:
        client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=VECTOR_SIZE,
        distance=Distance.COSINE
    )
)


ensure_collection()

# -----------------------------------
# Store memory
# -----------------------------------
def store_embedding(text: str):
    vector = get_embedding(text)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            {
                "id": str(uuid.uuid4()),
                "vector": vector,
                "payload": {"text": text}
            }
        ]
    )

# -----------------------------------
# ✅ CORRECT SEARCH METHOD
# -----------------------------------
def query_vectors(query: str, k: int = 3):
    qvec = get_embedding(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        prefetch=[],
        query=qvec,
        limit=k,
        with_payload=True
    )

    return [point.payload["text"] for point in results.points]
