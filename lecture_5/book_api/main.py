from fastapi import FastAPI
from .routers.book_router import router
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)