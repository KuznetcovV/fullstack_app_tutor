import pytest

# Создание лога с минимальным набором полей (student_id + дата) — успех
async def test_create_lesson_log_with_minimal_fields_returns_201(created_solo_student_and_lesson, authorized_client):
    student_id = created_solo_student_and_lesson["student_id"]

    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "lesson_log_date": "1998-01-01"
    })

    assert response.status_code == 201, response.text

    body = response.json()

    assert body["student_id"] == student_id
    assert body["lesson_log_date"] == "1998-01-01"

# Создание лога со всеми возможными полями заполненными — успех
async def test_create_lesson_log_with_all_fields_returns_201(created_solo_student_and_lesson, authorized_client):
    student_id = created_solo_student_and_lesson["student_id"]
    lesson_id = created_solo_student_and_lesson["id"]

    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "lesson_id": lesson_id,
        "lesson_log_date": "1998-01-01",
        "topic": "Квадратные уравнения",
        "textbook": "Тестовый учебник",
        "solved_tasks": "№451, 433, 470",
        "grade": 3,
        "comment": "Хорошо понял формулу дискриминанта"
    })

    assert response.status_code == 201, response.text

    body = response.json()

    assert body["student_id"] == student_id
    assert body["lesson_id"] == lesson_id
    assert body["lesson_log_date"] == "1998-01-01"
    assert body["topic"] == "Квадратные уравнения"
    assert body["textbook"] == "Тестовый учебник"
    assert body["solved_tasks"] == "№451, 433, 470"
    assert body["grade"] == 3
    assert body["comment"] == "Хорошо понял формулу дискриминанта"

# Создание лога для несуществующего ученика
async def test_create_lesson_log_with_nonexistent_student_returns_404(authorized_client):
    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": 1,
        "lesson_log_date": "1998-01-01"
    })

    assert response.status_code == 404, response.text

# Создание лога с привязкой к несуществующему занятию
async def test_create_lesson_log_with_nonexistent_lesson_returns_404(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]

    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "lesson_log_date": "1998-01-01",
        "lesson_id": 1
    })

    assert response.status_code == 404, response.text

# Создание лога с привязкой к занятию, которое принадлежит другому ученику
async def test_create_lesson_log_with_foreign_lesson_returns_409(created_many_students_many_lessons, authorized_client):
    first_student_id = list(created_many_students_many_lessons.keys())[0]
    second_student_id = list(created_many_students_many_lessons.keys())[1]

    first_student_first_lesson_id = created_many_students_many_lessons[first_student_id][0]["id"]

    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": second_student_id,
        "lesson_id": first_student_first_lesson_id,
        "lesson_log_date": "1998-01-01"
    })

    assert response.status_code == 409, response.text

# Создание лога с lesson_id, явно переданным как null — отвязанный лог создаётся нормально
async def test_create_lesson_log_with_null_lesson_id_returns_201(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]

    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "lesson_id": None,
        "lesson_log_date": "2026-09-22"
    })

    assert response.status_code == 201, response.text

# Создание лога без обязательного поля student_id
async def test_create_lesson_log_without_student_id_returns_422(authorized_client):
    response = await authorized_client.post("/lesson_logs/", json={
        "lesson_id": 1,
        "lesson_log_date": "2026-09-22"
    })

    assert response.status_code == 422, response.text

# Создание лога с нечисловым student_id
async def test_create_lesson_log_with_non_numeric_student_id_returns_422(authorized_client):
    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": "asd",
        "lesson_id": 1,
        "lesson_log_date": "2026-09-22"
    })

    assert response.status_code == 422, response.text

# Создание лога без обязательного поля lesson_log_date
async def test_create_lesson_log_without_date_returns_422(created_solo_student, authorized_client):
    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": created_solo_student["id"],
    })

    assert response.status_code == 422, response.text

# Создание лога с датой в неверном формате
async def test_create_lesson_log_with_invalid_date_format_returns_422(created_solo_student, authorized_client):
    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": created_solo_student["id"],
        "lesson_log_date": "21.11.1998"
    })

    assert response.status_code == 422, response.text

# Создание лога с topic длиннее 1000 символов
async def test_create_lesson_log_with_too_long_topic_returns_422(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    topic = 'a' * 1001
    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "topic": topic,
        "lesson_log_date": "2026-09-22"
    })

    assert response.status_code == 422, response.text

# Создание лога с topic ровно 1000 символов — граница, должно пройти
async def test_create_lesson_log_with_max_length_topic_returns_201(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    topic = 'a' * 1000
    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "topic": topic,
        "lesson_log_date": "2026-09-22"
    })

    assert response.status_code == 201, response.text

