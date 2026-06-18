import json
import base64
import os
from openai import OpenAI
from dotenv import load_dotenv
from rag import search_knowledge

load_dotenv()

client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
CHAT_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-8b-instant"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


def _chat(messages, max_tokens=1600, temperature=0.35):
    """Call Groq with automatic fallback to smaller model on rate limit."""
    from openai import RateLimitError
    try:
        resp = client.chat.completions.create(
            model=CHAT_MODEL, messages=messages,
            max_tokens=max_tokens, temperature=temperature
        )
        return resp.choices[0].message.content.strip()
    except RateLimitError:
        print(f"Rate limit on {CHAT_MODEL}, falling back to {FALLBACK_MODEL}")
        resp = client.chat.completions.create(
            model=FALLBACK_MODEL, messages=messages,
            max_tokens=max_tokens, temperature=temperature
        )
        return resp.choices[0].message.content.strip()


def get_grade(score: float) -> str:
    if score >= 90: return "S"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    if score >= 50: return "D"
    return "F"


def calculate_score(game: str, stats: dict) -> float:
    if game == "valorant":
        deaths = max(stats.get("deaths", 1), 1)
        kd = stats.get("kills", 0) / deaths
        hs = min(stats.get("headshot_pct", 0), 100)
        rw = stats.get("rounds_won", 0)
        rl = stats.get("rounds_lost", 0)
        total = rw + rl
        wr = (rw / total * 100) if total > 0 else 50
        eco = stats.get("economy_score", 60)
        score = min(kd * 20, 40) + min(hs * 0.3, 30) + min(wr * 0.2, 20) + min(eco * 0.1, 10)

    elif game == "fifa":
        goals = stats.get("goals", 0)
        conceded = stats.get("goals_conceded", 0)
        pass_acc = stats.get("pass_accuracy", 75)
        possession = stats.get("possession_pct", 50)
        shots = stats.get("shots_on_target", 0)
        score = min(goals * 7, 30) + max(0, 25 - conceded * 5) + min((pass_acc - 60) * 0.5, 20) + min(possession * 0.15, 15) + min(shots * 1.5, 10)

    elif game == "f1":
        finish = stats.get("finish_position", 10)
        qual = stats.get("qualifying_position", 10)
        clean = stats.get("clean_laps_pct", 80)
        gained = qual - finish
        fastest = 5 if stats.get("fastest_lap", False) else 0
        score = max(0, 40 - (finish - 1) * 2.5) + min(max(0, 15 + gained * 3), 30) + min(clean * 0.25, 25) + fastest

    else:
        score = 50.0

    return round(min(max(score, 0), 100), 1)


def _extract_json(text: str):
    for marker in ["```json", "```"]:
        if marker in text:
            try:
                inner = text.split(marker)[1].split("```")[0].strip()
                return json.loads(inner)
            except Exception:
                pass
    try:
        return json.loads(text)
    except Exception:
        pass
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except Exception:
            pass
    return None


def _rag_context(game: str, stats: dict) -> str:
    queries = []
    if game == "valorant":
        agent = stats.get("agent", "")
        if agent:
            queries.append(f"{agent} Valorant agent tips abilities")
        queries += ["Valorant best weapons economy ranked", "Valorant strategy tips"]
    elif game == "fifa":
        formation = stats.get("formation", "")
        if formation:
            queries.append(f"FIFA {formation} formation custom tactics")
        queries += ["FIFA FUT meta skill moves", "FIFA attacking strategy"]
    elif game == "f1":
        circuit = stats.get("circuit", "")
        if circuit:
            queries.append(f"F1 {circuit} circuit strategy setup")
        queries += ["F1 tyre strategy optimal", "F1 car setup guide"]

    chunks = []
    for q in queries[:3]:
        results = search_knowledge(q, game_filter=game, n_results=2)
        for r in results:
            chunks.append(r["content"][:350])
    return "\n\n---\n\n".join(chunks[:5])


