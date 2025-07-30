import chromadb
from chromadb.utils import embedding_functions

# Initialize Chroma client
db = chromadb.Client()

# Default embedding function (use OpenAI, HuggingFace, or local encoder)
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

# Create collection (or get existing)
collection = db.get_or_create_collection("gyaanchand_embeddings")

def add_document(doc_id: str, text: str):
    collection.add(documents=[text], ids=[doc_id])

def query_document(query: str, top_k=3):
    return collection.query(query_texts=[query], n_results=top_k)
