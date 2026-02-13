import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

TEXT_MODEL = "gemini-2.5-flash"
EMBED_MODEL = "gemini-embedding-001"


# ---------------------------
# Text Generation
# ---------------------------
def generate_text(prompt: str) -> str:
    model = genai.GenerativeModel(TEXT_MODEL)
    response = model.generate_content(prompt)
    return response.text


# ---------------------------
# Embeddings (v1beta compatible)
# ---------------------------
def get_embedding(text: str) -> list[float]:
    result = genai.embed_content(
        model=EMBED_MODEL,
        content=text,
        task_type="retrieval_document"
    )
    return result["embedding"]

print(len(get_embedding("test")))
