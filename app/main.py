"""
FastAPI Application Factory for APEX Revenue SDR OS
Follows Team Architectural Invariants (App Factory Pattern).
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.webhook import router as webhook_router
from app.routers.sandbox_ui import router as sandbox_ui_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.main")

def create_app() -> FastAPI:
    """Application factory pattern"""
    app = FastAPI(
        title="APEX Revenue SDR OS API",
        description="Zero-Trust Conversational Autonomous SDR Operating System",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # CORS Configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register Routers
    app.include_router(webhook_router)
    app.include_router(sandbox_ui_router)


    @app.get("/healthz", tags=["System"])
    async def health_check():
        return {
            "status": "healthy",
            "service": "APEX Revenue SDR OS Engine",
            "zapi_instance": "3F7CDA470843917372BC9E4132DEE0C8"
        }

    return app

app = create_app()
