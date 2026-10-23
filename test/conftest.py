import pytest
import requests

from config import url_login, url_courier
from test.test_data import courier_1_username, password, courier_2_username, courier_3_username


@pytest.fixture(scope="class")
def manage_courier(request):
    payload = {
        "login": "test1",
        "password": "123",
    }
    requests.post(url_courier, data=payload)
    resp_login_user = requests.post(url_login, data=payload)

    if request.cls is not None:
        request.cls.courier_id = str(resp_login_user.json()['id'])

    yield

    body = {
        "login": "test1",
        "password": "123"
    }
    resp = requests.post(url_login, data=body)
    if resp.status_code == 200:
        courier_id = resp.json()['id']
        url_delete = f"{url_courier}/{courier_id}"
        requests.delete(url_delete)


@pytest.fixture(scope="class")
def create_new_user_before_test_and_clear_after():
    payload = {
        "login": courier_1_username,
        "password": password,
        "firstName": "test1"
    }

    resp = requests.post(url_courier, data=payload)

    yield

    body = {
        "login": courier_1_username,
        "password": password
    }
    resp = requests.post(url_login, body)
    if resp.status_code == 200:
        id = resp.json()['id']
        url_delete = url_courier + f"/{id}"
        resp = requests.delete(url_delete)
        pass


@pytest.fixture(scope="class")
def clean_data_before_test():
    for user in [courier_1_username, courier_2_username, courier_3_username]:
        body = {
            "login": user,
            "password": password
        }
        resp = requests.post(url_login, body)
        if resp.status_code == 200:
            id = resp.json()['id']
            url_delete = url_courier + f"/{id}"
            resp = requests.delete(url_delete)
            pass
