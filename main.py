import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Host, Location, Retreat, Message, Preference

app = FastAPI(title="The Sanctuary of Nature API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "The Sanctuary of Nature Backend is alive"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "Unknown"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:100]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# ----- Basic create/list endpoints using helper functions -----

@app.post("/api/hosts", response_model=dict)
def create_host(host: Host):
    try:
        _id = create_document("host", host)
        return {"id": _id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hosts", response_model=List[dict])
def list_hosts():
    try:
        return get_documents("host")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/locations", response_model=dict)
def create_location(location: Location):
    try:
        _id = create_document("location", location)
        return {"id": _id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/locations", response_model=List[dict])
def list_locations():
    try:
        return get_documents("location")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/retreats", response_model=dict)
def create_retreat(retreat: Retreat):
    try:
        _id = create_document("retreat", retreat)
        return {"id": _id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/retreats", response_model=List[dict])
def list_retreats(nature_type: Optional[str] = None):
    try:
        filter_q = {"nature_type": nature_type} if nature_type else {}
        return get_documents("retreat", filter_q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/messages", response_model=dict)
def create_message(message: Message):
    try:
        _id = create_document("message", message)
        return {"id": _id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/messages", response_model=List[dict])
def list_messages(topic: Optional[str] = None):
    try:
        filter_q = {"topic": topic} if topic else {}
        return get_documents("message", filter_q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Simple AI-like recommendation & quiz endpoints -----

class QuizInput(BaseModel):
    energy: Optional[str] = None
    preferred_nature: Optional[str] = None
    budget: Optional[float] = None
    duration: Optional[int] = None
    goals: Optional[str] = None

@app.post("/api/recommend", response_model=dict)
def recommend(pref: QuizInput):
    """Rule-based starter recommendations (placeholder for real AI)."""
    try:
        # Build basic query
        q = {}
        if pref.preferred_nature:
            q["nature_type"] = pref.preferred_nature
        if pref.duration:
            q["duration_days"] = {"$lte": pref.duration}
        if pref.budget is not None:
            q["price_usd"] = {"$lte": pref.budget}

        retreats = get_documents("retreat", q, limit=8)

        # Lightweight guidance text
        spirit_note = ""
        if pref.energy == "calm":
            spirit_note = "The waters are still today; gentle breath and soft horizons call you."
        elif pref.energy == "transformative":
            spirit_note = "Winds of change swirl around you; trust the metamorphosis."
        elif pref.energy == "adventurous":
            spirit_note = "Peaks and tides await; your courage is the compass."
        elif pref.energy == "restorative":
            spirit_note = "Let the earth hold you; sleep, nourish, and renew."
        else:
            spirit_note = "Nature listens. Share more, and I’ll guide you further."

        return {
            "matches": retreats,
            "spirit_message": spirit_note
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/quiz", response_model=dict)
def quiz(pref: Preference):
    """Echoes back preferences and forwards to recommend."""
    try:
        return recommend(QuizInput(**pref.model_dump()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
