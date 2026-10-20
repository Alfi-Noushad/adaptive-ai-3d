from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from mesh.utils.response import success_response, error_response
from mesh.api.routes_analysis import router as analysis_router
from mesh.api.routes_repair import router as repair_router
from mesh.api.routes_optimize import router as optimize_router




app = FastAPI(title="Mesh Layer", version="0.1.0")

app.include_router(analysis_router)
app.include_router(repair_router)
app.include_router(optimize_router)


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=error_response("Invalid request", error=exc.errors()),
    )


@app.exception_handler(StarletteHTTPException)
async def http_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(str(exc.detail)),
    )


@app.exception_handler(Exception)
async def unhandled_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=error_response("Internal mesh service error", error=str(exc)),
    )


@app.get("/health")
def health():
    return success_response({"service": "mesh"}, "Mesh layer is up")