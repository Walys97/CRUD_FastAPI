from fastapi import FastAPI
from .database import engine
from .database import Base
from .controllers import persona_controller
from .controllers import masivo_controller, analitica_controller, consultas_controller
from .error_handlers import register_exception_handlers


def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(title="FastAPI Persona CRUD (MySQL)", version="1.0.0")

    # Register global exception handlers (domain → HTTP)
    register_exception_handlers(app)

    @app.on_event("startup")
    def on_startup() -> None:
        # Create tables at startup (demo purpose)
        Base.metadata.create_all(bind=engine)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    # Las rutas del laboratorio van ANTES del CRUD base para que
    # /personas/reset o /personas/reporte/activos no se confundan con /personas/{persona_id}
    app.include_router(masivo_controller.router)
    app.include_router(analitica_controller.router)
    app.include_router(consultas_controller.router)
    app.include_router(persona_controller.router)
    return app


app = create_app()