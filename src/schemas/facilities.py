from pydantic import BaseModel, Field, ConfigDict

class FacilityAdd(BaseModel):
    title: str


class Facility(FacilityAdd):
    id:int

    model_config = ConfigDict(from_attributes=True)



# class RoomPatchRequest(BaseModel):
#     title: str | None = Field(None)
#     description: str | None = Field(None)
#     price: int | None = Field(None)
#     quantity: int | None = Field(None)
#
#
# class RoomPatch(RoomPatchRequest):
#     hotel_id: int
