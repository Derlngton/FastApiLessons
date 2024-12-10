from fastapi import Query, APIRouter, Body


from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import Room, RoomAdd, RoomPATCH, RoomPut

router_rooms = APIRouter(prefix="/hotels", tags=["Rooms"])



@router_rooms.post("/rooms", summary="Добавление номера")
async def create_room(room_data: RoomAdd = Body(
    openapi_examples={
    "1":{"summary": "Лакшери", "value": {
        "title" : "Лакшерус",
        "description" : "Ого, вот это номер",
        "price" : 1000000,
        "quantity" : 5,
        "hotel_id" : 2
    }},
    "2":{"summary": "Одиночный", "value": {
        "title" : "Одноместный",
        "description" : "Для бедолаг",
        "price" : 1000,
        "quantity" : 5,
        "hotel_id" : 6
    }},
    })
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(data=room_data)
        await session.commit()

    return {"status": "ok", "data": room}




@router_rooms.get("/{hotel_id}/rooms", summary="Получение номеров в отеле")
async def get_rooms(
        hotel_id: int,
        title: str | None = Query(None, description="Название номера"),
        min_price: int | None = Query(None, description="Минимальная цена"),
        max_price: int | None = Query(None, description="Максимальная цена")
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id = hotel_id,
            title=title,
            min_price=min_price,
            max_price=max_price
        )



@router_rooms.get("/{hotel_id}/rooms/{room_id}", summary="Получение конкретного номера в отеле")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)




@router_rooms.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "ok"}



#
@router_rooms.put("/{hotel_id}/rooms/{room_id}", summary="Полное обновление данных о номере")
async def put_hotel(hotel_id: int, room_id:int, room_data: RoomPut):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).update(room_data, id=room_id, hotel_id= hotel_id)
        await session.commit()

    return {"status": "ok", "data": room}




@router_rooms.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление данных о номере",
           description="В отличии от ручки PUT, тут можно отправлять по одному параметру")
async def patch_hotel(hotel_id: int, room_id:int, room_data: RoomPATCH):

    async with async_session_maker() as session:
        room = await RoomsRepository(session).update(room_data, is_patch=True, id=room_id, hotel_id= hotel_id)
        await session.commit()

    return {"status": "ok", "data": room}