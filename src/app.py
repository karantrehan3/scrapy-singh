from fastapi import FastAPI
from routers import router

app = FastAPI()


@app.get("/health")
async def health_check():
    return {"ok": True, "message": "I'm alive!"}


app.include_router(router)
