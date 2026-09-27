import pytest

# ─── Создание — POST /subscriptions/ ───

# Успешное создание с валидными данными → 201, тело содержит корректно рассчитанные planned_lessons и total_price
async def test_create_subscription_returns_201(created_solo_student_and_many_lessons, authorized_client):
    student_id = created_solo_student_and_many_lessons[0]["student_id"]
    
    post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-01",
        "end_date": "2026-09-30",
        "price_for_one_lesson": 1000,
        "is_paid": True
    })

    assert post_response.status_code == 201, post_response.text

    body = post_response.json()

    assert body["student_id"] == student_id
    assert body["start_date"] == "2026-09-01"
    assert body["end_date"] == "2026-09-30"
    assert body["price_for_one_lesson"] == "1000.00"
    assert body["is_paid"] == True

    assert body["planned_lessons"] == 13
    assert body["total_price"] == "13000.00"

# Правильность расчёта: контролируемые даты (например, ровно 2 недели) + занятие на конкретный день недели → точное число planned_lessons и total_price = planned_lessons * price_for_one_lesson
async def test_create_subscription_calculates_planned_lessons_and_total_price_correctly(created_solo_student_and_lesson, authorized_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 201, post_response.text

    body = post_response.json()

    assert body["student_id"] == student_id
    assert body["start_date"] == "2026-09-07"
    assert body["end_date"] == "2026-09-21"
    assert body["price_for_one_lesson"] == "1000.00"
    assert body["is_paid"] == False

    assert body["planned_lessons"] == 2
    assert body["total_price"] == "2000.00"

# Создание для несуществующего student_id → 404
async def test_create_subscription_with_nonexistent_student_returns_404(authorized_client):
    post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": 1,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 404, post_response.text

# Создание для ученика без единого занятия в расписании → 404 (ZeroLessonsForSubscriptionCreate)
async def test_create_subscription_without_existing_lessons_returns_404(created_solo_student, authorized_client):
    student_id = created_solo_student["id"]

    post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 404, post_response.text

# Точное совпадение дат с существующим абонементом того же ученика → 409
async def test_create_subscription_exact_dates_match_returns_409(created_solo_student_and_lesson,  authorized_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 201, post_response.text

    second_post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert second_post_response.status_code == 409, second_post_response.text

# Частичное пересечение слева от существующего абонемента → 409
async def test_create_subscription_overlap_from_left_returns_409(created_solo_student_and_lesson,  authorized_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 201, post_response.text

    second_post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-01",
        "end_date": "2026-09-08",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert second_post_response.status_code == 409, second_post_response.text

# Частичное пересечение справа от существующего абонемента → 409
async def test_create_subscription_overlap_from_right_returns_409(created_solo_student_and_lesson, authorized_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })
    assert post_response.status_code == 201, post_response.text

    second_post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-15",
        "end_date": "2026-09-25",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })
    assert second_post_response.status_code == 409, second_post_response.text

# Новый интервал целиком поглощает существующий абонемент → 409
async def test_create_subscription_new_interval_contains_existing_returns_409(created_solo_student_and_lesson,  authorized_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 201, post_response.text

    second_post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-05",
        "end_date": "2026-09-23",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert second_post_response.status_code == 409, second_post_response.text

# Новый интервал целиком внутри существующего абонемента → 409
async def test_create_subscription_new_interval_inside_existing_returns_409(created_solo_student_and_lesson,  authorized_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 201, post_response.text

    second_post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-08",
        "end_date": "2026-09-20",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert second_post_response.status_code == 409, second_post_response.text

# end_date нового абонемента == start_date существующего (касание границ) → 409.
# Важно: в отличие от lessons, это тоже пересечение — проверка включительная по дням, не баг
async def test_create_subscription_touching_dates_returns_409(created_solo_student_and_lesson,  authorized_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 201, post_response.text

    second_post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-01",
        "end_date": "2026-09-07",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert second_post_response.status_code == 409, second_post_response.text

# Пересекающиеся даты, но разные ученики → 201 (проверка пересечения идёт по student_id, не глобально)
async def test_create_subscription_overlap_between_different_students_returns_201(created_many_students_many_lessons, authorized_client):
    first_student_id, second_student_id, *_ = list(created_many_students_many_lessons.keys())

    post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": first_student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 201, post_response.text

    second_post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": second_student_id,
        "start_date": "2026-09-08",
        "end_date": "2026-09-20",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert second_post_response.status_code == 201, second_post_response.text

# start_date >= end_date → 422 (валидатор в схеме)
async def test_create_subscription_with_start_after_or_equal_end_returns_422(created_solo_student_and_lesson, authorized_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-20",
        "end_date": "2026-09-01",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 422, post_response.text

# price_for_one_lesson отрицательная → 422
async def test_create_subscription_with_negative_price_returns_422(created_solo_student_and_lesson, authorized_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-01",
        "end_date": "2026-09-20",
        "price_for_one_lesson": -1000,
        "is_paid": False
    })

    assert post_response.status_code == 422, post_response.text

# price_for_one_lesson = 0 → 201 (граница, ноль допустим)
async def test_create_subscription_with_zero_price_returns_201(created_solo_student_and_lesson, authorized_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-01",
        "end_date": "2026-09-20",
        "price_for_one_lesson": 0,
        "is_paid": False
    })

    assert post_response.status_code == 201, post_response.text

@pytest.mark.parametrize("missing_field", ["student_id", "start_date", "end_date", "price_for_one_lesson", "is_paid"])
# Отсутствие любого обязательного поля (student_id, start_date, end_date, price_for_one_lesson, is_paid) по отдельности → 422
async def test_create_subscription_with_missing_required_fields_returns_422(missing_field, created_solo_student_and_lesson, authorized_client):
    student_id = created_solo_student_and_lesson["student_id"]

    payload = {
        "student_id": student_id,
        "start_date": "2026-09-01",
        "end_date": "2026-09-20",
        "price_for_one_lesson": 0,
        "is_paid": False
    }

    del payload[missing_field]

    response = await authorized_client.post("/subscriptions/", json=payload)

    assert response.status_code == 422, response.text

# Нечисловой student_id → 422
async def test_create_subscription_with_non_numeric_student_id_returns_422(authorized_client):
    post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": "asd",
        "start_date": "2026-09-01",
        "end_date": "2026-09-20",
        "price_for_one_lesson": 0,
        "is_paid": False
    })

    assert post_response.status_code == 422, post_response.text

# Некорректный формат даты → 422
async def test_create_subscription_with_invalid_date_format_returns_422(created_solo_student_and_lesson, authorized_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await authorized_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "01.09.2026",
        "end_date": "29.09.2026",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 422, post_response.text

# Без авторизации → 401
async def test_create_subscription_without_auth_returns_401(client):
    post_response = await client.post("/subscriptions/", json={
        "student_id": 1,
        "start_date": "01.09.2026",
        "end_date": "29.09.2026",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 401, post_response.text
