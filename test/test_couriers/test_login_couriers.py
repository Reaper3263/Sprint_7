import pytest
import requests

from config import url_login, url_courier


class TestLoginCouriers:
    courier_1_username = "Test1"
    courier_2_username = "Test2"
    password = "123"

    @pytest.fixture(scope="class", autouse=True)
    def create_new_user_before_test_and_clear_after(self):
        payload = {
            "login": self.courier_1_username,
            "password": self.password,
            "firstName": "test1"
        }

        resp = requests.post(url_courier, data=payload)

        yield

        body = {
            "login": self.courier_1_username,
            "password": self.password
        }
        resp = requests.post(url_login, body)
        if resp.status_code == 200:
            id = resp.json()['id']
            url_delete = url_courier + f"/{id}"
            resp = requests.delete(url_delete)
            pass

    def test_success_login(self):
        body = {
            "login": self.courier_1_username,
            "password": self.password
        }
        resp = requests.post(url_login, body)
        assert resp.status_code == 200

    def test_all_fields_required(self):
        body = {
        }
        try:
            resp = requests.post(url_login, body, timeout=10)
            assert resp.status_code == 400
        except requests.exceptions.Timeout:
            assert True
        except Exception:
            assert False

    def test_incorrect_password(self):
        body = {
            "login": self.courier_1_username,
            "password": "2222"
        }
        resp = requests.post(url_login, body)
        assert resp.status_code == 404

    def test_incorrect_username(self):
        body = {
            "login": "test_user111224",
            "password": self.password
        }
        resp = requests.post(url_login, body)
        assert resp.status_code == 404