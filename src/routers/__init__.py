from fastapi import APIRouter, Depends, HTTPException
from .auth import authenticateRequest

router = APIRouter(
    dependencies=[Depends(authenticateRequest)],
)
