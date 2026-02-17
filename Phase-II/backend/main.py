from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from db import create_db_and_tables, engine
from models import Task

# Load environment variables
load_dotenv()

# Get configuration from environment
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# =============================================================================
# Create FastAPI Application
# =============================================================================

app = FastAPI(
    title="Todo App Backend API",
    description="REST API for Todo App with JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# =============================================================================
# CORS Configuration
# =============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=600,
)

# =============================================================================
# Exception Handlers
# =============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handle HTTP exceptions with consistent error format."""
    error_code = "INTERNAL_ERROR"
    if exc.status_code == 401:
        error_code = "UNAUTHORIZED"
    elif exc.status_code == 403:
        error_code = "FORBIDDEN"
    elif exc.status_code == 404:
        error_code = "NOT_FOUND"
    elif exc.status_code == 422:
        error_code = "VALIDATION_ERROR"
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": error_code,
                "message": exc.detail.get("message", str(exc.detail)) if isinstance(exc.detail, dict) else str(exc.detail),
                "details": exc.detail.get("details") if isinstance(exc.detail, dict) else None
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """Handle validation errors with consistent format."""
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed",
                "details": {
                    error["loc"][0]: error["msg"]
                    for error in exc.errors()
                }
            }
        }
    )


# =============================================================================
# Lifespan Events
# =============================================================================

@app.on_event("startup")
async def on_startup():
    """Initialize database tables on startup."""
    create_db_and_tables()


# =============================================================================
# Health Check Endpoint
# =============================================================================

@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


# =============================================================================
# Include Routers
# =============================================================================

from routes.tasks import router as tasks_router

app.include_router(tasks_router)

# =============================================================================
# Root Endpoint
# =============================================================================

@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Todo App Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
