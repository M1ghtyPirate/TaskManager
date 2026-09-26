from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from . import __version__
from .middleware import request_context_middleware
from .routers.tasks import router as tasks_router
from .state import AppState


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.state = AppState()
    yield


app = FastAPI(
    title="Neto AI FastAPI — теория в коде",
    version=__version__,
    lifespan=lifespan,
)

app.middleware("http")(request_context_middleware)

app.include_router(tasks_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404 and exc.detail == "Task not found" and exc.headers:
        task_id = exc.headers.get("X-Task-Id")
        if task_id is not None:
            return JSONResponse(
                status_code=404,
                content={"detail": "Task not found", "task_id": int(task_id)},
            )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/", tags=["meta"])
async def index() -> dict[str, str]:
    return {"message": "See /docs for Swagger UI, /redoc for ReDoc"}