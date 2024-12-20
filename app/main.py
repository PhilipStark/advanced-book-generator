from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import books, events, generator
from .database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Generator API",
    description="AI-powered book generation service with advanced capabilities",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(books.router)
app.include_router(events.router)
app.include_router(generator.router)

@app.get("/")
async def root():
    return {
        "message": "Advanced Book Generator API is running",
        "version": "1.0.0",
        "features": [
            "Advanced AI Generation",
            "Quality Analysis",
            "Content Refinement",
            "Multi-Model Pipeline"
        ]
    }