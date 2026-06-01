from fastapi import FastAPI

from airfoil_platform.api.aerodynamics import router as aerodynamics_router
from airfoil_platform.api.artifacts import router as artifacts_router

app = FastAPI(title="Airfoil Design Platform", version="0.2.0")
app.include_router(artifacts_router)
app.include_router(aerodynamics_router)


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.2.0"}
