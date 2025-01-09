import pytest

from src.database import engine_null_pull, Base, async_session_maker_null_pull
from src.utils.db_manager import DBManager


# параметризированный тест
@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1,"2024-08-01","2024-08-10", 200),
    (1,"2024-08-05","2024-08-12", 200),
    (1,"2024-08-03","2024-08-11", 200),
    (1,"2024-07-30","2024-08-08", 200),
    (1,"2024-08-03","2024-08-15", 200),
    (1,"2024-08-05","2024-08-09", 404),
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db,
        authenticated_ac
):

    # room_id = (await db.rooms.get_all())[0].id

    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )

    assert response.status_code == status_code

    if status_code == 200:
        res = response.json()
        # print(f"{res=}")

        assert isinstance(res, dict)
        assert res["status"] == "ok"



# @pytest.fixture(scope="session")
# async def delete_all_bookings():
#
#
#     async with (DBManager(session_factory=async_session_maker_null_pull) as db_):
#
#         for booking in range(5):
#             await db_.bookings.delete(id = booking)
#
#         await db_.commit()






@pytest.mark.parametrize("room_id, date_from, date_to, status_code, count", [
    (1,"2024-08-01","2024-08-10", 200, 1),
    (2,"2025-08-01","2025-08-10", 200, 2),
    (1,"2026-08-01","2026-08-10", 200, 3),
    (2,"2027-08-01","2027-08-10", 200, 4),
])
async def test_add_and_get_my_bookings(
        delete_all_bookings,
        room_id, date_from, date_to, status_code, count,
        db,
        authenticated_ac
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )

    assert response.status_code == status_code

    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "ok"




    response_me = await authenticated_ac.get("/bookings/me",
                                             params={
                                                 "per_page":5
                                             })

    # c = len(response_me.json())
    # print(c)


    assert response_me.status_code == status_code
    if status_code == 200:
        res = response_me.json()
        assert isinstance(res, list)
        assert len(res) == count

