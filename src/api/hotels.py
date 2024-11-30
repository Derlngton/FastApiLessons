from typing import Annotated

from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH
from src.database import async_session_maker, engine




router_hotels = APIRouter(prefix="/hotels", tags=["Hotels"])




@router_hotels.get("")
async def get_hotels(
        pagination: PaginationDep,
        # hotel_data: HotelGET
        # id: int | None = Query(None, description="Айдишникк"),
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Расположение отеля")
):
    per_page = pagination.per_page or 5


    async with async_session_maker() as session:

        query = select(HotelsOrm)

        if title:
            query=query.filter(HotelsOrm.title.icontains(title))
        if location:
            query=query.filter(HotelsOrm.location.icontains(location))

        query=(
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))

        result = await session.execute(query)

        # print(type(result), result)

        # hotels = result.all()
        # возвращает список кортежей из одного элемента (в кортеже объект HotelsOrm)

        hotels = result.scalars().all()
        # возвращает так же список, но из каждого кортежа берет по первому элементу
        # т.е получаем список объектов HotelsOrm

        # другие варианты получения резалт
        # first_hotel = result.first()
        # result.one_or_none()

        return hotels



@router_hotels.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}





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

        # model_dump - преобразует модель в словарь
        add_hotel_stmt = insert(HotelsOrm).values(hotel_data.model_dump())


        # для более коректного дебага какого-то конкретного запроса (вместо echo=True):
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds" : True}))

        # в уроке полученный словарь еще распаковывают ** в словарь
        # зачем? если мы уже получаем словарь
        # add_hotel_stat = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)

        await session.commit()


        return {"status": "ok"}




@router_hotels.put("/{hotel_id}", summary="Полное обновление данных об отеле")
def put_hotel(hotel_id: int, hotel_data: Hotel):

    global hotels

    hotels[hotel_id - 1]["title"] = hotel_data.title
    hotels[hotel_id - 1]["name"] = hotel_data.name

    return {"status": "ok"}



@router_hotels.patch("/{hotel_id}", summary="Частичное обновление данных об отеле",
           description="Частичное обновление данных об отеле, в отличии от ручки PUT, тут можно отправлять по одному параметру")
def patch_hotel( hotel_id: int, hotel_data: HotelPATCH):

    global hotels

    if hotel_data.title != None:
        hotels[hotel_id - 1]["title"] = hotel_data.title
    elif hotel_data.name != None:
        hotels[hotel_id - 1]["name"] = hotel_data.name


    return {"status": "ok"}