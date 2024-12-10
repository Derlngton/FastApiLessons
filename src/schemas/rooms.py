from pydantic import BaseModel, Field, ConfigDict


class RoomAdd(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int
    hotel_id: int



class Room(RoomAdd):
    id:int


    model_config = ConfigDict(from_attributes=True)



class RoomPATCH(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)



class RoomPut(BaseModel):
    title: str
    description: str
    price: int
    quantity: int