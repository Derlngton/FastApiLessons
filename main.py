import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi","name": "sochi"},
    {"id": 2, "title": "Dubai","name": "dubai"},
]




@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
        name: str | None = Query(None, description="Название отеля")
):

    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_



@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True),
        name: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
    })
    return {"status": "ok"}


@app.put("/hotels/{hotel_id}", summary="Полное обновление данных об отеле")
def put_hotel(hotel_id: int,
              title: str = Body(),
              name: str = Body()
):

    global hotels

    hotels[hotel_id - 1]["title"] = title
    hotels[hotel_id - 1]["name"] = name

    return {"status": "ok"}


@app.patch("/hotels/{hotel_id}", summary="Частичное обновление данных об отеле",
           description="Частичное обновление данных об отеле, в отличии от ручки PUT, тут можно отправлять по одному параметру")
def patch_hotel(
        hotel_id: int,
        title: str | None = Body(None),
        name: str | None = Body(None)
):

    global hotels

    if title != None:
        hotels[hotel_id - 1]["title"] = title
    elif name != None:
        hotels[hotel_id - 1]["name"] = name


    return {"status": "ok"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)