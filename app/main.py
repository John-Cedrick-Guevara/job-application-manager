from fastapi import FastAPI
from app.database import Base, engine
from app.jobs import router

Base.metadata.create_all(bind=engine) 

app = FastAPI(title="Job Application Manager", description="A simple job application manager API", version="1.0.0")
app.include_router(router.router)