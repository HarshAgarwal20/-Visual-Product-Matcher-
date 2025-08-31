import os
import uuid
import json
import numpy as np
import requests
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine, Base
from models import Image as ImageModel
from embeddings import get_embedding
from PIL import Image

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    filename = os.path.basename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    emb = get_embedding(file_path)
    emb_json = json.dumps(emb.tolist())

    existing = db.query(ImageModel).filter(ImageModel.filename == filename).first()
    if existing:
        existing.embedding = emb_json
        db.add(existing)
        db.commit()
        db.refresh(existing)
        status = "updated"
    else:
        rec = ImageModel(filename=filename, embedding=emb_json)
        db.add(rec)
        db.commit()
        db.refresh(rec)
        status = "inserted"

    return {"filename": filename, "url": f"/uploads/{filename}", "status": status}


# --- File upload search ---
@app.post("/similar-file")
async def similar_file(file: UploadFile = File(...), top_k: int = 5, db: Session = Depends(get_db)):
    tmp_name = f"query_{uuid.uuid4().hex}_{os.path.basename(file.filename)}"
    tmp_path = os.path.join(UPLOAD_DIR, tmp_name)
    content = await file.read()
    with open(tmp_path, "wb") as f:
        f.write(content)

    try:
        q_emb = get_embedding(tmp_path)
    except Exception as e:
        return {"error": f"Failed to process uploaded image: {str(e)}"}
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    rows = db.query(ImageModel).all()
    results = []
    for r in rows:
        db_emb = np.array(json.loads(r.embedding), dtype=np.float32)
        score = float(np.dot(q_emb, db_emb))
        results.append({"filename": r.filename, "url": f"/uploads/{r.filename}", "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)
    return {"similar_images": results[:top_k]}


# --- URL search ---
class URLBody(BaseModel):
    url: str

@app.post("/similar-url")
async def similar_url(body: URLBody, top_k: int = 5, db: Session = Depends(get_db)):
    url = body.url
    if not url:
        return {"error": "No URL provided."}

    tmp_name = f"query_url_{uuid.uuid4().hex}.jpg"
    tmp_path = os.path.join(UPLOAD_DIR, tmp_name)

    # Download and validate image
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        with open(tmp_path, "wb") as f:
            f.write(resp.content)

        try:
            Image.open(tmp_path).verify()
        except Exception:
            return {"error": "Downloaded file is not a valid image."}

    except Exception as e:
        return {"error": f"Failed to fetch image: {str(e)}"}

    try:
        q_emb = get_embedding(tmp_path)
    except Exception as e:
        return {"error": f"Failed to process image: {str(e)}"}
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    rows = db.query(ImageModel).all()
    results = []
    for r in rows:
        db_emb = np.array(json.loads(r.embedding), dtype=np.float32)
        score = float(np.dot(q_emb, db_emb))
        results.append({"filename": r.filename, "url": f"/uploads/{r.filename}", "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)
    return {"similar_images": results[:top_k]}


@app.get("/list-db")
def list_db(db: Session = Depends(get_db)):
    rows = db.query(ImageModel).all()
    return {"count": len(rows), "images": [r.filename for r in rows]}
