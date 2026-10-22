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

async def test_get_cancelled_lesson_by_id_returns_200(created_lessons_and_cancelled_lessons, teacher_client):
    expected = created_lessons_and_cancelled_lessons[0]
    response = await teacher_client.get(f"/cancelled-lessons/{expected["id"]}")

    assert response.status_code == 200, response.text
    assert response.json() == expected

async def test_get_cancelled_lesson_by_id_not_found_returns_404(teacher_client):
    response = await teacher_client.get("/cancelled-lessons/999")
    assert response.status_code == 404, response.text

async def test_delete_cancelled_lesson_returns_204(created_lessons_and_cancelled_lessons, teacher_client):
    cancelled_lesson_id = created_lessons_and_cancelled_lessons[0]["id"]

    response = await teacher_client.delete(f"/cancelled-lessons/{cancelled_lesson_id}")
    assert response.status_code == 204, response.text

async def test_delete_cancelled_lesson_removes_it_from_list(created_lessons_and_cancelled_lessons, teacher_client):
    cancelled_lesson_id = created_lessons_and_cancelled_lessons[0]["id"]

    delete_response = await teacher_client.delete(f"/cancelled-lessons/{cancelled_lesson_id}")
    assert delete_response.status_code == 204, delete_response.text

    get_response = await teacher_client.get(f"/cancelled-lessons/{cancelled_lesson_id}")
    assert get_response.status_code == 404, get_response.text

async def test_delete_cancelled_lesson_not_found_returns_404(teacher_client):
    response = await teacher_client.delete("/cancelled-lessons/999999")
    assert response.status_code == 404, response.text

async def test_delete_cancelled_lesson_allows_cancelling_same_date_again(created_lessons_and_cancelled_lessons, teacher_client):
    cancelled_lesson_id = created_lessons_and_cancelled_lessons[0]["id"]
    first_lesson_id = created_lessons_and_cancelled_lessons[0]["lesson_id"]
    
    delete_response = await teacher_client.delete(f"/cancelled-lessons/{cancelled_lesson_id}")
    assert delete_response.status_code == 204, delete_response.text

    post_response = await teacher_client.post("/cancelled-lessons/", json={
        "lesson_id": first_lesson_id,
        "lesson_date": "2026-10-20"
    })

    assert post_response.status_code == 201, post_response.text