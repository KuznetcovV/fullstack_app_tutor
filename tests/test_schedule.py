

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


async def test_schedule_for_one_day_returns_empty_list_when_no_lesson_on_that_weekday(teacher_client, created_solo_student):
    
    post_response = await teacher_client.post("/lessons/", json={
        "student_id": created_solo_student["id"],
        "day": 0,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })
    assert post_response.status_code == 201, post_response.text
    
    response = await teacher_client.get("/schedule/", params={"date_from": "2026-10-20"})
    assert response.status_code == 200, response.text
    body = response.json()
    assert body == [], response.text


async def test_schedule_for_week_returns_each_lesson_on_its_weekday_date(teacher_client, created_solo_student_and_many_lessons):
    response = await teacher_client.get("/schedule/", params={"date_from": "2026-10-19", "date_to": "2026-10-25"})
    assert response.status_code == 200, response.text
    body = response.json()
    assert len(body) == 3, response.text

    first_lesson = created_solo_student_and_many_lessons[0]
    second_lesson = created_solo_student_and_many_lessons[1]
    third_lesson = created_solo_student_and_many_lessons[2]

    first_lesson_schedule = body[0]
    second_lesson_schedule = body[1]
    third_lesson_schedule = body[2]

    assert first_lesson_schedule["lesson_date"] == "2026-10-20", response.text
    assert first_lesson_schedule["lesson_id"] == first_lesson["id"], response.text
    assert first_lesson_schedule["time_start"] == first_lesson["time_start"], response.text
    assert first_lesson_schedule["time_end"] == first_lesson["time_end"], response.text

    assert second_lesson_schedule["lesson_date"] == "2026-10-22", response.text
    assert second_lesson_schedule["lesson_id"] == second_lesson["id"], response.text
    assert second_lesson_schedule["time_start"] == second_lesson["time_start"], response.text
    assert second_lesson_schedule["time_end"] == second_lesson["time_end"], response.text

    assert third_lesson_schedule["lesson_date"] == "2026-10-24", response.text
    assert third_lesson_schedule["lesson_id"] == third_lesson["id"], response.text
    assert third_lesson_schedule["time_start"] == third_lesson["time_start"], response.text
    assert third_lesson_schedule["time_end"] == third_lesson["time_end"], response.text

