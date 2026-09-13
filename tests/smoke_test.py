async def test_root_returns_ok(client):
    response = await client.get("/")
    assert response.status_code == 200