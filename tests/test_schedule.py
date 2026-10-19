

async def test_schedule_for_one_day_returns_lesson_of_that_weekday(teacher_client, created_solo_student):

    post_response = await teacher_client.post("/lessons/", json={
        "student_id": created_solo_student["id"],
        "day": 0,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })
    assert post_response.status_code == 201, post_response.text

    response = await teacher_client.get("/schedule/", params={"date_from": "2026-10-19"})
    assert response.status_code == 200, response.text
    body = response.json()
    assert len(body) == 1, response.text
    first_lesson = body[0]

    assert first_lesson["lesson_date"] == "2026-10-19", response.text
    assert first_lesson["lesson_id"] == post_response.json()["id"], response.text
    assert first_lesson["time_start"] == "12:00:00", response.text
    assert first_lesson["time_end"] == "13:00:00", response.text
