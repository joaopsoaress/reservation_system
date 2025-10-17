from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from backend.routers import slots
# from config.settings import DATABASE_URL, DEBUG

    # Initialize FastAPI app
app = FastAPI()

    # CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    # Tortoise ORM configuration
register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['backend.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)

    # Include routers
app.include_router(slots.router)

    # Basic root endpoint
@app.get("/")
async def root():
    return {"message": "Reservation System API"}

    # Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

    # Serve static files for frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

    # Serve frontend application
@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/index.html")