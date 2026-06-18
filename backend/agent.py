import os
from openai import OpenAI
from dotenv import load_dotenv
from rag import search_knowledge

load_dotenv()

client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
CHAT_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-8b-instant"


def _chat(messages, max_tokens=2048, temperature=0.5):
    from openai import RateLimitError
    try:
        r = client.chat.completions.create(model=CHAT_MODEL, messages=messages, max_tokens=max_tokens, temperature=temperature)
        return r.choices[0].message.content or ""
    except RateLimitError:
        print(f"Rate limit on {CHAT_MODEL}, falling back to {FALLBACK_MODEL}")
        r = client.chat.completions.create(model=FALLBACK_MODEL, messages=messages, max_tokens=max_tokens, temperature=temperature)
        return r.choices[0].message.content or ""

SYSTEM_PROMPT = """You are PAV1 AI, an elite gaming assistant for the PAV1 gaming platform.
You are an expert on Valorant, FIFA, and F1 racing games.

Your personality:
- Enthusiastic and knowledgeable, like a pro gamer friend
- Give specific, actionable advice (not generic tips)
- Use gaming terminology naturally
- Be concise but thorough — answer what's asked, nothing extra

Format responses with **bold headers** and bullet points when listing multiple items.
Reference specific agents, weapons, formations, or circuits when relevant."""


def _detect_intent(message: str) -> str:
    msg = message.lower()
    if any(w in msg for w in ["vs", "versus", "compare", "difference between", "better", "or "]):
        return "compare"
    if any(w in msg for w in ["build", "loadout", "setup", "recommend", "best for", "which should"]):
        return "build"
    return "search"


def _smart_search(message: str, game: str) -> tuple[list, str]:
    """Search RAG intelligently based on query intent. Returns (results, tool_name)."""
    intent = _detect_intent(message)
    game_filter = game if game != "all" else None

    if intent == "compare":
        # Search for both items mentioned
        results = search_knowledge(message, game_filter=game_filter, n_results=4)
        return results, "compare_options"

    if intent == "build":
        r1 = search_knowledge(message, game_filter=game_filter, n_results=3)
        # Also search for meta/tier context
        r2 = search_knowledge(f"{game} best meta tier list", game_filter=game_filter, n_results=2)
        seen, merged = set(), []
        for r in r1 + r2:
            if r["content"] not in seen:
                seen.add(r["content"])
                merged.append(r)
        return merged[:4], "get_build_recommendation"

    # General search
    results = search_knowledge(message, game_filter=game_filter, n_results=4)
    return results, "search_game_knowledge"


def chat_with_agent(messages: list[dict], game_context: str = "all") -> dict:
    last_user_msg = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user_msg = m["content"]
            break

    # Search knowledge base
    rag_results, tool_name = _smart_search(last_user_msg, game_context)

    tools_used = []
    rag_context = ""

    if rag_results:
        tools_used = [{"tool": tool_name, "input": {"query": last_user_msg, "game": game_context}}]
        chunks = []
        for r in rag_results:
            meta = r.get("metadata", {})
            game_tag = meta.get("game", "").upper()
            cat = meta.get("category", "")
            chunks.append(f"[{game_tag} — {cat}]\n{r['content']}")
        rag_context = "\n\n---\n\n".join(chunks)

    # Build system prompt with retrieved context
    system = SYSTEM_PROMPT
    if game_context != "all":
        system += f"\n\nCurrent game context: {game_context.upper()}. Focus responses on this game."
    if rag_context:
        system += f"\n\n## Retrieved Knowledge Base\n{rag_context}"

    openai_messages = [{"role": "system", "content": system}] + messages

    response = _chat(openai_messages, max_tokens=2048, temperature=0.5)

    return {
        "response": response or "Sorry, I could not generate a response.",
        "tools_used": tools_used
    }
