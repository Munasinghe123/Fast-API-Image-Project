from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import threading

from routes.survey_routes import router as survey_router
from publish.publish_engine import run_publish_engine
from config.db_config import test_db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")

    test_db_connection()

    #  Start background publish engine
    thread = threading.Thread(
        target=run_publish_engine,
        daemon=True
    )
    thread.start()

    yield   #  app runs here

    print(" Application shutting down...")


app = FastAPI(
    title="Drone Image Management API",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(survey_router, prefix="/survey")


# Health
@app.get("/health")
def health():
    return {"status": "ok"}