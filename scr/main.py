from fastapi import FastAPI
from scr.api.routes import router
from scr.database.connection import engine
from scr.database.models import Base

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="N-Queens Solver",
    description="API para resolver el problema de las N reinas",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")