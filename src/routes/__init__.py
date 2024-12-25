from fastapi import APIRouter, Depends
from src.routes.auth import authenticate_request

router = APIRouter(
    dependencies=[Depends(authenticate_request)],
)
