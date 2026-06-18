from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
import json
import uvicorn

from rag import ingest_all_data, search_knowledge, get_document_count
from agent import chat_with_agent
from database import init_db, get_db, PlayerSession
from analyzer import analyze_gameplay, extract_stats_from_image, get_grade
from sqlalchemy.orm import Session

app = FastAPI(title="PAV1 AI Gaming Assistant", version="2.0.0")

DEFAULT_STATS = {
    "valorant": {"agent": "Jett", "map": "Bind", "kills": 15, "deaths": 10,
                 "assists": 5, "headshot_pct": 25, "rounds_won": 13, "rounds_lost": 9,
                 "economy_score": 65, "first_bloods": 2},
    "fifa":     {"formation": "4-3-3", "match_result": "Win", "goals": 2,
                 "goals_conceded": 1, "shots_on_target": 6, "pass_accuracy": 80,
                 "possession_pct": 52, "game_mode": "FUT"},
    "f1":       {"team": "McLaren", "circuit": "Silverstone", "qualifying_position": 5,
                 "finish_position": 4, "pit_stops": 2, "tyre_strategy": "Soft → Medium",
                 "clean_laps_pct": 88, "fastest_lap": False},
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


# ── Models ─────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []
    game: Optional[str] = "all"

class SearchRequest(BaseModel):
    query: str
    game: Optional[str] = "all"
    num_results: Optional[int] = 4

class AnalyzeRequest(BaseModel):
    username: str
    game: str
    stats: dict


# ── Startup ─────────────────────────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    init_db()
    print("Indexing game knowledge base...")
    count = ingest_all_data()
    print(f"Ready. {count} documents indexed.")


# ── Static ──────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    index = os.path.join(frontend_path, "index.html")
    if os.path.exists(index):
        return FileResponse(index)
    return {"message": "PAV1 AI Gaming Assistant v2.0", "docs": "/docs"}


# ── Health ──────────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    stats = get_document_count()
    return {"status": "ok", "knowledge_base": stats, "games_supported": ["valorant", "fifa", "f1"]}


# ── Gameplay Analysis ───────────────────────────────────────────────────────

@app.post("/api/analyze")
async def analyze(req: AnalyzeRequest, db: Session = Depends(get_db)):
    if req.game not in ("valorant", "fifa", "f1"):
        raise HTTPException(status_code=400, detail="Invalid game. Choose: valorant, fifa, f1")
    if not req.username.strip():
        raise HTTPException(status_code=400, detail="Username required")

    result = analyze_gameplay(req.username.strip(), req.game, req.stats)

    session = PlayerSession(
        username=req.username.strip(),
        game=req.game,
        stats_json=json.dumps(req.stats),
        analysis_json=json.dumps(result["analysis"]),
        performance_score=result["score"]
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    result["session_id"] = session.id
    return result


@app.post("/api/analyze/image")
async def analyze_image(
    username: str = Form(...),
    game: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if game not in ("valorant", "fifa", "f1"):
        raise HTTPException(status_code=400, detail="Invalid game")

    image_bytes = await file.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image too large (max 10MB)")

    extracted = extract_stats_from_image(image_bytes, game)
    stats_source = "screenshot"
    if not extracted:
        # Vision extraction failed — fall back to defaults and still run analysis
        extracted = DEFAULT_STATS.get(game, {})
        stats_source = "default"

    result = analyze_gameplay(username.strip(), game, extracted)
    result["stats_source"] = stats_source

    session = PlayerSession(
        username=username.strip(),
        game=game,
        stats_json=json.dumps(extracted),
        analysis_json=json.dumps(result["analysis"]),
        performance_score=result["score"]
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    result["session_id"] = session.id
    return result


# ── History & Progress ──────────────────────────────────────────────────────

@app.get("/api/history/{username}")
async def history(username: str, game: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(PlayerSession).filter(PlayerSession.username == username)
    if game and game != "all":
        query = query.filter(PlayerSession.game == game)
    sessions = query.order_by(PlayerSession.created_at.desc()).limit(20).all()

    result = []
    for s in sessions:
        analysis = json.loads(s.analysis_json)
        result.append({
            "id": s.id,
            "game": s.game,
            "score": s.performance_score,
            "grade": get_grade(s.performance_score),
            "summary": analysis.get("summary", "")[:150],
            "stats": json.loads(s.stats_json),
            "analysis": analysis,
            "created_at": s.created_at.isoformat()
        })
    return result


@app.get("/api/progress/{username}")
async def progress(username: str, game: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(PlayerSession).filter(PlayerSession.username == username)
    if game and game != "all":
        query = query.filter(PlayerSession.game == game)
    sessions = query.order_by(PlayerSession.created_at.asc()).limit(20).all()

    if not sessions:
        return {"sessions": [], "avg_score": 0, "improvement": 0, "total_sessions": 0, "best_score": 0}

    data = [
        {"date": s.created_at.strftime("%b %d"), "score": s.performance_score, "game": s.game}
        for s in sessions
    ]
    scores = [s.performance_score for s in sessions]
    avg = round(sum(scores) / len(scores), 1)
    best = round(max(scores), 1)

    improvement = 0
    if len(sessions) >= 2:
        recent = scores[-min(3, len(scores)):]
        early = scores[:min(3, len(scores))]
        improvement = round(sum(recent) / len(recent) - sum(early) / len(early), 1)

    return {
        "sessions": data,
        "avg_score": avg,
        "best_score": best,
        "improvement": improvement,
        "total_sessions": len(sessions)
    }


# ── Chat ─────────────────────────────────────────────────────────────────────

@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    messages = []
    for turn in req.history[-10:]:
        if turn.get("role") in ("user", "assistant") and turn.get("content"):
            messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": req.message})

    try:
        result = chat_with_agent(messages=messages, game_context=req.game or "all")
    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}\n{traceback.format_exc()}")

    return {"response": result["response"], "tools_used": result["tools_used"], "game": req.game}


@app.post("/api/search")
async def search(req: SearchRequest):
    results = search_knowledge(
        query=req.query,
        game_filter=req.game if req.game != "all" else None,
        n_results=req.num_results
    )
    return {"query": req.query, "game": req.game, "results": results}


@app.get("/api/quick-tips/{game}")
async def quick_tips(game: str):
    if game not in ("valorant", "fifa", "f1"):
        raise HTTPException(status_code=404, detail="Game not found")
    messages = [{"role": "user", "content": f"Give me 5 essential quick tips for {game} in bullet points. Keep each tip to 1-2 lines."}]
    result = chat_with_agent(messages=messages, game_context=game)
    return {"game": game, "tips": result["response"]}


@app.post("/api/ingest")
async def reingest():
    count = ingest_all_data()
    stats = get_document_count()
    return {"message": "Re-indexed successfully", "total": count, "by_game": stats["by_game"]}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
