from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    location: str


class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)

# class HotelGET(BaseModel):
#     title: str | None = Field(None, description="Название отеля"),
#     location: str | None = Field(None, description="Расположение отеля")

