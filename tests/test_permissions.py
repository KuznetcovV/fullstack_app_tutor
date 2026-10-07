import pytest


@pytest.mark.parametrize("method, url", [
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
    ])
async def test_student_has_no_access_to_crm(method, url, student_client):
    response = await student_client.request(method, url)
    assert response.status_code == 403, response.text