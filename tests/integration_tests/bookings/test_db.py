from datetime import date

from src.schemas.bookings import BookingAdd

async def test_booking_crud(db):

    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    booking_data = BookingAdd(
        date_from=date(year=2025, month=8, day=28),
        date_to=date(year=2025, month=9, day=1),
        room_id=room_id,
        price = 100,
        user_id=user_id
    )

    booking = await db.bookings.add(booking_data)

    booking = await db.bookings.get_one_or_none(id = booking.id)
    assert booking
    print(f"{booking=}")


    new_booking_data = BookingAdd(
        date_from=date(year=2025, month=10, day=8),
        date_to=date(year=2025, month=10, day=11),
        room_id=room_id,
        price=100,
        user_id=user_id
    )


    update_booking = await db.bookings.update(new_booking_data, id = booking.id)
    assert update_booking
    assert update_booking.id == booking.id
    assert update_booking.date_from == new_booking_data.date_from
    print(f"{update_booking=}")



    await db.bookings.delete(id = booking.id)
    deleted_booking = await db.bookings.get_one_or_none(id=booking.id)
    assert deleted_booking is None

    await db.commit()