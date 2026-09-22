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

#Успешное создания студента
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
async def test_update_student_correct_vals(created_solo_student, authorized_client):

    id = created_solo_student["id"]

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
async def test_correct_delete_student(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]

    delete_response = await authorized_client.delete(f"/students/{student_id}")
    assert delete_response.status_code == 204, delete_response.text

    get_response = await authorized_client.get(f"/students/{student_id}")
    assert get_response.status_code == 404, get_response.text

#Проверка передачи айди при удалении, который не является числом
@pytest.mark.parametrize("id", ["f,", "F", "@"])
async def test_delete_student_with_non_numeric_id_returns_422(id, authorized_client):
    delete_response = await authorized_client.delete(f"/students/{id}")
    assert delete_response.status_code == 422, delete_response.text

#Передача невозможных числовых значений id при удалении
@pytest.mark.parametrize("id", [0, -1])
async def test_delete_nonexistent_student_returns_404(id, authorized_client):
    delete_response = await authorized_client.delete(f"/students/{id}")
    assert delete_response.status_code == 404, delete_response.text

#Передача пустого поля id при удалении
async def test_delete_student_with_empty_id_hits_collection_route(authorized_client):
    delete_response = await authorized_client.delete("/students/")
    assert delete_response.status_code == 405, delete_response.text

#Проверка получения ученика по его id
async def test_create_and_get_student(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]

    get_response = await authorized_client.get(f"/students/{student_id}")
    assert get_response.status_code == 200

#Проверка успешного получения списка всех студентов без фильтров
async def test_get_all_students(created_solo_student, authorized_client):
    second_student = await authorized_client.post("/students/", json=DEFAULT_USER)
    third_student = await authorized_client.post("/students/", json=UPDATED_USER)

    assert second_student.status_code == 201, second_student.text
    assert third_student.status_code == 201, third_student.text

    response = await authorized_client.get("/students/")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 3

#проверка успешного получения списка студентов с фильтром по классу
async def test_get_students_with_filter_by_number_of_class(created_many_students, authorized_client):
    response = await authorized_client.get("/students/", params={"number_of_class": 10})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert all(el["number_of_class"] == 10 for el in body)

#проверка успешного получения списка студентов с фильтром по активности
async def test_get_students_with_filter_by_active(created_many_students, authorized_client):
    response = await authorized_client.get("/students/", params={"is_active": True})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert all(el["is_active"] for el in body)

#проверка успешного получения списка студентов с фильтрами по классу и активности
async def test_get_students_with_number_of_class_and_active(created_many_students, authorized_client):
    response = await authorized_client.get("/students/", params={"is_active": True, "number_of_class": 10})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert all(el["is_active"] and el["number_of_class"] == 10 for el in body)

