from typing import Annotated

from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH
from src.database import async_session_maker, engine
from src.repositories.hotels import HotelsRepository



router_hotels = APIRouter(prefix="/hotels", tags=["Hotels"])



@router_hotels.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Расположение отеля")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )





@router_hotels.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()


    return {"status": "ok", "data": hotel}





@router_hotels.post("")
async def create_hotel(hotel_data: Hotel = Body(
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
    async with async_session_maker() as session:
        # await HotelsRepository(session).add(data=hotel_data)
        hotel = await HotelsRepository(session).add(data=hotel_data)
        # hotel = await HotelsRepository(session).get_one_or_none(**hotel_data.model_dump())
        await session.commit()

    return {"status": "ok", "data": hotel}




@router_hotels.put("/{hotel_id}", summary="Полное обновление данных об отеле")
async def put_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).full_update(id=hotel_id,data=hotel_data)
        await session.commit()

    return {"status": "ok", "data": hotel}



@router_hotels.patch("/{hotel_id}", summary="Частичное обновление данных об отеле",
           description="Частичное обновление данных об отеле, в отличии от ручки PUT, тут можно отправлять по одному параметру")
async def patch_hotel( hotel_id: int, hotel_data: HotelPATCH):

    global hotels

    if hotel_data.title != None:
        hotels[hotel_id - 1]["title"] = hotel_data.title
    elif hotel_data.name != None:
        hotels[hotel_id - 1]["name"] = hotel_data.name


    return {"status": "ok"}