from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from airfoil_platform.api import geometry, artifacts, aerodynamics, structure, optimization, teaching

app = FastAPI(title="Airfoil Design Platform", version="0.1.0")

app.include_router(geometry.router)
app.include_router(artifacts.router)
app.include_router(aerodynamics.router)
app.include_router(structure.router)
app.include_router(optimization.router)
app.include_router(teaching.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    messages = []
    for error in exc.errors():
        loc = " -> ".join(str(p) for p in error["loc"])
        messages.append(f"{loc}: {error['msg']}")
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "; ".join(messages),
                "resolution": "请根据上述校验详情修正请求参数后重试。",
            }
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
