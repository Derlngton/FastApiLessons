from pydantic import BaseModel, Field, ConfigDict


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int



class RoomAdd(RoomAddRequest):
    hotel_id: int


class Room(RoomAdd):
    id:int


    model_config = ConfigDict(from_attributes=True)



class RoomPatchRequest(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)


class RoomPatch(RoomPatchRequest):
    hotel_id: int
