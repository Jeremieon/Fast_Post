from fastapi import FastAPI
from fastapi.response import JSONResponse
from sqlalchemy import create_engine, Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = FastAPI()

DATABASE_URL = "postgresql://postgres:password@db:5432/tesdb"

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.post("/items/")
async def create_item(name:str):
    db = SessionLocal()
    db_item = Item(name=name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return JSONResponse(content={"id": db_item.id, "name": db_item.name}, status_code=201)