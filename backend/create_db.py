# create_db.py
from database import Base, engine
from models import Image

Base.metadata.create_all(bind=engine)
print("Database created!")
