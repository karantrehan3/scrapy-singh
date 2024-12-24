from fastapi import Header, HTTPException, status
from typing_extensions import Annotated


async def authenticateRequest(Authorization: Annotated[str, Header()]):
    if Authorization != "fake-super-secret-token":
        raise HTTPException(
            status_code=status.HTTP_401, detail="Authorization header invalid"
        )
