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