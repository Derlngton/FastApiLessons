from datetime import date

from fastapi import Query, APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import Room, RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

router_rooms = APIRouter(prefix="/hotels", tags=["Rooms"])



@router_rooms.post("/{hotel_id}/rooms", summary="Добавление номера")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body(
    openapi_examples={
    "1":{"summary": "Лакшери", "value": {
        "title" : "Лакшерус",
        "description" : "Ого, вот это номер",
        "price" : 1000000,
        "quantity" : 5,
        "facilities_ids": [1, 2]
    }},
    "2":{"summary": "Одиночный", "value": {
        "title" : "Одноместный",
        "description" : "Для бедолаг",
        "price" : 1000,
        "quantity" : 5,
        "facilities_ids": [2, 3]
    }},
    })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    room = await db.rooms.add(data=_room_data)

    if room_data.facilities_ids is not None:
        rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]

        await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "ok", "data": room}




# @router_rooms.get("/{hotel_id}/rooms", summary="Получение номеров в отеле")
# async def get_rooms(
#         db: DBDep,
#         hotel_id: int,
#         title: str | None = Query(None, description="Название номера"),
#         min_price: int | None = Query(None, description="Минимальная цена"),
#         max_price: int | None = Query(None, description="Максимальная цена")
# ):
#     return await db.rooms.get_filtered(
#         hotel_id = hotel_id,
#         title=title,
#         min_price=min_price,
#         max_price=max_price
#         )


@router_rooms.get("/{hotel_id}/rooms", summary="Получение номеров в отеле")
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2025-01-08"),
        date_to: date = Query(example="2025-01-01")
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id,date_from=date_from, date_to=date_to)




@router_rooms.get("/{hotel_id}/rooms/{room_id}", summary="Получение конкретного номера в отеле")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)




@router_rooms.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "ok"}



@router_rooms.put("/{hotel_id}/rooms/{room_id}", summary="Полное обновление данных о номере")
async def put_room(db: DBDep, hotel_id: int, room_id:int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    room = await db.rooms.update(_room_data, id=room_id, hotel_id= hotel_id)

    await db.rooms_facilities.set_room_facilities(room_id = room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()

    return {"status": "ok", "data": room}




@router_rooms.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление данных о номере",
           description="В отличии от ручки PUT, тут можно отправлять по одному параметру")
async def patch_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):

    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)

    room = await db.rooms.update(_room_data, is_patch=True, id=room_id, hotel_id=hotel_id)

    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"])

    await db.commit()
    return {"status": "ok", "data": room}