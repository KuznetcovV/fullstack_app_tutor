import pytest
from app.core.time import today

#Успешное создание занятия
async def test_create_lesson(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    response = await authorized_client.post("/lessons/", json={
        "student_id": student_id,
        "day": 1,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })

    assert response.status_code == 201, response.text

    body = response.json()

    assert body["id"] > 0
    assert body["student_id"] == student_id
    assert body["day"] == 1
    assert body["time_start"] == "12:00:00"
    assert body["time_end"] == "13:00:00"

#Создание занятия с несуществующим student_id -> 404
async def test_create_lesson_with_nonexistent_student_returns_404(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    response = await authorized_client.post("/lessons/", json={
        "student_id": student_id + 999,
        "day": 1,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })

    assert response.status_code == 404, response.text

#Создание занятия с нечисловым student_id -> 422
async def test_create_lesson_with_non_numeric_student_id_returns_422(authorized_client):
    response = await authorized_client.post("/lessons/", json={
        "student_id": "asd",
        "day": 1,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })

    assert response.status_code == 422, response.text

#Создание занятия с day вне диапазона 0-6 или некорректного типа -> 422
@pytest.mark.parametrize("day", [-1, 7, 2.3, "asd"])
async def test_create_lesson_with_invalid_day_returns_422(day, created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    response = await authorized_client.post("/lessons/", json={
        "student_id": student_id,
        "day": day,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })

    assert response.status_code == 422, response.text

#Создание занятия, где time_start больше или равен time_end -> 422
@pytest.mark.parametrize("time_start", ["13:00:00", "14:00:00"])
async def test_create_lesson_with_start_after_or_equal_end_returns_422(time_start, created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    response = await authorized_client.post("/lessons/", json={
        "student_id": student_id,
        "day": 1,
        "time_start": time_start,
        "time_end": "13:00:00"
    })

    assert response.status_code == 422

#Создание занятия с невалидным форматом time_start/time_end -> 422
@pytest.mark.parametrize("time_start, time_end", [
    ("asd", "13:00:00"),
    ("12:00:00", "asd"),
])
async def test_create_lesson_with_invalid_time_format_returns_422(time_start, time_end, created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    response = await authorized_client.post("/lessons/", json={
        "student_id": student_id,
        "day": 1,
        "time_start": time_start,
        "time_end": time_end
    })

    assert response.status_code == 422, response.text

#Создание занятия с явным null в одном из обязательных полей -> 422
@pytest.mark.parametrize("student_id, day, time_start, time_end", [
    (None, 1, "12:00:00", "13:00:00"),
    (1, None, "12:00:00", "13:00:00"),
    (1, 1, None, "13:00:00"),
    (1, 1, "12:00:00", None)
])
async def test_create_lesson_with_null_required_fields_returns_422(student_id, day, time_start, time_end, authorized_client):
    response = await authorized_client.post("/lessons/", json={
        "student_id": student_id,
        "day": day,
        "time_start": time_start,
        "time_end": time_end
    })

    assert response.status_code == 422, response.text

#Точное совпадение интервала с уже существующим занятием -> 409
async def test_create_lesson_exact_time_match_returns_409(created_solo_student_and_lesson, authorized_client):
    response = await authorized_client.post("/lessons/", json={
        "student_id": created_solo_student_and_lesson["student_id"],
        "day": 1,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })
    assert response.status_code == 409, response.text

#Частичное пересечение слева от существующего занятия -> 409
async def test_create_lesson_overlap_from_left_returns_409(created_solo_student_and_lesson, authorized_client):
    response = await authorized_client.post("/lessons/", json={
        "student_id": created_solo_student_and_lesson["student_id"],
        "day": 1,
        "time_start": "11:00:00",
        "time_end": "12:30:00"
    })
    assert response.status_code == 409, response.text

#Частичное пересечение справа от существующего занятия -> 409
async def test_create_lesson_overlap_from_right_returns_409(created_solo_student_and_lesson, authorized_client):
    response = await authorized_client.post("/lessons/", json={
        "student_id": created_solo_student_and_lesson["student_id"],
        "day": 1,
        "time_start": "12:30:00",
        "time_end": "13:30:00"
    })
    assert response.status_code == 409, response.text

#Новый интервал целиком поглощает существующее занятие -> 409
async def test_create_lesson_new_interval_contains_existing_returns_409(created_solo_student_and_lesson, authorized_client):
    response = await authorized_client.post("/lessons/", json={
        "student_id": created_solo_student_and_lesson["student_id"],
        "day": 1,
        "time_start": "11:00:00",
        "time_end": "13:30:00"
    })
    assert response.status_code == 409, response.text

#Новый интервал целиком внутри существующего занятия -> 409
async def test_create_lesson_new_interval_inside_existing_returns_409(created_solo_student_and_lesson, authorized_client):
    response = await authorized_client.post("/lessons/", json={
        "student_id": created_solo_student_and_lesson["student_id"],
        "day": 1,
        "time_start": "12:10:00",
        "time_end": "12:30:00"
    })
    assert response.status_code == 409, response.text

#Новое занятие начинается ровно в момент конца существующего (касание) -> 201, не пересечение
async def test_create_lesson_touching_after_existing_returns_201(created_solo_student_and_lesson, authorized_client):
    response = await authorized_client.post("/lessons/", json={
        "student_id": created_solo_student_and_lesson["student_id"],
        "day": 1,
        "time_start": "13:00:00",
        "time_end": "14:00:00"
    })
    assert response.status_code == 201, response.text

#Новое занятие заканчивается ровно в момент начала существующего (касание) -> 201, не пересечение
async def test_create_lesson_touching_before_existing_returns_201(created_solo_student_and_lesson, authorized_client):
    response = await authorized_client.post("/lessons/", json={
        "student_id": created_solo_student_and_lesson["student_id"],
        "day": 1,
        "time_start": "11:00:00",
        "time_end": "12:00:00"
    })
    assert response.status_code == 201, response.text

#Тот же интервал времени, но другой день недели -> 201, не пересечение
async def test_create_lesson_same_time_different_day_returns_201(created_solo_student_and_lesson, authorized_client):
    response = await authorized_client.post("/lessons/", json={
        "student_id": created_solo_student_and_lesson["student_id"],
        "day": 2,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })
    assert response.status_code == 201, response.text

#Пересечение по времени между занятиями разных учеников -> 409 (проверка глобальная, не по ученику)
async def test_create_lesson_overlap_between_different_students_returns_409(created_many_students, authorized_client):

    first_student_id = created_many_students[0]["id"]
    second_student_id = created_many_students[1]["id"]

    first_response = await authorized_client.post("/lessons/", json={
        "student_id": first_student_id,
        "day": 1,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })

    assert first_response.status_code == 201, first_response.text

    second_response = await authorized_client.post("/lessons/", json={
        "student_id": second_student_id,
        "day": 1,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })

    assert second_response.status_code == 409, second_response.text

#Получение списка всех занятий без фильтра
async def test_get_all_lessons(created_many_students_many_lessons, authorized_client):
    response = await authorized_client.get("/lessons/")

    assert response.status_code == 200, response.text
    
    body = response.json()

    assert len(body) == 9

#Фильтр по конкретному дню -> только занятия этого дня
async def test_get_all_lessons_with_day_filter(created_many_students_many_lessons, authorized_client):
    response = await authorized_client.get("/lessons/", params={"day": 1})
    assert response.status_code == 200, response.text

    body = response.json()

    assert len(body) == 3

#Фильтр по дню, под который ничего не подходит -> пустой список, а не 404
async def test_get_lessons_with_day_filter_no_matches_returns_empty_list(created_many_students_many_lessons, authorized_client):
    response = await authorized_client.get("/lessons/", params={"day": 2})
    assert response.status_code == 200, response.text

    body = response.json()

    assert len(body) == 0

#Нечисловое значение day в query -> 422 (валидация срабатывает до похода в БД)
async def test_get_lessons_with_invalid_day_filter_returns_422(authorized_client):
    response = await authorized_client.get("/lessons/", params={"day": "as"})
    assert response.status_code == 422, response.text

#Запрос без авторизации -> 401
async def test_get_lessons_without_auth_returns_401(client):

    response = await client.get("/lessons/")
    assert response.status_code == 401, response.text

#Возвращает только уроки с сегодняшним днём недели (день берём из того же today(), что использует сервис)
async def test_get_today_lessons_returns_todays_lessons(authorized_client, created_solo_student):
    today_weekday = today().weekday()

    response = await authorized_client.post("/lessons/", json={
        "student_id": created_solo_student["id"],
        "day": today_weekday,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })

    assert response.status_code == 201, response.text

    get_response = await authorized_client.get("/lessons/today")
    assert get_response.status_code == 200, get_response.text

    body = get_response.json()

    assert len(body) == 1
    assert body[0]["day"] == today_weekday

#Уроков на сегодня нет -> пустой список
async def test_get_today_empty_list_lessons(authorized_client):

    response = await authorized_client.get("/lessons/today")
    assert response.status_code == 200, response.text

    body = response.json()

    assert len(body) == 0

#Запрос без авторизации -> 401
async def test_get_today_lessons_without_auth_returns_401(client):

    response = await client.get("/lessons/today")
    assert response.status_code == 401, response.text

#Успешное получение урока по id
async def test_get_lesson_by_id_returns_200(created_solo_student_and_lesson, authorized_client):
    lesson_id = created_solo_student_and_lesson["id"]

    response = await authorized_client.get(f"/lessons/{lesson_id}")
    assert response.status_code == 200, response.text

#Несуществующий id -> 404
async def test_get_lesson_by_nonexistent_id_returns_404(authorized_client):
    response = await authorized_client.get("/lessons/999999")
    assert response.status_code == 404, response.text

#Нечисловой id -> 422
async def test_get_lesson_by_not_numeric_id_returns_422(authorized_client):
    response = await authorized_client.get("/lessons/asd")
    assert response.status_code == 422, response.text

#Запрос без авторизации -> 401
async def test_get_lesson_without_auth_returns_401(client):

    response = await client.get("/lessons/1")
    assert response.status_code == 401, response.text

#Успешное обновление всех полей урока, включая смену ученика -> 200
async def test_update_lesson_all_fields_returns_200(created_many_students_many_lessons, authorized_client):
    student_ids = list(created_many_students_many_lessons.keys())
    first_student_id = student_ids[0]
    second_student_id = student_ids[1]

    first_student_first_lesson_id = created_many_students_many_lessons[first_student_id][0]["id"]
    first_student_first_lesson_day = created_many_students_many_lessons[first_student_id][0]["day"]

    response = await authorized_client.patch(f"/lessons/{first_student_first_lesson_id}", json={
        "student_id": second_student_id,
        "day": first_student_first_lesson_day + 1,
        "time_start": "14:00:00",
        "time_end": "15:00:00"
    })

    assert response.status_code == 200, response.text

#Частичное обновление (только время) -> остальные поля не меняются
async def test_update_lesson_partial_fields_keeps_rest_unchanged(created_solo_student_and_many_lessons, authorized_client):
    first_lesson = created_solo_student_and_many_lessons[0]
    first_lesson_id = first_lesson["id"]

    response = await authorized_client.patch(f"/lessons/{first_lesson_id}", json={
        "time_start": "15:00:00",
        "time_end": "16:00:00"
    })

    assert response.status_code == 200, response.text

    body = response.json()

    assert body["time_start"] == "15:00:00"
    assert body["time_end"] == "16:00:00"
    assert body["day"] == first_lesson["day"]
    assert body["student_id"] == first_lesson["student_id"]

#Обновление несуществующего урока -> 404
async def test_update_nonexistent_lesson_returns_404(authorized_client):
    response = await authorized_client.patch(f"/lessons/-1", json={
        "time_start": "15:00:00",
        "time_end": "16:00:00"  
    })

    assert response.status_code == 404, response.text

#day вне диапазона при обновлении -> 422
async def test_update_lesson_with_invalid_day_returns_422(created_solo_student_and_lesson, authorized_client):
    lesson_id = created_solo_student_and_lesson["id"]

    response = await authorized_client.patch(f"/lessons/{lesson_id}", json={
        "day": 8
    })

    assert response.status_code == 422, response.text

#student_id при обновлении указывает на несуществующего ученика -> 404
async def test_update_lesson_with_nonexistent_student_returns_404(created_solo_student_and_lesson, authorized_client):
    lesson_id = created_solo_student_and_lesson["id"]

    response = await authorized_client.patch(f"/lessons/{lesson_id}", json={
        "student_id": 0
    })

    assert response.status_code == 404, response.text

#Оба поля времени переданы сразу, start >= end -> 422 (validate_lesson_time в сервисе, согласовано с 422 при создании)
async def test_update_lesson_with_start_after_or_equal_end_returns_422(created_solo_student_and_lesson, authorized_client):
    lesson_id = created_solo_student_and_lesson["id"]

    response = await authorized_client.patch(f"/lessons/{lesson_id}", json={
        "time_start": "14:00:00",
        "time_end": "13:00:00"
    })

    assert response.status_code == 422, response.text

#Меняется только time_start, вместе с текущим (не переданным) time_end получается некорректный интервал -> 422
async def test_update_lesson_time_start_conflicts_with_existing_time_end_returns_422(created_solo_student_and_lesson, authorized_client):
    lesson_id = created_solo_student_and_lesson["id"]

    response = await authorized_client.patch(f"/lessons/{lesson_id}", json={
        "time_start": "14:00:00"
    })

    assert response.status_code == 422, response.text

#Меняется только time_end, вместе с текущим (не переданным) time_start получается некорректный интервал -> 422
async def test_update_lesson_time_end_conflicts_with_existing_time_start_returns_422(created_solo_student_and_lesson, authorized_client):
    lesson_id = created_solo_student_and_lesson["id"]

    response = await authorized_client.patch(f"/lessons/{lesson_id}", json={
        "time_end": "11:00:00"
    })

    assert response.status_code == 422, response.text

#Обновление создаёт пересечение с другим существующим уроком -> 409
async def test_update_lesson_creates_intersection_with_other_lesson_returns_409(created_solo_student_and_many_lessons, authorized_client):
    first_lesson_id = created_solo_student_and_many_lessons[0]["id"]

    response = await authorized_client.patch(f"/lessons/{first_lesson_id}", json={
        "day": 3
    })

    assert response.status_code == 409, response.text

#Обновление на свободный день, пересечения нет -> 200
async def test_update_lesson_without_intersection_returns_200(created_solo_student_and_many_lessons, authorized_client):
    first_lesson_id = created_solo_student_and_many_lessons[0]["id"]

    response = await authorized_client.patch(f"/lessons/{first_lesson_id}", json={
        "day": 4
    })

    assert response.status_code == 200, response.text

#Обновление, не трогающее время (меняется только student_id) -> не должно ложно сработать как пересечение с самим собой (exclude_id)
async def test_update_lesson_without_touching_time_does_not_trigger_self_intersection(created_many_students_many_lessons, authorized_client):
    students_ids = list(created_many_students_many_lessons.keys())
    first_student_id = students_ids[0]
    second_student_id = students_ids[1]

    second_student_first_lesson_id = created_many_students_many_lessons[second_student_id][0]["id"]

    response = await authorized_client.patch(f"/lessons/{second_student_first_lesson_id}", json={
        "student_id": first_student_id
    })

    assert response.status_code == 200, response.text

#Пустое тело {} -> 200, ничего не меняется
async def test_update_lesson_with_empty_body_returns_200(created_solo_student_and_lesson, authorized_client):
    lesson_id = created_solo_student_and_lesson["id"]

    response = await authorized_client.patch(f"/lessons/{lesson_id}", json={})

    assert response.status_code == 200, response.text

#Запрос без авторизации -> 401
async def test_update_lesson_without_auth_returns_401(client):
    response = await client.patch("/lessons/1", json={})

    assert response.status_code == 401, response.text

#Успешное удаление -> 204, повторный GET того же id -> 404
async def test_delete_lesson_returns_204_and_then_404(created_solo_student_and_lesson, authorized_client):
    lesson_id = created_solo_student_and_lesson["id"]

    delete_response = await authorized_client.delete(f"/lessons/{lesson_id}")
    assert delete_response.status_code == 204, delete_response.text

    get_response = await authorized_client.get(f"/lessons/{lesson_id}")

    assert get_response.status_code == 404, get_response.text

#Удаление несуществующего урока -> 404
async def test_delete_nonexistent_lesson_returns_404(authorized_client):
    response = await authorized_client.delete("/lessons/1")

    assert response.status_code == 404, response.text

#Нечисловой id при удалении -> 422
async def test_delete_lesson_with_non_numeric_id_returns_422(authorized_client):
    response = await authorized_client.delete("/lessons/asd")

    assert response.status_code == 422, response.text

#DELETE без id попадает на роут коллекции, где нет DELETE -> 405
async def test_delete_lessons_without_id_returns_405(authorized_client):
    response = await authorized_client.delete("/lessons/")

    assert response.status_code == 405, response.text

#Запрос без авторизации -> 401
async def test_delete_lesson_without_auth_returns_401(client):
    response = await client.delete("/lessons/1")

    assert response.status_code == 401, response.text
