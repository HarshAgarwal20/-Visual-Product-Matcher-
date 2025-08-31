# backend/populate_db.py
import os
import json
from database import SessionLocal
from models import Image
from embeddings import get_embedding

UPLOAD_DIR = "uploads"
db = SessionLocal()

def populate():
    supported = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")
    files = sorted([f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith(supported)])
    inserted = 0
    for fn in files:
        if fn.startswith("query_"):
            continue
        existing = db.query(Image).filter(Image.filename == fn).first()
        if existing:
            print(f"Skipping (exists): {fn}")
            continue
        path = os.path.join(UPLOAD_DIR, fn)
        print(f"Processing: {fn}")
        emb = get_embedding(path)
        rec = Image(filename=fn, embedding=json.dumps(emb.tolist()))
        db.add(rec)
        db.commit()
        inserted += 1
    db.close()
    print(f"Done. Inserted {inserted} images.")

if __name__ == "__main__":
    populate()
