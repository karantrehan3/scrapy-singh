from fastapi import FastAPI
from pydantic import BaseModel
from src.routes import router

app = FastAPI()


class HealthCheckResponse(BaseModel):
    ok: bool
    message: str


@app.get(
    "/health",
    summary="Health Check",
    description="Health Check API",
    response_model=HealthCheckResponse,
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {"example": {"ok": True, "message": "Burrah!"}}
            },
        },
    },
)
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(ok=True, message="Burrah!")


app.include_router(router)
