"""
FastAPI application for Loan Approval System
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.config import settings
from src.utils import get_logger

app = FastAPI(
    title="Loan Approval System",
    description="Multi-Agent Agentic AI for automated loan decisions",
    version="1.0.0",
)

logger = get_logger("api")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Loan Approval System",
        "version": "1.0.0",
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Loan Approval System API",
        "docs": "/docs",
        "version": "1.0.0",
    }


# Import routes after app definition to avoid circular imports
from src.api.routes import loans, decisions

app.include_router(loans.router, prefix="/api/v1", tags=["Loans"])
app.include_router(decisions.router, prefix="/api/v1", tags=["Decisions"])


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower(),
    )
