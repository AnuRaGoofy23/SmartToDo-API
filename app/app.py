from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import create_db_and_tables
from app.routers import auth, tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    create_db_and_tables()
    yield
    # Shutdown

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Task Management System"}