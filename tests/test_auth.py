async def test_login_returns_token(client):
    await client.post("/auth/register", json={
        "login": "test_user",
        "password": "strongpassword123",
    })

    response = await client.post("/auth/login", json={
        "login": "test_user",
        "password": "strongpassword123"
    })

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"

async def test_login_with_wrong_password_returns_401(client):
    await client.post("/auth/register", json={
        "login": "test_user",
        "password": "strongpassword123",
    })

    response = await client.post("/auth/login", json={
        "login": "test_user",
        "password": "strongpassword12"
    })

    assert response.status_code == 401

async def test_register_with_duplicate_login_fails(client):

    await client.post("/auth/register", json={
        "login": "test_user",
        "password": "strongpassword123",
    })

    response = await client.post("/auth/register", json={
        "login": "test_user",
        "password": "strongpassword1234"
    })

    assert response.status_code == 409

#Успешная регистрация возвращает токены -> 200/201
async def test_register_returns_token(client):
    
    response = await client.post("/auth/register", json={
        "login": "test_user",
        "password": "strongpassword123",
    })

    assert response.status_code == 200, response.text

    body = response.json()

    assert "access_token" in body
    assert "refresh_token" in body

#Регистрация с занятым email -> 409
async def test_register_with_duplicate_email_fails(client):
    first_response = await client.post("/auth/register", json={
        "login": "test_user",
        "password": "strongpassword123",
        "email": "sobaka@mail.ru"
    })

    assert first_response.status_code == 200, first_response.text

    second_response = await client.post("/auth/register", json={
        "login": "test_user2",
        "password": "strongpassword12",
        "email": "sobaka@mail.ru"
    })

    assert second_response.status_code == 409, first_response.text

#Регистрация без обязательного поля (login/password) -> 422
async def test_register_without_required_field_returns_422(client):
    response = await client.post("/auth/register", json={
        "password": "strongpassword123",
    })

    assert response.status_code == 422, response.text

#Логин несуществующего пользователя -> 401
async def test_login_with_nonexistent_user_returns_401(client):
    response = await client.post("/auth/login", json={
            "login": "test_user2",
            "password": "strongpassword123"
        })

    assert response.status_code == 401, response.text

#Логин без обязательного поля -> 422
async def test_login_without_required_field_returns_422(client):
    response = await client.post("/auth/login", json={
            "login": "test_user2",
        })

    assert response.status_code == 422, response.text

#Получение текущего пользователя (/me) -> 200, проверка id/login/role
async def test_me_returns_current_user(authorized_client):
    response = await authorized_client.get("/auth/me")
    assert response.status_code == 200, response.text

    body = response.json()
    assert isinstance(body["id"], int)
    assert body["login"] == "test_user"
    assert body["role"] == "student"

#Получение /me без авторизации -> 401
async def test_me_without_auth_returns_401(client):
    response = await client.get("/auth/me")
    assert response.status_code == 401, response.text

#Получение /me с невалидным токеном -> 401
async def test_me_with_invalid_token_returns_401(client):
    client.headers["Authorization"] = "Мусорный токен"
    response = await client.get("/auth/me")
    assert response.status_code == 401, response.text

#Обновление токенов по валидному refresh_token -> 200
async def test_refresh_returns_new_tokens(client):
    register_response = await client.post("/auth/register", json={
        "login": "test_user",
        "password": "strongpassword123",
        "email": "sobaka@mail.ru"
    })

    refresh_token = register_response.json()["refresh_token"]

    response = await client.post("/auth/refresh", json={
        "refresh_token": refresh_token
    })

    assert response.status_code == 200, response.text

#Обновление с невалидным/некорректным refresh_token -> 401
async def test_refresh_with_invalid_token_returns_401(client):
    register_response = await client.post("/auth/register", json={
        "login": "test_user",
        "password": "strongpassword123",
        "email": "sobaka@mail.ru"
    })

    refresh_token = "Мусорный токен"

    response = await client.post("/auth/refresh", json={
        "refresh_token": refresh_token
    })

    assert response.status_code == 401, response.text

#Успешный logout -> 200
async def test_logout_returns_200(client):
    register_response = await client.post("/auth/register", json={
        "login": "test_user",
        "password": "strongpassword123",
    })
    body = register_response.json()

    client.headers["Authorization"] = f"Bearer {body["access_token"]}"
    logout_response = await client.post("/auth/logout")
    assert logout_response.status_code == 200, logout_response.text

#Обновление с отозванным refresh_token (после logout) -> 401
async def test_refresh_with_revoked_token_returns_401(client):
    register_response = await client.post("/auth/register", json={
        "login": "test_user",
        "password": "strongpassword123",
    })
    body = register_response.json()

    client.headers["Authorization"] = f"Bearer {body["access_token"]}"
    logout_response = await client.post("/auth/logout")
    assert logout_response.status_code == 200, logout_response.text

    refresh_response = await client.post("/auth/refresh", json={
        "refresh_token": body["refresh_token"]
    })
    assert refresh_response.status_code == 401, refresh_response.text

#Обновление без поля refresh_token в теле -> 422
async def test_refresh_without_token_field_returns_422(client):
    response = await client.post("/auth/refresh", json={})

    assert response.status_code == 422, response.text

#Logout без авторизации -> 401
async def test_logout_without_auth_returns_401(client):
    logout_response = await client.post("/auth/logout")
    assert logout_response.status_code == 401, logout_response.text