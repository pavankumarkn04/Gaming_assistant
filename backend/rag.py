import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

from data.valorant_data import VALORANT_DATA
from data.fifa_data import FIFA_DATA
from data.f1_data import F1_DATA

load_dotenv()

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")

def get_embedding_function():
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    ef = get_embedding_function()
    return client.get_or_create_collection(
        name="gaming_knowledge",
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"}
    )


def ingest_all_data():
    collection = get_collection()
    all_data = VALORANT_DATA + FIFA_DATA + F1_DATA

    existing = set(collection.get()["ids"])
    new_docs = [doc for doc in all_data if doc["id"] not in existing]

    if not new_docs:
        print(f"All {len(all_data)} documents already indexed.")
        return len(all_data)

    collection.add(
        ids=[doc["id"] for doc in new_docs],
        documents=[f"{doc['title']}\n\n{doc['content']}" for doc in new_docs],
        metadatas=[{
            "game": doc["game"],
            "category": doc["category"],
            "title": doc["title"]
        } for doc in new_docs]
    )
    print(f"Indexed {len(new_docs)} new documents. Total: {len(all_data)}.")
    return len(all_data)


def search_knowledge(query: str, game_filter: str = None, n_results: int = 4) -> list[dict]:
    collection = get_collection()
    where = {"game": game_filter} if game_filter and game_filter != "all" else None

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count()),
        where=where,
        include=["documents", "metadatas", "distances"]
    )

    docs = []
    for i, doc in enumerate(results["documents"][0]):
        docs.append({
            "content": doc,
            "metadata": results["metadatas"][0][i],
            "relevance": round(1 - results["distances"][0][i], 3)
        })
    return docs


def get_document_count() -> dict:
    collection = get_collection()
    total = collection.count()
    all_meta = collection.get(include=["metadatas"])["metadatas"]
    by_game = {}
    for m in all_meta:
        g = m.get("game", "unknown")
        by_game[g] = by_game.get(g, 0) + 1
    return {"total": total, "by_game": by_game}
