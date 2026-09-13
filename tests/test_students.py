import pytest

DEFAULT_USER = {
        "first_name": "Userok",
        "last_name": "Userovski",
        "number_of_class": 10,
        "phone": "+79969133520",
        "parent_name": "Ваня",
        "parent_phone": "+79969133521",
        "notes": "Любит формулу дискриминанта",
        "is_active": True,
}


UPDATED_USER = {
        "first_name": "Иван",
        "last_name": "Иванов",
        "number_of_class": 5,
        "phone": "+79969133523",
        "parent_name": "Илона",
        "parent_phone": "+79969133524",
        "notes": "Плохо решает дроби",
        "is_active": False,
}

#Успешное создание студента
async def test_create_student(authorized_client):
    user = DEFAULT_USER.copy()
    response = await authorized_client.post("/students/", json=user)

    assert response.status_code == 201, response.text

    body = response.json()

    assert body["id"] > 0
    assert body["first_name"] == user["first_name"]
    assert body["last_name"] == user["last_name"]
    assert body["number_of_class"] == user["number_of_class"]
    assert body["phone"] == user["phone"]
    assert body["parent_name"] == user["parent_name"]
    assert body["parent_phone"] == user["parent_phone"]
    assert body["notes"] == user["notes"]
    assert body["is_active"] is user["is_active"]

#Проверка валидации неправильных телефонных номеров
@pytest.mark.parametrize("phone", [
    "+799691335201", 
    "+7996913352",
    "899691335201",
    "8996913352",
    "59969133520",
    "+59969133520"
])
async def test_create_student_with_invalid_length_phone(phone, authorized_client):
    user = DEFAULT_USER.copy()
    user["phone"] = phone
    response = await authorized_client.post("/students/", json=user)

    assert response.status_code == 422, response.text

#Проверка валидации неправильных данных в поле класса
@pytest.mark.parametrize("number", [
    12, "!", "f", "F", 0, -12, 2.3
])
async def test_create_student_with_invalid_class_number(number, authorized_client):
    user = DEFAULT_USER.copy()
    user["number_of_class"] = number
    response = await authorized_client.post("/students/", json=user)

    assert response.status_code == 422, response.text

#Проверка создания с незаполненными обязательными полями
@pytest.mark.parametrize("first_name, last_name, number_of_class", [
    (DEFAULT_USER["first_name"], DEFAULT_USER["last_name"], None),
    (DEFAULT_USER["first_name"], None, DEFAULT_USER["number_of_class"]),
    (None, DEFAULT_USER["last_name"], DEFAULT_USER["number_of_class"]),
])
async def test_create_student_with_empty_required_vals(first_name,
                                                       last_name,
                                                       number_of_class,
                                                       authorized_client):
    user = DEFAULT_USER.copy()
    user["first_name"] = first_name
    user["last_name"] = last_name
    user["number_of_class"] = number_of_class
    response = await authorized_client.post("/students/", json=user)

    assert response.status_code == 422, response.text

#Проверка корректного обновления
async def test_update_student_correct_vals(authorized_client):
    user = DEFAULT_USER.copy()
    updated_user = UPDATED_USER.copy()

    post_response = await authorized_client.post("/students/", json=user)

    body = post_response.json()

    id = body["id"]

    updated_user = UPDATED_USER.copy()

    update_response = await authorized_client.patch(f"/students/{id}", json=updated_user)

    updated_body = update_response.json()

    assert update_response.status_code == 200, update_response.text

    assert updated_body["id"] == id
    assert updated_body["first_name"] == updated_user["first_name"]
    assert updated_body["last_name"] == updated_user["last_name"]
    assert updated_body["number_of_class"] == updated_user["number_of_class"]
    assert updated_body["phone"] == updated_user["phone"]
    assert updated_body["parent_name"] == updated_user["parent_name"]
    assert updated_body["parent_phone"] == updated_user["parent_phone"]
    assert updated_body["notes"] == updated_user["notes"]
    assert updated_body["is_active"] is updated_user["is_active"]

#Проверка корректного удаления
async def test_correct_delete_student(authorized_client):
    post_response = await authorized_client.post("/students/", json=DEFAULT_USER.copy())
    student_id = post_response.json()["id"]

    delete_response = await authorized_client.delete(f"/students/{student_id}")
    assert delete_response.status_code == 204, delete_response.text

    get_response = await authorized_client.get(f"/students/{student_id}")
    assert get_response.status_code == 404, get_response.text




