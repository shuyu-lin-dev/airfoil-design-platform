from fastapi import FastAPI

from airfoil_platform.api.artifacts import router as artifacts_router

app = FastAPI(title="Airfoil Design Platform", version="0.2.0")
app.include_router(artifacts_router)


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.2.0"}
