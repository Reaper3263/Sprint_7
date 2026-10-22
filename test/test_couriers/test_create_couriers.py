import pytest
import requests

from config import url_login, url_courier


class TestCreateCourier:
    courier_1_username = "Test123sa"
    courier_2_username = "Test2sad"
    courier_3_username = "Test32312"
    password = "123"

    @pytest.fixture(scope="class", autouse=True)
    def clean_data_before_test(self):
        for user in [self.courier_1_username, self.courier_2_username, self.courier_3_username]:
            body = {
                "login": user,
                "password": self.password
            }
            resp = requests.post(url_login, body)
            if resp.status_code == 200:
                id = resp.json()['id']
                url_delete = url_courier + f"/{id}"
                resp = requests.delete(url_delete)

    def test_check_exist_username(self):
        body = {
            "login": self.courier_1_username,
            "password": self.password
        }
        resp = requests.post(url_login, body)
        if resp.status_code == 404:
            assert resp.json()['message'] == 'Учетная запись не найдена'
        else:
            assert False

    def test_create_two_same_username(self):
        payload = {
            "login": self.courier_1_username,
            "password": self.password,
            "firstName": "test1"
        }

        resp = requests.post(url_courier, data=payload)
        if resp.status_code == 201:
            resp_repeated = requests.post(url_courier, data=payload)

            assert resp_repeated.json()['message'] == 'Этот логин уже используется. Попробуйте другой.'
        else:
            assert False

    def test_create_user_not_all_fields(self):
        payload = {
            "login": self.courier_1_username,
        }

        resp = requests.post(url_courier, data=payload)
        if resp.status_code == 400:
            assert resp.json()['message'] == 'Недостаточно данных для создания учетной записи'
        else:
            assert False
    
    def test_success_creation_new_user_status_code(self):
        payload = {
            "login": self.courier_2_username,
            "password": self.password,
            "firstName": "test1"
        }

        resp = requests.post(url_courier, data=payload)
        if resp.status_code == 201:
            assert resp.status_code == 201
        else:
            assert False

    def test_success_creation_new_user_answer(self):
        payload = {
            "login": self.courier_3_username,
            "password": self.password,
            "firstName": "test1"
        }

        resp = requests.post(url_courier, data=payload)
        if resp.status_code == 201:
            assert resp.text == '{"ok":true}'
        else:
            assert False
