from fastapi import FastAPI

from database import Base, engine
from routers import cats, missions


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Spy Cat API")

app.include_router(cats.router)
app.include_router(missions.router)
