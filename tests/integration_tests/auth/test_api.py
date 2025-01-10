# import pytest
#
# @pytest.mark.parametrize("email, password, status_code", [
#     ("katenka@sup.ru","124345",200),
#     ("katenkaa@sup.ru","Pumpkins22",200)
# ])
# async def full_auth_test(
#         email,
#         password,
#         status_code,
#         ac
# ):
#
#     response = await ac.post(
#         "/auth/register",
#         json={
#             "email":email,
#             "password": password
#         }
#     )
#
#     assert response.status_code == status_code
#
#     res = response.json()
#     print(f"{res=}")
#     print("22")
#     assert isinstance(res, dict)
#     assert res["status"] == "ok"
#
#
#
#     response_login = await ac.post(
#         "/auth/login",
#         json={
#             "email":email,
#             "password": password
#         }
#     )
#
#     assert response_login.status_code == status_code
#
#     res = response_login.json()
#     print(f"{res=}")
#     assert isinstance(res, dict)
#     assert ac.cookies["access_token"]
#     assert res["access_token"]
#
#
#
#
#     response_me = await ac.me("/auth/me")
#     assert response_me.status_code == status_code
#
#     res = response_me.json()
#     print(f"{res=}")
#     # assert isinstance(res, dict)
#     assert res["id"]
#     assert res["email"] == email
#     assert "password" not in res
#
#
#
#     response_logout = await ac.post(
#         "/auth/logout",
#         json={
#             "email":email,
#             "password": password
#         }
#     )
#
#     assert response_logout.status_code == status_code
#     res = response.json()
#     print(f"{res=}")
#     assert isinstance(res, dict)
#     assert res["status"] == "ok"
#     assert "access_token" not in ac.cookies
#
#
#
#
#
#     response_me = await ac.me("/auth/me")
#     assert response_me.status_code == 500
#
#     res = response_me.json()
#     print(f"{res=}")
#     # assert isinstance(res, dict)
#     assert res["id"]
#

import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("k0t@pes.com", "1234", 200),
    ("k0t@pes.com", "1234", 400),
    ("k0t1@pes.com", "1235", 200),
    ("abcde", "1235", 422),
    ("abcde@abc", "1235", 422),
])
async def test_auth_flow(email: str, password: str, status_code: int, ac):
    # /register
    resp_register = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        }
    )
    assert resp_register.status_code == status_code
    if status_code != 200:
        return

    # /login
    resp_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        }
    )
    assert resp_login.status_code == 200
    assert ac.cookies["access_token"]
    assert "access_token" in resp_login.json()

    # /me
    resp_me = await ac.get("/auth/me")
    assert resp_me.status_code == 200
    user = resp_me.json()
    assert user["email"] == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    # /logout
    resp_logout = await ac.post("/auth/logout")
    assert resp_logout.status_code == 200
    assert "access_token" not in ac.cookies