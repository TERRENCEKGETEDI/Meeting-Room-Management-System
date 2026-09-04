import pytest
from fastapi import Depends
from app.database.dependencies import get_db
from app.services.rooms import delete_room_services


@pytest.mark.asyncio
async def test_delete_room():
    session = Depends(get_db)
    message = await delete_room_services(10,session)
    assert message["message"] == "Room deleted"