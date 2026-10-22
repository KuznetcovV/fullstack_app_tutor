import pytest

async def test_create_cancelled_lesson_returns_201(teacher_client, created_solo_student_and_many_lessons):
    first_lesson_id = created_solo_student_and_many_lessons[0]["id"]
    response = await teacher_client.post("/cancelled-lessons/", json={
        "lesson_id": first_lesson_id,
        "lesson_date": "2026-10-20"
    })

    assert response.status_code == 201, response.text
    body = response.json()

    assert "id" in body
    assert body["lesson_id"] == first_lesson_id, response.text
    assert body["lesson_date"] == "2026-10-20", response.text

async def test_create_cancelled_lesson_for_nonexistent_lesson_returns_404(teacher_client):
    response = await teacher_client.post("/cancelled-lessons/", json={
        "lesson_id": 999999,
        "lesson_date": "2026-10-20"
    })

    assert response.status_code == 404, response.text

async def test_create_cancelled_lesson_with_wrong_weekday_returns_422(teacher_client, created_solo_student_and_lesson):
    lesson_id = created_solo_student_and_lesson["id"]
    response = await teacher_client.post("/cancelled-lessons/", json={
        "lesson_id": lesson_id,
        "lesson_date": "2026-10-21"
    })

    assert response.status_code == 422, response.text

async def test_create_duplicate_cancelled_lesson_returns_409(teacher_client, created_solo_student_and_lesson):
    lesson_id = created_solo_student_and_lesson["id"]
    first_response = await teacher_client.post("/cancelled-lessons/", json={
        "lesson_id": lesson_id,
        "lesson_date": "2026-10-20"
    })

    assert first_response.status_code == 201, first_response.text

    second_response = await teacher_client.post("/cancelled-lessons/", json={
        "lesson_id": lesson_id,
        "lesson_date": "2026-10-20"
    })

    assert second_response.status_code == 409, second_response.text

@pytest.mark.parametrize("payload", [
    {},
    {"lesson_id": 1},
    {"lesson_date": "2026-10-20"}
    ])
async def test_create_cancelled_lesson_without_required_fields_returns_422(payload, teacher_client):
    response = await teacher_client.post("/cancelled-lessons/", json=payload)
    assert response.status_code == 422, response.text

async def test_create_cancelled_lesson_with_invalid_date_format_returns_422(teacher_client, created_solo_student_and_lesson):
    lesson_id = created_solo_student_and_lesson["id"]
    response = await teacher_client.post("/cancelled-lessons/", json={
        "lesson_id": lesson_id,
        "lesson_date": "20-2026-10"
    })

    assert response.status_code == 422, response.text


async def test_get_cancelled_lessons_returns_list(created_lessons_and_cancelled_lessons, teacher_client):
    expected_id = {item["id"] for item in created_lessons_and_cancelled_lessons}
    response = await teacher_client.get("/cancelled-lessons/")
    assert response.status_code == 200, response.text

    body = response.json()
    assert len(body) == 3
    assert {item["id"] for item in body} == expected_id

async def test_get_cancelled_lessons_returns_empty_list_when_none_exist(teacher_client):
    response = await teacher_client.get("/cancelled-lessons/")
    assert response.status_code == 200, response.text
    assert response.json() == []

async def test_get_cancelled_lessons_filtered_by_lesson_id(created_lessons_and_cancelled_lessons, teacher_client):
    lesson_id = created_lessons_and_cancelled_lessons[0]["lesson_id"]

    response = await teacher_client.get("/cancelled-lessons/", params={
        "lesson_id": lesson_id
    })

    assert response.status_code == 200, response.text
    body = response.json()

    assert len(body) == 1, response.text
    assert body[0]["lesson_id"] == lesson_id

