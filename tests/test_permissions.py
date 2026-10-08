import pytest

CRM_ENDPOINTS = [
    ('get', '/students/'),
    ('get', '/students/1'),
    ('get', '/students/search'),
    ('post', '/students/'),
    ('patch', '/students/1'),
    ('delete', '/students/1'),
    ('get', '/lessons/'),
    ('get', '/lessons/today'),
    ('get', '/lessons/1'),
    ('post', '/lessons/'),
    ('patch', '/lessons/1'),
    ('delete', '/lessons/1'),
    ('get', '/lesson-logs/'),
    ('get', '/lesson-logs/1'),
    ('post', '/lesson-logs/'),
    ('patch', '/lesson-logs/1'),
    ('delete', '/lesson-logs/1'),
    ('get', '/subscriptions/'),
    ('get', '/subscriptions/1'),
    ('post', '/subscriptions/'),
    ('patch', '/subscriptions/1'),
    ('delete', '/subscriptions/1'),
    ]


@pytest.mark.parametrize("method, url", CRM_ENDPOINTS)
async def test_student_has_no_access_to_crm(method, url, student_client):
    response = await student_client.request(method, url)
    assert response.status_code == 403, response.text

@pytest.mark.parametrize("method, url", CRM_ENDPOINTS)
async def test_admin_has_access_to_crm(method, url, admin_client):
    response = await admin_client.request(method, url)
    assert response.status_code != 403, response.text

@pytest.mark.parametrize("method, url", CRM_ENDPOINTS)
async def test_teacher_has_access_to_crm(method, url, teacher_client):
    response = await teacher_client.request(method, url)
    assert response.status_code != 403, response.text

@pytest.mark.parametrize("role", ["teacher", "admin"])
async def test_register_ignores_role_field_and_creates_student(role, client):
    
    response = await client.post("/auth/register", json={
        "login": role,
        "password": "strongpassword123",
        "role": "teacher"
    })

    assert response.status_code == 200, response.text

    body = response.json()
    access_token = body["access_token"]

    get_response = await client.get("/students/", headers={"Authorization": f"Bearer {access_token}"})

    assert get_response.status_code == 403, get_response.text
