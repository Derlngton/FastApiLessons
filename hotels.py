from typing import Annotated

from fastapi import Query, APIRouter, Body

from dependencies import PaginationDep
from schemas.hotels import Hotel, HotelPATCH



hotels = [
    {"id": 1, "title": "Sochi","name": "sochi"},
    {"id": 2, "title": "Dubai","name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]



router_hotels = APIRouter(prefix="/hotels", tags=["Hotels"])




@router_hotels.get("")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
        name: str | None = Query(None, description="Название отеля"),
        # page:int | None = Query(1, description="Выбранная страница", gt=0),
        # per_page: int| None = Query(3, description="Кол-во отелей на странице", gt=0, lt=20)
):

    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        if name and hotel["name"] != name:
            continue
        hotels_.append(hotel)


    first_hotel= pagination.per_page * (pagination.page - 1)

    return hotels_[first_hotel: first_hotel + pagination.per_page]



@router_hotels.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}





@router_hotels.post("")
def create_hotel(hotel_data: Hotel = Body(
    openapi_examples={
    "1":{"summary": "Сочи", "value": {
        "title" : "Отель Сочи 5 звезд",
        "name" : "sochi_5_zvezd"
    }},
    "2":{"summary": "Дубай", "value": {
        "title" : "Отель Дубай плаза",
        "name" : "dubai_plaza"
    }}
    })
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
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