# Создание лога с пустой строкой в topic
async def test_create_lesson_log_with_empty_topic_returns_422(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "topic": "",
        "lesson_log_date": "2026-09-22"
    })

    assert response.status_code == 422, response.text

# Создание лога с textbook длиннее 255 символов
async def test_create_lesson_log_with_textbook_over_255_returns_422(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    textbook = "a" * 256
    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "textbook": textbook,
        "lesson_log_date": "2026-09-22"
    })

    assert response.status_code == 422, response.text

# Создание лога с textbook ровно 255 символов — граница, должно пройти
async def test_create_lesson_log_with_max_length_textbook_returns_201(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    textbook = "a" * 255
    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "textbook": textbook,
        "lesson_log_date": "2026-09-22"
    })

    assert response.status_code == 201, response.text

# Создание лога с очень длинным solved_tasks — у этого поля нет лимита длины, поведение осознанное
async def test_create_lesson_log_with_very_long_solved_tasks_returns_201(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    solved_tasks = "a" * 5000
    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "solved_tasks": solved_tasks,
        "lesson_log_date": "2026-09-22"
    })

    assert response.status_code == 201, response.text

# Создание лога с comment длиннее 1000 символов
async def test_create_lesson_log_with_too_long_comment_returns_422(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    comment = "a" * 1001
    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "comment": comment,
        "lesson_log_date": "2026-09-22"
    })

    assert response.status_code == 422, response.text

# Создание лога с пустой строкой в comment
async def test_create_lesson_log_with_empty_comment_returns_422(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    comment = ""
    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "comment": comment,
        "lesson_log_date": "2026-09-22"
    })

    assert response.status_code == 422, response.text

# Создание лога с grade вне допустимого диапазона (ниже и выше границ)
@pytest.mark.parametrize("grade", [1, 6])
async def test_create_lesson_log_with_grade_below_or_above_range_returns_422(grade, created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "grade": grade,
        "lesson_log_date": "2026-09-22"
    })

    assert response.status_code == 422, response.text

# Создание лога со всеми допустимыми значениями grade (2-5)
@pytest.mark.parametrize("grade", [2, 3, 4, 5])
async def test_create_lesson_log_with_all_grades_returns_201(grade, created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "grade": grade,
        "lesson_log_date": "2026-09-22"
    })

    assert response.status_code == 201, response.text

# Создание лога с нечисловым grade
async def test_create_lesson_log_with_non_numeric_grade_returns_422(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]
    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "grade": "asd",
        "lesson_log_date": "2026-09-22"
    })

    assert response.status_code == 422, response.text

# Создание лога без авторизации
async def test_create_lesson_log_without_auth_returns_401(client):
    response = await client.post("/lesson_logs/", json={
        "student_id": 1,
        "lesson_log_date": "2026-09-22"
    })

    assert response.status_code == 401

# Получение списка всех логов — непустой список
async def test_get_lesson_logs_returns_200(created_solo_student_and_lesson_log, authorized_client):
    response = await authorized_client.get("/lesson_logs/")

    assert response.status_code == 200, response.text

    body = response.json()
    assert len(body) == 1

# Получение списка логов, когда их ещё нет — пустой список
async def test_get_lesson_logs_empty_returns_200(authorized_client):
    response = await authorized_client.get("/lesson_logs/")

    assert response.status_code == 200, response.text

    body = response.json()
    assert len(body) == 0

# Получение списка логов без авторизации
async def test_get_lesson_logs_without_auth_returns_401(client):
    response = await client.get("/lesson_logs/")
    assert response.status_code == 401, response.text

# Получение существующего лога по id
async def test_get_lesson_log_by_id_returns_200(created_solo_student_and_lesson_log, authorized_client):
    lesson_log_id = created_solo_student_and_lesson_log["id"]
    response = await authorized_client.get(f"/lesson_logs/{lesson_log_id}")

    assert response.status_code == 200, response.text

# Получение лога по несуществующему id
async def test_get_lesson_log_by_nonexistent_id_returns_404(authorized_client):
    response = await authorized_client.get("/lesson_logs/1")

    assert response.status_code == 404, response.text

# Получение лога по нечисловому id
async def test_get_lesson_log_by_non_numeric_id_returns_422(authorized_client):
    response = await authorized_client.get("/lesson_logs/asd")

    assert response.status_code == 422, response.text

# Получение лога по id без авторизации
async def test_get_lesson_log_by_id_without_auth_returns_401(client):
    response = await client.get("/lesson_logs/1")

    assert response.status_code == 401, response.text

