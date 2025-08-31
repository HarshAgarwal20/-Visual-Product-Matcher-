from database import SessionLocal
from models import Image
import json

db = SessionLocal()
images = db.query(Image).all()

print(f"Total images in DB: {len(images)}")
for img in images:
    embedding = json.loads(img.embedding)
    print(f"Filename: {img.filename}, Embedding length: {len(embedding)}")
