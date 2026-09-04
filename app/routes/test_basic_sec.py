import asyncio
import time

from fastapi import APIRouter, Depends

from app.auth.basic_security import basic_auth

router = APIRouter(prefix="/basic", tags=["Basic Authentication"])


@router.get("/protected")
def basic_protected(username: str = Depends(basic_auth)):
    return {"message": "Basic authentication successful", "username": username}


@router.get("/test-sync")
def test_sync():
    time.sleep(5)
    return {"message": "done"}
@router.get("/test-sync2")
def test_sync2():
    time.sleep(5)
    return {"message": "done"}

@router.get("/test-async")
async def test_async():
    await asyncio.sleep(5)
    return {"message": "done"}
@router.get("/test-async2")
async def test_async2():
    await asyncio.sleep(5)
    return {"message": "done"}

@router.get("/bad-async")
async def bad_async():
    time.sleep(5)
    return {"message": "done"}


@router.get("/good-async")
async def good_async():
    await asyncio.sleep(5)
    return {"message": "done"}