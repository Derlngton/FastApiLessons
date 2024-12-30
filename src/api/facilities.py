# import json

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.tasks.tasks import test_task


router_facilities = APIRouter(prefix="/facilities", tags=["Facilities"])


@router_facilities.get("")
@cache(expire=10)
async def get_all_facilities(db: DBDep):
    # оставил код для понимания всяких джсон дампов и т.п
    # facilities_from_cache = await redis_manager.get("facilities")
    # # print(f"{facilities_from_cache=}")
    # if not facilities_from_cache:
    #     facilities = await db.facilities.get_all()
    #     facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
    #     facilities_json = json.dumps(facilities_schemas)
    #
    #     await redis_manager.set("facilities", facilities_json, 10)
    #
    #     return facilities
    # else:
    #     facilities_dicts = json.loads(facilities_from_cache)
    #     return facilities_dicts
    return await db.facilities.get_all()



@router_facilities.post("")
async def add_facilities(
        db: DBDep,
        facility_data: FacilityAdd
):
    facility = await db.facilities.add(data=facility_data)
    await db.commit()

    test_task.delay()

    return {"status": "ok", "data": facility}
