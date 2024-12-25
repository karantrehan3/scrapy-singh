from fastapi import APIRouter, Depends
from src.routes.auth import authenticate_request
from src.routes.scrape import scrape_router

router = APIRouter(
    dependencies=[Depends(authenticate_request)],
)
router.include_router(scrape_router)