# Обновление одного поля лога — остальные поля не затрагиваются
async def test_update_lesson_log_single_field_returns_200(created_solo_student_and_lesson_log, authorized_client):
    lesson_log_id = created_solo_student_and_lesson_log["id"]

    response = await authorized_client.patch(f"/lesson_logs/{lesson_log_id}", json={
        "lesson_log_date": "2025-09-22"
    })

    assert response.status_code == 200, response.text

    body = response.json()
    assert body["lesson_log_date"] == "2025-09-22"

# Обновление сразу нескольких полей лога
async def test_update_lesson_log_multiple_fields_returns_200(created_solo_student_and_lesson_log, authorized_client):
    lesson_log_id = created_solo_student_and_lesson_log["id"]

    response = await authorized_client.patch(f"/lesson_logs/{lesson_log_id}", json={
        "lesson_log_date": "2025-09-22",
        "topic": "Интегралы"
    })

    assert response.status_code == 200, response.text

    body = response.json()
    assert body["lesson_log_date"] == "2025-09-22"
    assert body["topic"] == "Интегралы"

# Обновление с пустым телом запроса — ничего не меняется, но запрос успешен
async def test_update_lesson_log_with_empty_body_returns_200(created_solo_student_and_lesson_log, authorized_client):
    lesson_log_id = created_solo_student_and_lesson_log["id"]

    response = await authorized_client.patch(f"/lesson_logs/{lesson_log_id}", json={})

    assert response.status_code == 200, response.text

# Обновление несуществующего лога
async def test_update_nonexistent_lesson_log_returns_404(authorized_client):
    response = await authorized_client.patch("/lesson_logs/2", json={})

    assert response.status_code == 404, response.text

# Обновление с нечисловым id лога
async def test_update_lesson_log_with_non_numeric_id_returns_422(authorized_client):
    response = await authorized_client.patch("/lesson_logs/asd")

    assert response.status_code == 422, response.text

# Обновление student_id на несуществующего ученика
async def test_update_lesson_log_with_nonexistent_student_returns_404(created_solo_student_and_lesson_log, authorized_client):
    lesson_log_id = created_solo_student_and_lesson_log["id"]
    student_id = created_solo_student_and_lesson_log["student_id"]

    response = await authorized_client.patch(f"/lesson_logs/{lesson_log_id}", json={
        "student_id": student_id - 1
    })

    assert response.status_code == 404, response.text

# Обновление lesson_id на несуществующее занятие
async def test_update_lesson_log_with_nonexistent_lesson_returns_404(created_solo_student_and_lesson_log, authorized_client):
    lesson_log_id = created_solo_student_and_lesson_log["id"]
    
    response = await authorized_client.patch(f"/lesson_logs/{lesson_log_id}", json={
        "lesson_id": 1
    })

    assert response.status_code == 404, response.text

# Обновление lesson_id на занятие, принадлежащее другому ученику
async def test_update_lesson_log_with_foreign_lesson_returns_409(created_solo_student_and_lesson_log, authorized_client):
    first_student_lesson_log_id = created_solo_student_and_lesson_log["id"]

    second_student_response = await authorized_client.post("/students/", json={
        "first_name": "Второй",
        "last_name": "Ученик",
        "number_of_class": 9
    })
    second_student_id = second_student_response.json()["id"]

    second_lesson_response = await authorized_client.post("/lessons/", json={
        "student_id": second_student_id,
        "day": 2,
        "time_start": "10:00:00",
        "time_end": "11:00:00"
    })
    lesson_id_for_second_student = second_lesson_response.json()["id"]

    response = await authorized_client.patch(f"/lesson_logs/{first_student_lesson_log_id}", json={
        "lesson_id": lesson_id_for_second_student
    })

    assert response.status_code == 409, response.text

# Явная отвязка занятия от лога (lesson_id → null)
async def test_update_lesson_log_unlink_lesson_returns_200(created_solo_student_and_lesson, authorized_client):
    student_id = created_solo_student_and_lesson["student_id"]
    lesson_id = created_solo_student_and_lesson["id"]

    post_response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "lesson_id": lesson_id,
        "lesson_log_date": "2026-09-22"
    })
    assert post_response.status_code == 201, post_response.text
    lesson_log_id = post_response.json()["id"]

    patch_response = await authorized_client.patch(f"/lesson_logs/{lesson_log_id}", json={
        "lesson_id": None
    })
    assert patch_response.status_code == 200, patch_response.text

