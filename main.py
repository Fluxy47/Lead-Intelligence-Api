from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from exceptions import AppError
from models import ErrorResponse, FieldError
from routes import router

app = FastAPI(title="Lead Intelligence API", version="0.2.0")
app.include_router(router)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    body = ErrorResponse(error_code=exc.error_code, message=exc.message)
    return JSONResponse(status_code=exc.status_code, content=body.model_dump())


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    details = [
        FieldError(
            field=".".join(str(part) for part in err["loc"] if part != "body"),
            message=err["msg"],
        )
        for err in exc.errors()
    ]
    body = ErrorResponse(
        error_code="VALIDATION_ERROR",
        message="Request validation failed.",
        details=details,
    )
    return JSONResponse(status_code=422, content=body.model_dump())


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    body = ErrorResponse(
        error_code="INTERNAL_ERROR",
        message="Something went wrong on our side.",
    )
    return JSONResponse(status_code=500, content=body.model_dump())