from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep, PaginationDep
from src.schemas.bookings import BookingAddRequest, BookingAdd


router_bookings = APIRouter(prefix="/bookings", tags=["Bookings"])




@router_bookings.post("")
async def create_booking(
            user_id: UserIdDep,
            db: DBDep,
            booking_data: BookingAddRequest
            = Body(
            openapi_examples={
            "1":{"summary": "Бронь 1", "value": {
                "date_from" : "2024-12-19",
                "date_to" : "2025-01-01",
                "room_id" : 7
            }},
            "2":{"summary": "Бронь 2", "value": {
                "date_from" : "2024-12-28",
                "date_to" : "2025-01-10",
                "room_id" : 7
            }}
            }
            )
):

    room = await db.rooms.get_one_or_none(id = booking_data.room_id)
    _booking_data= BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())

    booking = await db.bookings.add(data=_booking_data)
    await db.commit()

    return {"status": "ok", "data": booking}


@router_bookings.get("", summary="Получение всех броней на сервисе. Админская ручка")
async def get_bookings(pagination: PaginationDep, db: DBDep):
    per_page = pagination.per_page or 5
    return await db.bookings.get_filtered(
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router_bookings.get("/me", summary="Получение всех броней пользователя")
async def get_hotel(pagination: PaginationDep,db: DBDep, user_id: UserIdDep):
    per_page = pagination.per_page or 5
    return await db.bookings.get_filtered(
        limit=per_page,
        offset=per_page * (pagination.page - 1),
        user_id=user_id
    )
