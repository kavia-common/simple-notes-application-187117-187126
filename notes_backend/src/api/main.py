from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from .routes_notes import router as notes_router

# OpenAPI tag definitions
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

# Create FastAPI application with explicit metadata
app = FastAPI(
    title="Simple Notes API",
    description="A minimal FastAPI backend that supports creating, viewing, editing, and deleting notes.",
    version="0.1.0",
    openapi_tags=openapi_tags,
    terms_of_service="https://example.com/terms",
    contact={"name": "Notes API", "email": "support@example.com"},
    license_info={"name": "MIT"},
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Allow all origins for preview/testing purposes (suitable for ephemeral preview envs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PUBLIC_INTERFACE
@app.get("/", tags=["Health"], summary="Health Check", description="Lightweight liveness/readiness indicator. Always returns 200.")
def health_check():
    """
    Health check endpoint to verify the API is running.

    Returns:
    - dict: A simple object containing a 'message' key with 'Healthy' value.
    """
    # Keep the handler trivial and non-blocking for readiness systems
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.get("/health", tags=["Health"], summary="Health Check (alias)", description="Alias for health; designed to be fast and always 200.")
def health_check_alias():
    """
    Health check alias endpoint for readiness/liveness probes.

    Returns:
    - dict: A simple object containing a 'message' key with 'Healthy' value.
    """
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.head(
    "/docs",
    tags=["Health"],
    summary="Docs readiness (HEAD)",
)
def docs_head() -> Response:
    """
    Responds OK to HEAD /docs for readiness checks in environments that probe the docs path.
    Does not render the docs page, only returns 200 OK to indicate the app is responsive.
    """
    # Avoid heavy rendering; just return 200 OK with no body
    return Response(status_code=200)


# Register routes
app.include_router(notes_router)
