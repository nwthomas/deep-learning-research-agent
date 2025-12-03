from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import app_config
from app.errors import CustomError


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Hook into the application lifecycle for logging and custom logic. Run on startup and shutdown.

    Args:
        _app (FastAPI): The FastAPI app

    Returns:
        AsyncGenerator[None, None]: The lifespan generator
    """

    print(f"Starting {app_config.APP_NAME}")
    yield
    print(f"Shutting down {app_config.APP_NAME}")


app = FastAPI(
    title="Deep Learning Research Agent API",
    description="A deep learning research agent API",
    version=app_config.APP_VERSION,
    lifespan=lifespan,
    debug=app_config.APP_DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    # TODO: Update with variables from config for development and production environments
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic validation errors with a consistent format.

    Args:
        _request (Request): The request that caused the validation error
        exc (RequestValidationError): The validation error

    Returns:
        JSONResponse: The JSON response with the validation error
    """

    return JSONResponse(
        status_code=422,
        content={
            "detail": [
                {
                    "message": error["msg"],
                    "code": "VALIDATION_ERROR",
                    "field": (".".join(str(loc) for loc in error["loc"]) if error.get("loc") else None),
                }
                for error in exc.errors()
            ]
        },
    )


@app.exception_handler(CustomError)
async def custom_exception_handler(_request: Request, exc: CustomError) -> JSONResponse:
    """Handle custom application errors.

    Args:
        _request (Request): The request that caused the custom error
        exc (CustomError): The custom error

    Returns:
        JSONResponse: The JSON response with the custom error
    """

    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def global_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
    """Handle unexpected errors with consistent format.

    Args:
        _request (Request): The request that caused the error
        _exc (Exception): The unexpected error

    Returns:
        JSONResponse: The JSON response with the unexpected error
    """

    return JSONResponse(
        status_code=500,
        content={
            "detail": [
                {
                    "message": "An internal server error occurred",
                    "code": "INTERNAL_ERROR",
                    "field": None,
                }
            ]
        },
    )


@app.get("/health")
async def health_check() -> JSONResponse:
    """Health check endpoint.

    Returns:
        JSONResponse: The health check response
    """

    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": app_config.APP_NAME,
        },
    )