# Одновременная смена ученика и отвязка занятия — регрессионный тест на баг с model_fields_set
async def test_update_lesson_log_change_student_and_unlink_lesson_returns_200(created_solo_student_and_lesson, authorized_client):
    student_id = created_solo_student_and_lesson["student_id"]
    lesson_id = created_solo_student_and_lesson["id"]

    post_response = await authorized_client.post("/lesson_logs/", json={
        "student_id": student_id,
        "lesson_id": lesson_id,
        "lesson_log_date": "2026-09-22"
    })
    assert post_response.status_code == 201, post_response.text
    lesson_log_id = post_response.json()["id"]

    second_student_response = await authorized_client.post("/students/", json={
        "first_name": "Второй",
        "last_name": "Ученик",
        "number_of_class": 9
    })
    second_student_id = second_student_response.json()["id"]

    response = await authorized_client.patch(f"/lesson_logs/{lesson_log_id}", json={
        "student_id": second_student_id,
        "lesson_id": None
    })

    assert response.status_code == 200, response.text

# Обновление topic на пустую строку
async def test_update_lesson_log_with_empty_topic_returns_422(created_solo_student_and_lesson_log, authorized_client):
    lesson_log_id = created_solo_student_and_lesson_log["id"]
    response = await authorized_client.patch(f"/lesson_logs/{lesson_log_id}", json={
        "topic": ""
    })

    assert response.status_code == 422, response.text

# Обновление topic на строку длиннее 1000 символов
async def test_update_lesson_log_with_too_long_topic_returns_422(created_solo_student_and_lesson_log, authorized_client):
    topic = "a" * 1001
    lesson_log_id = created_solo_student_and_lesson_log["id"]
    response = await authorized_client.patch(f"/lesson_logs/{lesson_log_id}", json={
        "topic": topic
    })

    assert response.status_code == 422, response.text

# Обновление grade на значения вне допустимого диапазона
@pytest.mark.parametrize("grade", [1, 6])
async def test_update_lesson_log_with_invalid_grade_returns_422(grade, created_solo_student_and_lesson_log, authorized_client):
    lesson_log_id = created_solo_student_and_lesson_log["id"]
    response = await authorized_client.patch(f"/lesson_logs/{lesson_log_id}", json={
        "grade": grade
    })

    assert response.status_code == 422, response.text

# Обновление grade на граничные и промежуточные допустимые значения (2-5)
@pytest.mark.parametrize("grade", [2, 3, 4, 5])
async def test_update_lesson_log_with_boundary_grade_returns_200(grade, created_solo_student_and_lesson_log, authorized_client):
    lesson_log_id = created_solo_student_and_lesson_log["id"]
    response = await authorized_client.patch(f"/lesson_logs/{lesson_log_id}", json={
        "grade": grade
    })

    assert response.status_code == 200, response.text

# Обновление textbook на строку длиннее 255 символов
async def test_update_lesson_log_with_too_long_textbook_returns_422(created_solo_student_and_lesson_log, authorized_client):
    textbook = "a" * 256
    lesson_log_id = created_solo_student_and_lesson_log["id"]
    response = await authorized_client.patch(f"/lesson_logs/{lesson_log_id}", json={
        "textbook": textbook
    })

    assert response.status_code == 422, response.text

# Обновление лога без авторизации
async def test_update_lesson_log_without_auth_returns_401(client):
    response = await client.patch("/lesson_logs/1", json={})

    assert response.status_code == 401, response.text

# Удаление лога — успех, затем повторный запрос подтверждает, что лога больше нет
async def test_delete_lesson_log_returns_204_and_then_404(created_solo_student_and_lesson_log, authorized_client):
    lesson_log_id = created_solo_student_and_lesson_log["id"]
    delete_response = await authorized_client.delete(f"/lesson_logs/{lesson_log_id}")

    assert delete_response.status_code == 204, delete_response.text

    get_response = await authorized_client.get(f"/lesson_logs/{lesson_log_id}")

    assert get_response.status_code == 404, get_response.text

# Удаление несуществующего лога
async def test_delete_nonexistent_lesson_log_returns_404(authorized_client):
    response = await authorized_client.delete("/lesson_logs/1")
    assert response.status_code == 404, response.text

# Удаление лога с нечисловым id
async def test_delete_lesson_log_with_non_numeric_id_returns_422(authorized_client):
    response = await authorized_client.delete("/lesson_logs/asd")
    assert response.status_code == 422, response.text

# Удаление лога без авторизации
async def test_delete_lesson_log_without_auth_returns_401(client):
    response = await client.delete("/lesson_logs/1")
    assert response.status_code == 401, response.text