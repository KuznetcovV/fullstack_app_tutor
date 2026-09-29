#Получение списка пользователей админом -> 200
async def test_get_users_returns_200(created_many_users, admin_client):
    response = await admin_client.get("/users/")

    assert response.status_code == 200, response.text
    assert len(response.json()) == 5

#Фильтр списка пользователей по login -> 200
async def test_get_users_with_login_filter_returns_matching(created_many_users, admin_client):
    response = await admin_client.get("/users/", params={"login": "alina"})

    assert response.status_code == 200, response.text
    assert response.json()[0]["login"] == "alina"

#Фильтр списка пользователей по email -> 200
async def test_get_users_with_email_filter_returns_matching(created_many_users, admin_client):
    response = await admin_client.get("/users/", params={"email": "maria@test.ru"})

    assert response.status_code == 200, response.text
    assert response.json()[0]["email"] == "maria@test.ru"


#Фильтр списка пользователей по role -> 200
async def test_get_users_with_role_filter_returns_matching(created_many_users, admin_client):
    response = await admin_client.get("/users/", params={"role": "student"})
    assert response.status_code == 200, response.text

    body = response.json()

    assert len(body) == 2

    assert body[0]["role"] == "student"
    assert body[1]["role"] == "student"

#Получение списка пользователей не-админом -> 403
async def test_get_users_as_non_admin_returns_403(authorized_client):
    response = await authorized_client.get("/users/")
    assert response.status_code == 403, response.text

#Получение списка пользователей без авторизации -> 401
async def test_get_users_without_auth_returns_401(client):
    response = await client.get("/users/")
    assert response.status_code == 401, response.text

#Получение пользователя по id админом -> 200
async def test_get_user_by_id_returns_200(created_many_users, admin_client):
    first_user = created_many_users[0]
    response = await admin_client.get(f"/users/{first_user["id"]}")

    assert response.status_code == 200, response.text
    assert response.json()["login"] == first_user["login"]

#Получение несуществующего пользователя -> 404
async def test_get_nonexistent_user_returns_404(admin_client):
    response = await admin_client.get("/users/1")
    
    assert response.status_code == 404, response.text

#Получение пользователя с нечисловым id -> 422
async def test_get_user_by_id_with_non_numeric_id_returns_422(admin_client):
    response = await admin_client.get("/users/asd")
    
    assert response.status_code == 422, response.text

#Получение пользователя по id не-админом -> 403
async def test_get_user_by_id_as_non_admin_returns_403(authorized_client):
    response = await authorized_client.get("/users/1")
    
    assert response.status_code == 403, response.text

#Получение пользователя по id без авторизации -> 401
async def test_get_user_by_id_without_auth_returns_401(client):
    response = await client.get("/users/1")
    
    assert response.status_code == 401, response.text

#Удаление пользователя админом -> 204
async def test_delete_user_returns_204(created_many_users, admin_client):
    first_user_id = created_many_users[0]["id"]
    delete_response = await admin_client.delete(f"/users/{first_user_id}")
    assert delete_response.status_code == 204, delete_response.text

    get_response = await admin_client.get(f"/users/{first_user_id}")
    assert get_response.status_code == 404, delete_response.text


#Удаление несуществующего пользователя -> 404
async def test_delete_nonexistent_user_returns_404(admin_client):
    delete_response = await admin_client.delete("/users/1")
    assert delete_response.status_code == 404, delete_response.text

#Попытка удалить самого себя -> 400
async def test_delete_self_returns_400(admin_client):
    me_response = await admin_client.get("/auth/me")
    assert me_response.status_code == 200, me_response.text
    me_id = me_response.json()["id"]

    delete_response = await admin_client.delete(f"/users/{me_id}")
    assert delete_response.status_code == 400, delete_response.text


#Удаление пользователя с нечисловым id -> 422
async def test_delete_user_with_non_numeric_id_returns_422(admin_client):
    response = await admin_client.delete("/users/asd")
    assert response.status_code == 422, response.text

#Удаление пользователя не-админом -> 403
async def test_delete_user_as_non_admin_returns_403(authorized_client):
    response = await authorized_client.delete("/users/1")
    assert response.status_code == 403, response.text

#Удаление пользователя без авторизации -> 401
async def test_delete_user_without_auth_returns_401(client):
    response = await client.delete("/users/1")
    assert response.status_code == 401, response.text
