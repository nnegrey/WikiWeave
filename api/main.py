from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import wiki

app = FastAPI(
    title="WikiWeave API",
    description="API for generating evolutionary paths between Wikipedia articles",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(wiki.router, prefix="/api/v1", tags=["wiki"])
