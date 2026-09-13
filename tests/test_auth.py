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