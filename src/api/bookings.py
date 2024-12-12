from fastapi import Query, APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.bookings import BookingAddRequest, BookingAdd


router_bookings = APIRouter(prefix="/bookings", tags=["Bookings"])




@router_bookings.post("/{room_id}")
async def create_booking(
            db: DBDep,
            room_id:int,
            booking_data: BookingAddRequest
            = Body(
            openapi_examples={
            "1":{"summary": "Бронь 1", "value": {
                "date_from" : "2024-12-19",
                "date_to" : "2025-01-01",
                "user_id": 1
            }},
            "2":{"summary": "Бронь 2", "value": {
                "date_from" : "2024-12-28",
                "date_to" : "2025-01-10",
                "user_id": 1
            }}
            }
            )
):

    room = await db.rooms.get_one_or_none(id = room_id)
    print(room.price)
    _booking_data= BookingAdd(room_id= room_id,price=room.price, **booking_data.model_dump())

    booking = await db.booking.add(data=_booking_data)
    await db.commit()

    return {"status": "ok", "data": booking}