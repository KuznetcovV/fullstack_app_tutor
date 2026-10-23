

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

async def test_schedule_for_two_weeks_repeats_lesson_every_week(teacher_client, created_solo_student):

    post_response = await teacher_client.post("/lessons/", json={
        "student_id": created_solo_student["id"],
        "day": 0,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })
    assert post_response.status_code == 201, post_response.text

    response = await teacher_client.get("/schedule/", params={"date_from": "2026-10-19", "date_to": "2026-11-01"})
    assert response.status_code == 200, response.text
    body = response.json()
    assert len(body) == 2, response.text
    first_lesson = body[0]
    second_lesson = body[1]

    assert first_lesson["lesson_date"] == "2026-10-19", response.text
    assert first_lesson["lesson_id"] == post_response.json()["id"], response.text
    assert first_lesson["time_start"] == "12:00:00", response.text
    assert first_lesson["time_end"] == "13:00:00", response.text

    assert second_lesson["lesson_date"] == "2026-10-26", response.text
    assert second_lesson["lesson_id"] == post_response.json()["id"], response.text
    assert second_lesson["time_start"] == "12:00:00", response.text
    assert second_lesson["time_end"] == "13:00:00", response.text

async def test_schedule_returns_lessons_of_one_day_sorted_by_time(teacher_client, created_solo_student):
    first_post_response = await teacher_client.post("/lessons/", json={
        "student_id": created_solo_student["id"],
        "day": 0,
        "time_start": "15:00:00",
        "time_end": "16:00:00"
    })
    assert first_post_response.status_code == 201, first_post_response.text

    first_lesson_body = first_post_response.json()

    second_post_response = await teacher_client.post("/lessons/", json={
        "student_id": created_solo_student["id"],
        "day": 0,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })
    assert second_post_response.status_code == 201, second_post_response.text

    second_lesson_body = second_post_response.json()

    get_response = await teacher_client.get("/schedule/", params={"date_from": "2026-10-19"})
    assert get_response.status_code == 200, get_response.text

    get_body = get_response.json()
    assert len(get_body) == 2

    assert get_body[0]["lesson_id"] == second_lesson_body["id"], get_response.text
    assert get_body[1]["lesson_id"] == first_lesson_body["id"], get_response.text


async def test_schedule_returns_lessons_sorted_by_date_and_time(teacher_client, created_solo_student):
    first_post_response = await teacher_client.post("/lessons/", json={
        "student_id": created_solo_student["id"],
        "day": 1,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })
    assert first_post_response.status_code == 201, first_post_response.text

    first_lesson_body = first_post_response.json()

    second_post_response = await teacher_client.post("/lessons/", json={
        "student_id": created_solo_student["id"],
        "day": 0,
        "time_start": "14:00:00",
        "time_end": "15:00:00"
    })
    assert second_post_response.status_code == 201, second_post_response.text

    second_lesson_body = second_post_response.json()

    get_response = await teacher_client.get("/schedule/", params={"date_from": "2026-10-19", "date_to": "2026-10-20"})
    assert get_response.status_code == 200, get_response.text

    get_body = get_response.json()
    assert len(get_body) == 2, get_response.text

    assert get_body[0]["lesson_id"] == second_lesson_body["id"], get_response.text
    assert get_body[1]["lesson_id"] == first_lesson_body["id"], get_response.text

async def test_schedule_includes_lessons_of_all_students(teacher_client, created_many_students_many_lessons):
    students_ids = set(created_many_students_many_lessons.keys())
    count_lessons = sum(len(item) for item in created_many_students_many_lessons.values())
    response = await teacher_client.get("/schedule/", params={"date_from": "2026-10-19", "date_to": "2026-10-25"})
    assert response.status_code == 200, response.text
    body = response.json()

    assert len(body) == count_lessons, response.text
    students_ids_from_response = {item["student_id"] for item in body}

    assert students_ids == students_ids_from_response

async def test_schedule_with_date_from_after_date_to_returns_422(teacher_client):
    response = await teacher_client.get("/schedule/", params={
        "date_from": "2026-10-21", "date_to": "2026-10-19"
    })

    assert response.status_code == 422

async def test_schedule_with_too_long_range_returns_422(teacher_client):
    response = await teacher_client.get("/schedule/", params={
        "date_from": "2026-01-21", "date_to": "2026-10-19"
    })

    assert response.status_code == 422

async def test_schedule_with_max_allowed_range_returns_200(teacher_client):
    response = await teacher_client.get("/schedule/", params={
        "date_from": "2026-10-01", "date_to": "2026-10-31"
    })

    assert response.status_code == 200, response.text

async def test_schedule_with_invalid_date_format_returns_422(teacher_client):
    response = await teacher_client.get("/schedule/", params={
        "date_from": "asd"
    })

    assert response.status_code == 422

async def test_schedule_without_date_from_returns_422(teacher_client):
    response = await teacher_client.get("/schedule/")

    assert response.status_code == 422

async def test_schedule_without_auth_returns_401(client):
    response = await client.get("/schedule/")

    assert response.status_code == 401

async def test_schedule_excludes_cancelled_lesson_on_its_date(teacher_client, created_solo_student_and_many_lessons):

    first_lesson_id = created_solo_student_and_many_lessons[0]["id"]
    second_lesson_id = created_solo_student_and_many_lessons[1]["id"]
    third_lesson_id = created_solo_student_and_many_lessons[2]["id"]
    
    first_get_response = await teacher_client.get("/schedule/", params={
        "date_from": "2026-10-19", "date_to": "2026-10-25"
    })

    assert first_get_response.status_code == 200, first_get_response.text
    body = first_get_response.json()
    assert len(body) == 3, first_get_response.text

    assert body[0]["lesson_id"] == first_lesson_id
    assert body[1]["lesson_id"] == second_lesson_id
    assert body[2]["lesson_id"] == third_lesson_id

    post_response = await teacher_client.post("/cancelled-lessons/", json={
        "lesson_id": first_lesson_id,
        "lesson_date": body[0]["lesson_date"]
    })

    assert post_response.status_code == 201, post_response.text

    second_get_response = await teacher_client.get("/schedule/", params={
        "date_from": "2026-10-19", "date_to": "2026-10-25"
    })

    assert second_get_response.status_code == 200, second_get_response.text
    body = second_get_response.json()
    assert len(body) == 2, second_get_response.text
    assert body[0]["lesson_id"] == second_lesson_id
    assert body[1]["lesson_id"] == third_lesson_id