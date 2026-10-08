from decimal import Decimal

import pytest
from app.core.time import today
from datetime import timedelta

# ─── Создание — POST /subscriptions/ ───

# Успешное создание с валидными данными → 201, тело содержит корректно рассчитанные planned_lessons и total_price
async def test_create_subscription_returns_201(created_solo_student_and_many_lessons, teacher_client):
    student_id = created_solo_student_and_many_lessons[0]["student_id"]
    
    post_response = await teacher_client.post("/subscriptions/", json={
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
async def test_create_subscription_calculates_planned_lessons_and_total_price_correctly(created_solo_student_and_lesson, teacher_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await teacher_client.post("/subscriptions/", json={
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
async def test_create_subscription_with_nonexistent_student_returns_404(teacher_client):
    post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": 1,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 404, post_response.text

# Создание для ученика без единого занятия в расписании → 404 (ZeroLessonsForSubscriptionCreate)
async def test_create_subscription_without_existing_lessons_returns_404(created_solo_student, teacher_client):
    student_id = created_solo_student["id"]

    post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 404, post_response.text

# Точное совпадение дат с существующим абонементом того же ученика → 409
async def test_create_subscription_exact_dates_match_returns_409(created_solo_student_and_lesson,  teacher_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 201, post_response.text

    second_post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert second_post_response.status_code == 409, second_post_response.text

# Частичное пересечение слева от существующего абонемента → 409
async def test_create_subscription_overlap_from_left_returns_409(created_solo_student_and_lesson,  teacher_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 201, post_response.text

    second_post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-01",
        "end_date": "2026-09-08",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert second_post_response.status_code == 409, second_post_response.text

# Частичное пересечение справа от существующего абонемента → 409
async def test_create_subscription_overlap_from_right_returns_409(created_solo_student_and_lesson, teacher_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })
    assert post_response.status_code == 201, post_response.text

    second_post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-15",
        "end_date": "2026-09-25",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })
    assert second_post_response.status_code == 409, second_post_response.text

# Новый интервал целиком поглощает существующий абонемент → 409
async def test_create_subscription_new_interval_contains_existing_returns_409(created_solo_student_and_lesson,  teacher_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 201, post_response.text

    second_post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-05",
        "end_date": "2026-09-23",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert second_post_response.status_code == 409, second_post_response.text

# Новый интервал целиком внутри существующего абонемента → 409
async def test_create_subscription_new_interval_inside_existing_returns_409(created_solo_student_and_lesson,  teacher_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 201, post_response.text

    second_post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-08",
        "end_date": "2026-09-20",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert second_post_response.status_code == 409, second_post_response.text

# end_date нового абонемента == start_date существующего (касание границ) → 409.
# Важно: в отличие от lessons, это тоже пересечение — проверка включительная по дням, не баг
async def test_create_subscription_touching_dates_returns_409(created_solo_student_and_lesson,  teacher_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 201, post_response.text

    second_post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-01",
        "end_date": "2026-09-07",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert second_post_response.status_code == 409, second_post_response.text

# Пересекающиеся даты, но разные ученики → 201 (проверка пересечения идёт по student_id, не глобально)
async def test_create_subscription_overlap_between_different_students_returns_201(created_many_students_many_lessons, teacher_client):
    first_student_id, second_student_id, *_ = list(created_many_students_many_lessons.keys())

    post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": first_student_id,
        "start_date": "2026-09-07",
        "end_date": "2026-09-21",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 201, post_response.text

    second_post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": second_student_id,
        "start_date": "2026-09-08",
        "end_date": "2026-09-20",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert second_post_response.status_code == 201, second_post_response.text

# start_date >= end_date → 422 (валидатор в схеме)
async def test_create_subscription_with_start_after_or_equal_end_returns_422(created_solo_student_and_lesson, teacher_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-20",
        "end_date": "2026-09-01",
        "price_for_one_lesson": 1000,
        "is_paid": False
    })

    assert post_response.status_code == 422, post_response.text

# price_for_one_lesson отрицательная → 422
async def test_create_subscription_with_negative_price_returns_422(created_solo_student_and_lesson, teacher_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-01",
        "end_date": "2026-09-20",
        "price_for_one_lesson": -1000,
        "is_paid": False
    })

    assert post_response.status_code == 422, post_response.text

# price_for_one_lesson = 0 → 201 (граница, ноль допустим)
async def test_create_subscription_with_zero_price_returns_201(created_solo_student_and_lesson, teacher_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-09-01",
        "end_date": "2026-09-20",
        "price_for_one_lesson": 0,
        "is_paid": False
    })

    assert post_response.status_code == 201, post_response.text

@pytest.mark.parametrize("missing_field", ["student_id", "start_date", "end_date", "price_for_one_lesson", "is_paid"])
# Отсутствие любого обязательного поля (student_id, start_date, end_date, price_for_one_lesson, is_paid) по отдельности → 422
async def test_create_subscription_with_missing_required_fields_returns_422(missing_field, created_solo_student_and_lesson, teacher_client):
    student_id = created_solo_student_and_lesson["student_id"]

    payload = {
        "student_id": student_id,
        "start_date": "2026-09-01",
        "end_date": "2026-09-20",
        "price_for_one_lesson": 0,
        "is_paid": False
    }

    del payload[missing_field]

    response = await teacher_client.post("/subscriptions/", json=payload)

    assert response.status_code == 422, response.text

# Нечисловой student_id → 422
async def test_create_subscription_with_non_numeric_student_id_returns_422(teacher_client):
    post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": "asd",
        "start_date": "2026-09-01",
        "end_date": "2026-09-20",
        "price_for_one_lesson": 0,
        "is_paid": False
    })

    assert post_response.status_code == 422, post_response.text

# Некорректный формат даты → 422
async def test_create_subscription_with_invalid_date_format_returns_422(created_solo_student_and_lesson, teacher_client):
    student_id = created_solo_student_and_lesson["student_id"]

    post_response = await teacher_client.post("/subscriptions/", json={
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

# ─── Получение списка — GET /subscriptions/ ───

# Без фильтров → все абонементы
async def test_get_subscriptions_returns_200(created_solo_student_many_lessons_and_many_subscriptions, teacher_client):
    response = await teacher_client.get("/subscriptions/")

    assert response.status_code == 200, response.text
    assert len(response.json()) == 2

# is_active=true → только те, где start_date <= today <= end_date
async def test_get_subscriptions_with_active_filter_returns_only_active(created_solo_student_many_lessons_and_many_subscriptions, teacher_client):
    expired_sub, active_sub = created_solo_student_many_lessons_and_many_subscriptions

    response = await teacher_client.get("/subscriptions/", params={"is_active": True})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == active_sub["id"]

# is_active=false → только просроченные/ещё не начавшиеся
async def test_get_subscriptions_with_inactive_filter_returns_only_inactive(created_solo_student_many_lessons_and_many_subscriptions, teacher_client):
    expired_sub, active_sub= created_solo_student_many_lessons_and_many_subscriptions

    response = await teacher_client.get("/subscriptions/", params={"is_active": False})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == expired_sub["id"]


# is_paid=true / is_paid=false
@pytest.mark.parametrize("is_paid", [True, False])
async def test_get_subscriptions_with_is_paid_filter_returns_matching(is_paid, created_solo_student_many_lessons_and_many_subscriptions, teacher_client):
    response = await teacher_client.get("/subscriptions/", params={"is_paid": is_paid})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["is_paid"] == is_paid

# Комбинация is_active + is_paid
async def test_get_subscriptions_with_active_and_paid_filters_returns_matching(
    created_solo_student_many_lessons_and_many_subscriptions, teacher_client
):
    start_date = (today() - timedelta(days=5)).isoformat()
    end_date = (today() + timedelta(days=5)).isoformat()

    other_student_response = await teacher_client.post("/students/", json={
        "first_name": "Второй",
        "last_name": "Ученик",
        "number_of_class": 7,
        "phone": "+79990000002",
        "parent_name": "Родитель2",
        "parent_phone": "+79990000003",
        "notes": None,
        "is_active": True
    })
    assert other_student_response.status_code == 201, other_student_response.text
    other_student_id = other_student_response.json()["id"]

    other_lesson_response = await teacher_client.post("/lessons/", json={
        "student_id": other_student_id,
        "day": 2,
        "time_start": "10:00:00",
        "time_end": "11:00:00"
    })
    assert other_lesson_response.status_code == 201, other_lesson_response.text

    third_subscription = await teacher_client.post("/subscriptions/", json={
        "student_id": other_student_id,
        "start_date": start_date,
        "end_date": end_date,
        "price_for_one_lesson": 1000,
        "is_paid": True
    })
    assert third_subscription.status_code == 201, third_subscription.text

    response = await teacher_client.get("/subscriptions/", params={"is_paid": True, "is_active": True})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == third_subscription.json()["id"]

# Пустой список, если абонементов нет → 200, []
async def test_get_subscriptions_empty_returns_200(created_solo_student, teacher_client):
    response = await teacher_client.get("/subscriptions/")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 0

# Без авторизации → 401
async def test_get_subscriptions_without_auth_returns_401(client):
    response = await client.get("/subscriptions/")
    assert response.status_code == 401

# ─── Получение по id — GET /subscriptions/{id} ───

# Успешное получение → 200
async def test_get_subscription_by_id_returns_200(created_solo_student_many_lessons_and_subscription, teacher_client):
    sub_id = created_solo_student_many_lessons_and_subscription["id"]

    response = await teacher_client.get(f"/subscriptions/{sub_id}")
    assert response.status_code == 200, response.text
    assert response.json()["id"] == sub_id

# Несуществующий id → 404
async def test_get_subscription_by_nonexistent_id_returns_404(teacher_client):

    response = await teacher_client.get("/subscriptions/1")
    assert response.status_code == 404, response.text

# Нечисловой id → 422
async def test_get_subscription_by_non_numeric_id_returns_422(teacher_client):
    response = await teacher_client.get("/subscriptions/asd")
    assert response.status_code == 422, response.text

# Без авторизации → 401
async def test_get_subscription_by_id_without_auth_returns_401(client):
    response = await client.get("/subscriptions/1")
    assert response.status_code == 401, response.text

# ─── Обновление — PATCH /subscriptions/{id} ───

# Обновление одного поля (is_paid) → 200, остальное не тронуто, planned_lessons/total_price не пересчитываются (регрессия на need_recalculate)
async def test_update_subscription_is_paid_only_does_not_recalculate(created_solo_student_many_lessons_and_subscription, teacher_client):
    sub_id = created_solo_student_many_lessons_and_subscription["id"]
    
    response = await teacher_client.patch(f"/subscriptions/{sub_id}", json={
        "is_paid": False
    })

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["is_paid"] == False
    assert body["planned_lessons"] == created_solo_student_many_lessons_and_subscription["planned_lessons"]
    assert body["total_price"] == created_solo_student_many_lessons_and_subscription["total_price"]


# Обновление нескольких полей сразу
async def test_update_subscription_multiple_fields_returns_200(created_solo_student_many_lessons_and_subscription, teacher_client):
    sub_id = created_solo_student_many_lessons_and_subscription["id"]
    original_planned_lessons = created_solo_student_many_lessons_and_subscription["planned_lessons"]
    price = created_solo_student_many_lessons_and_subscription["price_for_one_lesson"]

    response = await teacher_client.patch(f"/subscriptions/{sub_id}", json={
        "start_date": "2026-09-02",
        "is_paid": False
    })

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["start_date"] == "2026-09-02"
    assert body["is_paid"] == False

    # start_date сдвинулся вперёд → пересчёт planned_lessons/total_price
    # должен сработать даже вместе с другим полем (is_paid), а не только
    # когда меняются исключительно даты
    assert body["planned_lessons"] <= original_planned_lessons
    expected_total = Decimal(body["planned_lessons"]) * Decimal(price)
    assert body["total_price"] == str(expected_total)

# Пустое тело {} → 200, ничего не меняется
async def test_update_subscription_with_empty_body_returns_200(created_solo_student_many_lessons_and_subscription, teacher_client):
    sub_id = created_solo_student_many_lessons_and_subscription["id"]
    
    response = await teacher_client.patch(f"/subscriptions/{sub_id}", json={})

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["start_date"] == created_solo_student_many_lessons_and_subscription["start_date"]
    assert body["end_date"] == created_solo_student_many_lessons_and_subscription["end_date"]
    assert body["is_paid"] == created_solo_student_many_lessons_and_subscription["is_paid"]
    assert body["planned_lessons"] == created_solo_student_many_lessons_and_subscription["planned_lessons"]
    assert body["total_price"] == created_solo_student_many_lessons_and_subscription["total_price"]

# Обновление несуществующего абонемента → 404
async def test_update_nonexistent_subscription_returns_404(teacher_client):
    response = await teacher_client.patch("/subscriptions/1", json={})
    assert response.status_code == 404

# Нечисловой id → 422
async def test_update_subscription_with_non_numeric_id_returns_422(teacher_client):
    response = await teacher_client.patch("/subscriptions/asd", json={})
    assert response.status_code == 422

# student_id → несуществующий ученик → 404
async def test_update_subscription_with_nonexistent_student_returns_404(created_solo_student_many_lessons_and_subscription, teacher_client):
    sub_id = created_solo_student_many_lessons_and_subscription["id"]
    student_id = created_solo_student_many_lessons_and_subscription["student_id"]

    response = await teacher_client.patch(f"/subscriptions/{sub_id}", json={
        "student_id": student_id - 1
    })

    assert response.status_code == 404, response.text

# student_id → другой существующий ученик, даты/цена не меняются → пересчёт planned_lessons/total_price по занятиям нового ученика
async def test_update_subscription_change_student_recalculates_by_new_student_lessons(created_two_students_different_weekdays, teacher_client):
    first_student_id, second_student_id = created_two_students_different_weekdays[0]["id"], created_two_students_different_weekdays[1]["id"]
    
    post_student_sub_response = await teacher_client.post("/subscriptions/", json={
        "student_id": first_student_id,
        "start_date": "2026-09-01",
        "end_date": "2026-09-30",
        "price_for_one_lesson": 1000,
        "is_paid": True
    })

    assert post_student_sub_response.status_code == 201, post_student_sub_response.text
    post_body = post_student_sub_response.json()
    assert post_body["planned_lessons"] == 5
    assert post_body["total_price"] == "5000.00"

    post_sub_id = post_body["id"]

    patch_student_sub_response = await teacher_client.patch(f"/subscriptions/{post_sub_id}", json={
        "student_id": second_student_id
    })

    assert patch_student_sub_response.status_code == 200, patch_student_sub_response.text
    patch_body = patch_student_sub_response.json()
    assert patch_body["planned_lessons"] == 4
    assert patch_body["total_price"] == "4000.00"

# Изменение price_for_one_lesson → пересчитывается только total_price, planned_lessons не меняется
async def test_update_subscription_price_recalculates_total_price_only(created_solo_student_many_lessons_and_subscription, teacher_client):
    sub_id = created_solo_student_many_lessons_and_subscription["id"]

    response = await teacher_client.patch(f"/subscriptions/{sub_id}", json={
        "price_for_one_lesson": "2000.00"
    })

    assert response.status_code == 200, response.text
    body = response.json()

    assert body["planned_lessons"] == created_solo_student_many_lessons_and_subscription["planned_lessons"]
    expected_total = Decimal(body["planned_lessons"]) * Decimal("2000.00")
    assert body["total_price"] == str(expected_total)

# Изменение start_date/end_date → пересчёт обоих полей
async def test_update_subscription_dates_recalculates_planned_lessons_and_total_price(created_solo_student_many_lessons_and_subscription, teacher_client):
    sub_id = created_solo_student_many_lessons_and_subscription["id"]

    response = await teacher_client.patch(f"/subscriptions/{sub_id}", json={
        "start_date": "2026-09-02",
        "end_date": "2026-09-29"
    })

    assert response.status_code == 200, response.text

    body = response.json()

    assert body["planned_lessons"] == 12
    expected_total = Decimal(body["planned_lessons"]) * Decimal("1000.00")
    assert body["total_price"] == str(expected_total)

# Передан только start_date, без end_date — получившийся интервал (новый start + старый end) невалиден → 409 (InvalidDatesInetvalError), не 422!
async def test_update_subscription_start_date_only_invalid_interval_returns_409(created_solo_student_many_lessons_and_subscription, teacher_client):
    sub_id = created_solo_student_many_lessons_and_subscription["id"]

    response = await teacher_client.patch(f"/subscriptions/{sub_id}", json={
        "start_date": "2026-09-30"
    })

    assert response.status_code == 409, response.text

# Передан только end_date, получившийся интервал невалиден → 409
async def test_update_subscription_end_date_only_invalid_interval_returns_409(created_solo_student_many_lessons_and_subscription, teacher_client):
    sub_id = created_solo_student_many_lessons_and_subscription["id"]

    response = await teacher_client.patch(f"/subscriptions/{sub_id}", json={
        "end_date": "2026-08-30"
    })

    assert response.status_code == 409, response.text

# Обновление дат создаёт пересечение с другим абонементом того же ученика → 409
async def test_update_subscription_creates_intersection_with_other_subscription_returns_409(created_solo_student_many_lessons_and_many_subscriptions, teacher_client):
    first_sub, second_sub = created_solo_student_many_lessons_and_many_subscriptions
    second_sub_id = second_sub["id"]

    response = await teacher_client.patch(f"/subscriptions/{second_sub_id}", json={
        "start_date": first_sub["start_date"],
        "end_date": first_sub["end_date"]
    })

    assert response.status_code == 409, response.text

# Обновление дат не создаёт ложное пересечение с самим собой (exclude_id работает) → 200
async def test_update_subscription_without_touching_dates_does_not_trigger_self_intersection(created_solo_student_many_lessons_and_subscription, teacher_client):
    sub_id = created_solo_student_many_lessons_and_subscription["id"]
    response = await teacher_client.patch(f"/subscriptions/{sub_id}", json={
            "start_date": created_solo_student_many_lessons_and_subscription["start_date"],
            "end_date": created_solo_student_many_lessons_and_subscription["end_date"]
        })

    assert response.status_code == 200, response.text

# price_for_one_lesson при обновлении отрицательная → 422
async def test_update_subscription_with_negative_price_returns_422(created_solo_student_many_lessons_and_subscription, teacher_client):
    sub_id = created_solo_student_many_lessons_and_subscription["id"]
    response = await teacher_client.patch(f"/subscriptions/{sub_id}", json={
        "price_for_one_lesson": -1000
    })

    assert response.status_code == 422, response.text

# start_date >= end_date при передаче обоих сразу → 422 (валидатор схемы)
async def test_update_subscription_with_start_after_or_equal_end_returns_422(created_solo_student_many_lessons_and_subscription, teacher_client):
    sub_id = created_solo_student_many_lessons_and_subscription["id"]
    response = await teacher_client.patch(f"/subscriptions/{sub_id}", json={
            "start_date": "2026-08-31",
            "end_date": "2026-08-01"
        })

    assert response.status_code == 422, response.text

# Без авторизации → 401
async def test_update_subscription_without_auth_returns_401(client):
    response = await client.patch("/subscriptions/1", json={})
    assert response.status_code == 401, response.text


# ─── Удаление — DELETE /subscriptions/{id} ───


# Успешное удаление → 204, повторный GET → 404
async def test_delete_subscription_returns_204_and_then_404(created_solo_student_many_lessons_and_subscription, teacher_client):
    sub_id = created_solo_student_many_lessons_and_subscription["id"]
    delete_response = await teacher_client.delete(f"/subscriptions/{sub_id}")

    assert delete_response.status_code == 204, delete_response.text

    get_response = await teacher_client.get(f"/subscriptions/{sub_id}")
    assert get_response.status_code == 404, get_response.text

# Несуществующий id → 404
async def test_delete_nonexistent_subscription_returns_404(teacher_client):
    response = await teacher_client.delete("/subscriptions/1")
    assert response.status_code == 404, response.text

# Нечисловой id → 422
async def test_delete_subscription_with_non_numeric_id_returns_422(teacher_client):
    response = await teacher_client.delete("/subscriptions/asd")
    assert response.status_code == 422, response.text

# Без авторизации → 401
async def test_delete_subscription_without_auth_returns_401(client):
    response = await client.delete("/subscriptions/1")
    assert response.status_code == 401, response.text

# ─── Вложенные эндпоинты в students-роутере ───

# GET /students/{id}/subscriptions — есть абонементы → 200, список
async def test_get_subscriptions_for_student_returns_200(created_solo_student_many_lessons_and_many_subscriptions, teacher_client):
    student_id = created_solo_student_many_lessons_and_many_subscriptions[0]["student_id"]
    response = await teacher_client.get(f"/students/{student_id}/subscriptions")

    assert response.status_code == 200, response.text
    body = response.json()
    assert len(body) == 2

# GET /students/{id}/subscriptions — абонементов нет → 404 (SubscriptionsForStudentNotFound)
async def test_get_subscriptions_for_student_empty_returns_404(created_solo_student_and_lesson, teacher_client):
    student_id = created_solo_student_and_lesson["student_id"]
    response = await teacher_client.get(f"/students/{student_id}/subscriptions")

    assert response.status_code == 404, response.text

# GET /students/{id}/subscriptions — несуществующий ученик → 404
async def test_get_subscriptions_for_nonexistent_student_returns_404(teacher_client):
    response = await teacher_client.get("/students/1/subscriptions")

    assert response.status_code == 404, response.text

# GET /students/{id}/subscriptions — без авторизации → 401
async def test_get_subscriptions_for_student_without_auth_returns_401(client):
    response = await client.get("/students/1/subscriptions")

    assert response.status_code == 401, response.text

# GET /students/{id}/current-subscription — есть активный → 200
async def test_get_current_subscription_for_student_returns_200(created_solo_student_many_lessons_and_many_subscriptions, teacher_client):
    student_id = created_solo_student_many_lessons_and_many_subscriptions[0]["student_id"]

    response = await teacher_client.get(f"/students/{student_id}/current-subscription")
    assert response.status_code == 200, response.text

# GET /students/{id}/current-subscription — абонемент есть, но истёк/ещё не начался → 404 (SubscriptionActiveNotFound)
async def test_get_current_subscription_for_student_without_active_returns_404(created_solo_student_and_many_lessons, teacher_client):
    student_id = created_solo_student_and_many_lessons[0]["student_id"]

    post_response = await teacher_client.post("/subscriptions/", json={
        "student_id": student_id,
        "start_date": "2026-08-01",
        "end_date": "2026-08-31",
        "price_for_one_lesson": 1000,
        "is_paid": True
    })

    assert post_response.status_code == 201, post_response.text

    get_response = await teacher_client.get(f"/students/{student_id}/current-subscription")
    assert get_response.status_code == 404, get_response.text

# GET /students/{id}/current-subscription — несуществующий ученик → 404
async def test_get_current_subscription_for_nonexistent_student_returns_404(teacher_client):
    response = await teacher_client.get("/students/1/current-subscription")
    assert response.status_code == 404, response.text

# GET /students/{id}/current-subscription — без авторизации → 401
async def test_get_current_subscription_for_student_without_auth_returns_401(client):

    response = await client.get("/students/1/current-subscription")
    assert response.status_code == 401, response.text

# GET /students/{id}/subscriptions — нечисловой id -> 422
async def test_get_subscriptions_for_student_with_non_numeric_id_returns_422(teacher_client):
    response = await teacher_client.get("/students/asd/subscriptions")

    assert response.status_code == 422, response.text

# GET /students/{id}/current-subscription — нечисловой id -> 422
async def test_get_current_subscription_for_student_with_non_numeric_id_returns_422(teacher_client):
    response = await teacher_client.get("/students/asd/current-subscription")

    assert response.status_code == 422, response.text

#Обнуление обязательного поля в patch
@pytest.mark.parametrize("field", ["student_id", "start_date", "end_date", "price_for_one_lesson", "is_paid"])
async def test_update_subscription_with_null_required_field_returns_422(field, teacher_client, created_solo_student_many_lessons_and_subscription):
    subscription_id = created_solo_student_many_lessons_and_subscription["id"]
    response = await teacher_client.patch(f"/subscriptions/{subscription_id}", json={
        field: None
    })

    assert response.status_code == 422, response.text