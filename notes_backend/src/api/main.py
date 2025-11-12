from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes_notes import router as notes_router

openapi_tags = [
    {
        "name": "Health",
        "description": "Health and diagnostics endpoints",
    },
    {
        "name": "Notes",
        "description": "CRUD operations for managing notes",
    },
]

app = FastAPI(
    title="Simple Notes API",
    description="A minimal FastAPI backend that supports creating, viewing, editing, and deleting notes.",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

# Allow all origins for preview/testing purposes.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PUBLIC_INTERFACE
@app.get("/", tags=["Health"], summary="Health Check")
def health_check():
    """
    Health check endpoint to verify the API is running.

    Returns:
    - dict: A simple object containing a 'message' key with 'Healthy' value.
    """
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.get("/health", tags=["Health"], summary="Health Check (alias)")
def health_check_alias():
    """
    Health check alias endpoint for readiness/liveness probes.

    Returns:
    - dict: A simple object containing a 'message' key with 'Healthy' value.
    """
    return {"message": "Healthy"}


# Register routes
app.include_router(notes_router)
