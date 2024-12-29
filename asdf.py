import json


def add_hotels_and_rooms():
    hotels_data = []


    with open("tests/mock_hotels.json") as file:
        # hotels_data = list(file)
        hotels_data = json.load(file)
        # print(type(file))
        for f in hotels_data:
            print(f"{f=}")

    print(hotels_data)
    print(type(hotels_data))



add_hotels_and_rooms()