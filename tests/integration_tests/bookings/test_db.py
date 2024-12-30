from datetime import date

from src.schemas.bookings import BookingAdd



async def test_add_booking(db):

    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    booking_data = BookingAdd(
        date_from=date(year=2025, month=8, day=28),
        date_to=date(year=2025, month=9, day=1),
        room_id=room_id,
        price = 100,
        user_id=user_id
    )

    await db.bookings.add(booking_data)
    await db.commit()
