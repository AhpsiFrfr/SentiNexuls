"""
SentiNexuls FastAPI Backend
Main application entry point for the SentiNexuls platform API.
Hosts on http://localhost:8000 with CORS support for frontend integration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.api_router import router as api_router

# Initialize FastAPI application
app = FastAPI(
    title="SentiNexuls API",
    description="Advanced threat intelligence and breach simulation platform for critical infrastructure",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default
        "http://localhost:5173",  # Vite default
        "http://localhost:8080",  # Alternative frontend port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "SentiNexuls API is operational",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "dashboard": "/api/v1/dashboard",
            "intel_feed": "/api/v1/intel-feed",
            "simulate": "/api/v1/simulate",
            "agents": "/api/v1/agents",
            "alerts": "/api/v1/alerts",
            "vault_settings": "/api/v1/vault-settings",
            "docs": "/docs"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "SentiNexuls API",
        "timestamp": "2025-06-05T12:00:00Z"
    }

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for API errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "status": "error"
        }
    )

if __name__ == "__main__":
    print("🚀 Starting SentiNexuls API server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 Auto-reload enabled for development")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 