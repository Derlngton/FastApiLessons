from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache


from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd


router_hotels = APIRouter(prefix="/hotels", tags=["Hotels"])



@router_hotels.get("")
# @cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Расположение отеля"),
        date_from: date = Query(example="2025-01-08"),
        date_to: date = Query(example="2025-01-01")
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
        date_from=date_from,
        date_to=date_to
        )



@router_hotels.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)



@router_hotels.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "ok"}



@router_hotels.post("")
async def create_hotel(db: DBDep,
                       hotel_data: HotelAdd = Body(
    openapi_examples={
    "1":{"summary": "Сочи", "value": {
        "title" : "Отель Сочи 5 звезд",
        "location" : "Сочи, улица Отелей 5"
    }},
    "2":{"summary": "Дубай", "value": {
        "title" : "Отель Дубай плаза",
        "location" : "Дубай, улица Арабская 8"
    }}
    })
):
    hotel = await db.hotels.add(data=hotel_data)
    await db.commit()
    return {"status": "ok", "data": hotel}



@router_hotels.put("/{hotel_id}", summary="Полное обновление данных об отеле")
async def put_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    hotel = await db.hotels.update(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "ok", "data": hotel}



@router_hotels.patch("/{hotel_id}", summary="Частичное обновление данных об отеле",
           description="Частичное обновление данных об отеле, в отличии от ручки PUT, тут можно отправлять по одному параметру")
async def patch_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPATCH):
    hotel = await db.hotels.update(hotel_data, is_patch=True, id=hotel_id)
    await db.commit()
    return {"status": "ok", "data": hotel}