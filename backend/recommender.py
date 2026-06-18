import os
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI, RateLimitError
from dotenv import load_dotenv
from data.creators_data import CREATORS_DATA

load_dotenv()

client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
CHAT_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-8b-instant"

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")


def _llm(messages, max_tokens=1024):
    try:
        r = client.chat.completions.create(model=CHAT_MODEL, messages=messages, max_tokens=max_tokens, temperature=0.4)
        return r.choices[0].message.content.strip()
    except RateLimitError:
        r = client.chat.completions.create(model=FALLBACK_MODEL, messages=messages, max_tokens=max_tokens, temperature=0.4)
        return r.choices[0].message.content.strip()


def _get_creator_collection():
    chroma = chromadb.PersistentClient(path=CHROMA_PATH)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    return chroma.get_or_create_collection(
        name="creators",
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"}
    )


def ingest_creators():
    col = _get_creator_collection()
    existing = set(col.get()["ids"])
    new = [c for c in CREATORS_DATA if c["id"] not in existing]
    if not new:
        return len(CREATORS_DATA)

    col.add(
        ids=[c["id"] for c in new],
        documents=[f"{c['name']} — {c['category']}\n{c['description']}\nTags: {c['content_tags']}" for c in new],
        metadatas=[{
            "name": c["name"],
            "platform": c["platform"],
            "category": c["category"],
            "games": ", ".join(c["games"]),
            "style": c["style"],
            "audience": c["audience"]
        } for c in new]
    )
    return len(CREATORS_DATA)


def recommend_creators(games: list[str], content_style: str, goal: str, n: int = 5) -> dict:
    col = _get_creator_collection()
    total = col.count()
    if total == 0:
        ingest_creators()

    # Build a rich preference query for embedding similarity
    query = f"I play {', '.join(games)}. I enjoy {content_style} content. My goal is {goal}."

    results = col.query(
        query_texts=[query],
        n_results=min(n, col.count()),
        include=["documents", "metadatas", "distances"]
    )

    creators = []
    creator_lookup = {c["id"]: c for c in CREATORS_DATA}

    for i, doc in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][i]
        match_score = round((1 - results["distances"][0][i]) * 100, 1)
        # Find full creator data by name
        full = next((c for c in CREATORS_DATA if c["name"] == meta["name"]), None)
        creators.append({
            "name": meta["name"],
            "platform": meta["platform"],
            "category": meta["category"],
            "games": meta["games"],
            "style": meta["style"],
            "audience": meta["audience"],
            "description": full["description"] if full else doc[:200],
            "match_score": match_score
        })

    # Ask LLM to explain why each creator matches
    creators_text = "\n\n".join([
        f"{i+1}. {c['name']} ({c['category']}) — {c['style']}\n   {c['description'][:200]}"
        for i, c in enumerate(creators)
    ])

    prompt = f"""A user is looking for gaming creators to follow.

User Profile:
- Games they play: {', '.join(games)}
- Content style they enjoy: {content_style}
- Their goal: {goal}

Recommended Creators (already selected by AI similarity search):
{creators_text}

For each creator, write 1-2 sentences explaining exactly WHY this creator matches this specific user's profile and goal.
Be specific — mention their games, style, and goal.

Reply in this exact format for each creator:
1. [CreatorName]: [explanation]
2. [CreatorName]: [explanation]
...and so on."""

    explanation_text = _llm([{"role": "user", "content": prompt}])

    # Parse explanations and attach to creators
    explanations = {}
    for line in explanation_text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        for c in creators:
            if c["name"] in line and ":" in line:
                exp = line.split(":", 1)[-1].strip()
                explanations[c["name"]] = exp
                break

    for c in creators:
        c["why"] = explanations.get(c["name"], f"Matches your interest in {', '.join(games)} content.")

    return {
        "query": query,
        "games": games,
        "style": content_style,
        "goal": goal,
        "creators": creators
    }