def analyze_gameplay(username: str, game: str, stats: dict) -> dict:
    score = calculate_score(game, stats)
    grade = get_grade(score)
    context = _rag_context(game, stats)

    prompt = f"""You are PAV1 AI, an elite gaming performance coach. Analyze this player session.

Player: {username} | Game: {game.upper()} | Performance Score: {score}/100 (Grade {grade})
Stats: {json.dumps(stats, indent=2)}

Knowledge Base:
{context}

Return ONLY a JSON object (no other text):
{{
  "summary": "2-3 personalized sentences mentioning specific stats",
  "strengths": ["specific strength with stat reference", "another strength", "third strength"],
  "weaknesses": ["specific weakness with stat", "another weakness", "third weakness"],
  "improvements": [
    {{"tip": "very specific actionable advice referencing their stats", "priority": "high"}},
    {{"tip": "specific actionable advice", "priority": "high"}},
    {{"tip": "actionable advice", "priority": "medium"}},
    {{"tip": "useful tip", "priority": "medium"}}
  ],
  "weapon_recommendations": [
    {{"name": "specific weapon/formation/setup", "reason": "why it suits their playstyle"}},
    {{"name": "second pick", "reason": "complementary choice"}},
    {{"name": "third option", "reason": "situational pick"}}
  ],
  "teammate_suggestions": {{
    "your_role": "player's playstyle label (e.g. Entry Fragger, Playmaker, Defensive Anchor)",
    "needed_roles": ["role 1 that complements them", "role 2 needed"],
    "recommended": ["specific agent/archetype 1", "specific agent/archetype 2"],
    "synergy": "1-2 sentences on why these teammates complement this player's stats"
  }},
  "strategy": "4-5 sentences of strategic advice specific to their stats and patterns",
  "patch_notes_impact": "2-3 sentences on how the current meta/patch affects this playstyle"
}}"""

    raw = _chat([{"role": "user", "content": prompt}], max_tokens=1600, temperature=0.35)
    analysis = _extract_json(raw)

    if not analysis:
        analysis = {
            "summary": f"{username} scored {score}/100. Good effort — focus on the improvements below.",
            "strengths": ["Shows game awareness", "Consistent play style", "Positive stats in key areas"],
            "weaknesses": ["Room to improve key metrics", "Some areas need work"],
            "improvements": [
                {"tip": "Review your match replays to identify positioning mistakes", "priority": "high"},
                {"tip": "Practice aim training for 15 minutes before each session", "priority": "high"},
                {"tip": "Study the current meta for your game mode", "priority": "medium"},
            ],
            "weapon_recommendations": [
                {"name": "Practice Tool", "reason": "Build consistency in fundamentals first"},
            ],
            "teammate_suggestions": {
                "your_role": "Flex Player",
                "needed_roles": ["Support", "Entry Fragger"],
                "recommended": ["Sage", "Jett"],
                "synergy": "A balanced team composition will amplify your strengths."
            },
            "strategy": "Focus on consistency and reviewing your match history. Small improvements compound over time.",
            "patch_notes_impact": "Stay updated with the latest patch notes to adapt your playstyle to the meta."
        }

    return {"score": score, "grade": grade, "game": game, "stats": stats, "analysis": analysis}


def extract_stats_from_image(image_bytes: bytes, game: str) -> dict:
    b64 = base64.b64encode(image_bytes).decode()

    field_hints = {
        "valorant": "kills, deaths, assists, agent name, map name, headshot percentage, rounds won, rounds lost, ACS (average combat score), economy rating",
        "fifa": "goals scored, goals conceded, shots on target, possession percentage, pass accuracy, formation, match result",
        "f1": "finishing position, qualifying position, fastest lap time, tyre compound used, number of pit stops, gaps to other drivers, sector times"
    }

    prompt = f"""This is a {game.upper()} gameplay screenshot. Extract all visible match statistics.

Look specifically for: {field_hints.get(game, 'any visible stats')}

Return ONLY a JSON object with the stats you can read from the image.
Use snake_case keys. Use null for anything not clearly visible.
Example for Valorant: {{"kills": 18, "deaths": 8, "assists": 4, "headshot_pct": 32, "agent": "Jett", "map": "Bind", "rounds_won": 13, "rounds_lost": 7}}
Example for FIFA: {{"goals": 3, "goals_conceded": 1, "possession_pct": 58, "pass_accuracy": 84, "shots_on_target": 7, "formation": "4-3-3"}}
Example for F1: {{"finish_position": 3, "qualifying_position": 5, "fastest_lap": true, "pit_stops": 2, "clean_laps_pct": 92}}

Return ONLY the JSON."""

    try:
        resp = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                ]
            }],
            max_tokens=600
        )
        raw = resp.choices[0].message.content.strip()
        result = _extract_json(raw)
        return {k: v for k, v in (result or {}).items() if v is not None}
    except Exception as e:
        print(f"Vision extraction failed: {e}")
        return {}
