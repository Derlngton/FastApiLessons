from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitieAdd


router_facilities = APIRouter(prefix="/facilities", tags=["Facilities"])


@router_facilities.get("")
async def get_all_facilities(
        db: DBDep
):
    return await db.facilities.get_all()



@router_facilities.post("")
async def add_facilities(
        db: DBDep,
        facility_data: FacilitieAdd
):
    facility = await db.facilities.add(data=facility_data)
    await db.commit()
    return {"status": "ok", "data": facility}
