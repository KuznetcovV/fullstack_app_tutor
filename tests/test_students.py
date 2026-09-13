async def test_create_student(authorized_client):
    response = await authorized_client.post("/students/", json={
        "first_name": "Userok",
        "last_name": "Userovski",
        "number_of_class": 10,
        "phone": "+79969133520",
        "parent_name": "Ваня",
        "parent_phone": "+79969133521",
        "notes": "Любит формулу дискриминанта",
        "is_active": True,
    })

    assert response.status_code == 201, response.text

    body = response.json()

    assert body["id"] > 0
    assert body["first_name"] == "Userok"
    assert body["last_name"] == "Userovski"
    assert body["number_of_class"] == 10
    assert body["phone"] == "+79969133520"
    assert body["parent_name"] == "Ваня"
    assert body["parent_phone"] == "+79969133521"
    assert body["notes"] == "Любит формулу дискриминанта"
    assert body["is_active"] is True