async def test_search_students_by_first_name(created_many_students, authorized_client):
    response = await authorized_client.get("/students/search", params={"query": "Дми"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert all("Дми" in el["first_name"] for el in body)

async def test_search_students_by_last_name(created_many_students, authorized_client):
    response = await authorized_client.get("/students/search", params={"query": "Ивано"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert all("Ивано" in el["last_name"] for el in body)

async def test_search_by_full_name(created_many_students, authorized_client):
    response = await authorized_client.get("/students/search", params={"query": "Дмитрий Иванов"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert all("Дмитрий" in el["first_name"] and "Иванов" in el["last_name"] for el in body)

async def test_search_ignore_register(created_many_students, authorized_client):
    response = await authorized_client.get("/students/search", params={"query": "дмитрий"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert all("Дмитрий" in el["first_name"] for el in body)

    response = await authorized_client.get("/students/search", params={"query": "иванов"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert all("Иванов" in el["last_name"] for el in body)

    response = await authorized_client.get("/students/search", params={"query": "дмитрий иванов"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert all("Дмитрий" in el["first_name"] and "Иванов" in el["last_name"] for el in body)

async def test_search_in_middle(created_many_students, authorized_client):
    response = await authorized_client.get("/students/search", params={"query": "итрий"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert all("Дмитрий" in el["first_name"] for el in body)

async def test_not_match_query(created_many_students, authorized_client):
    response = await authorized_client.get("/students/search", params={"query": "Стас"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 0

async def test_search_without_query(authorized_client):
    response = await authorized_client.get("/students/search")
    assert response.status_code == 422

async def test_search_empty_query(created_many_students, authorized_client):
    response = await authorized_client.get("/students/search", params={"query": ""})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 3

async def test_search_non_authorized_client(client):
    response = await client.get("/students/search", params={"query": ""})
    assert response.status_code == 401

#Проверка на пустую строку (не None) в имени/фамилии
@pytest.mark.parametrize("first_name, last_name", [
    ("", DEFAULT_USER["last_name"]),
    (DEFAULT_USER["first_name"], ""),
])
async def test_create_student_with_empty_string_name(first_name, last_name, authorized_client):
    user = DEFAULT_USER.copy()
    user["first_name"] = first_name
    user["last_name"] = last_name
    response = await authorized_client.post("/students/", json=user)

    assert response.status_code == 422, response.text

#Проверка превышения максимальной длины имени/фамилии/комментария
async def test_create_student_with_too_long_first_name(authorized_client):
    user = DEFAULT_USER.copy()
    user["first_name"] = "А" * 101
    response = await authorized_client.post("/students/", json=user)

    assert response.status_code == 422, response.text

async def test_create_student_with_too_long_last_name(authorized_client):
    user = DEFAULT_USER.copy()
    user["last_name"] = "Б" * 101
    response = await authorized_client.post("/students/", json=user)

    assert response.status_code == 422, response.text

async def test_create_student_with_too_long_notes(authorized_client):
    user = DEFAULT_USER.copy()
    user["notes"] = "текст " * 1000
    response = await authorized_client.post("/students/", json=user)

    assert response.status_code == 422, response.text

#Проверка валидации неправильного parent_phone (отдельный параметр от phone)
@pytest.mark.parametrize("parent_phone", [
    "+799691335201",
    "+7996913352",
    "899691335201",
    "8996913352",
    "59969133520",
    "+59969133520"
])
async def test_create_student_with_invalid_parent_phone(parent_phone, authorized_client):
    user = DEFAULT_USER.copy()
    user["parent_phone"] = parent_phone
    response = await authorized_client.post("/students/", json=user)

    assert response.status_code == 422, response.text

#Обновление несуществующего студента -> 404
@pytest.mark.parametrize("id", [0, -1, 999999])
async def test_update_nonexistent_student_returns_404(id, authorized_client):
    response = await authorized_client.patch(f"/students/{id}", json={"first_name": "Кто-то"})
    assert response.status_code == 404, response.text

#Обновление с невалидным телефоном -> 422
async def test_update_student_with_invalid_phone_returns_422(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    response = await authorized_client.patch(
        f"/students/{student_id}", json={"phone": "899691335"}
    )
    assert response.status_code == 422, response.text

#Обновление с классом вне диапазона -> 422
@pytest.mark.parametrize("number", [0, 12, -1])
async def test_update_student_with_invalid_class_number_returns_422(number, created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    response = await authorized_client.patch(
        f"/students/{student_id}", json={"number_of_class": number}
    )
    assert response.status_code == 422, response.text

#Обновление с пустой строкой в имени -> 422
async def test_update_student_with_empty_first_name_returns_422(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    response = await authorized_client.patch(
        f"/students/{student_id}", json={"first_name": ""}
    )
    assert response.status_code == 422, response.text

#Получение несуществующего студента -> 404
@pytest.mark.parametrize("id", [0, -1, 999999])
async def test_get_nonexistent_student_returns_404(id, authorized_client):
    response = await authorized_client.get(f"/students/{id}")
    assert response.status_code == 404, response.text