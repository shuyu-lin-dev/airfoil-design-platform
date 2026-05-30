from fastapi import FastAPI

app = FastAPI(title="Airfoil Design Platform", version="0.2.0")


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.2.0"}
