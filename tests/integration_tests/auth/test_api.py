import pytest

@pytest.mark.parametrize("email, password, status_code", [
    ("katenka@sup.ru","124345",200),
    ("katenkaa@sup.ru","Pumpkins22",200)
])
async def full_auth_test(
        email,
        password,
        status_code,
        ac
):

    response = await ac.post(
        "/auth/register",
        json={
            "email":email,
            "password": password
        }
    )

    assert response.status_code == status_code

    res = response.json()
    print(f"{res=}")
    print("22")
    assert isinstance(res, dict)
    assert res["status"] == "ok"



    response_login = await ac.post(
        "/auth/login",
        json={
            "email":email,
            "password": password
        }
    )

    assert response_login.status_code == status_code

    res = response_login.json()
    print(f"{res=}")
    assert isinstance(res, dict)
    assert res["access_token"]




    response_me = await ac.me("/auth/me")
    assert response_me.status_code == status_code

    res = response_me.json()
    print(f"{res=}")
    # assert isinstance(res, dict)
    assert res["id"]



    response_logout = await ac.post(
        "/auth/login",
        json={
            "email":email,
            "password": password
        }
    )

    assert response.status_code == status_code
    res = response.json()
    print(f"{res=}")
    assert isinstance(res, dict)
    assert res["status"] == "ok"




    response_login = await ac.me("/auth/me")
    assert response_login.status_code == 500

    res = response_login.json()
    print(f"{res=}")
    # assert isinstance(res, dict)
    assert res["id"]

