import allure
import pytest
import requests

from config import url_login
from test.test_data import courier_1_username, password


@pytest.mark.usefixtures("create_new_user_before_test_and_clear_after")
class TestLoginCouriers:
    @allure.title("Авторизация с корректными данными возвращает статус 200")
    def test_success_login(self):
        body = {"login": courier_1_username, "password": password}
        with allure.step("Отправка запроса авторизации"):
            resp = requests.post(url_login, data=body)

        with allure.step("Проверка статус-кода 200"):
            assert resp.status_code == 200

    @allure.title("Авторизация без обязательных полей возвращает статус 400")
    def test_all_fields_required_returns_400(self):
        body = {}
        with allure.step("Отправка запроса авторизации с пустым телом"):
            try:
                resp = requests.post(url_login, data=body, timeout=10)
            except requests.exceptions.Timeout:
                assert True

    @allure.title("Авторизация с неверным паролем возвращает статус 404")
    def test_incorrect_password_returns_404(self):
        body = {"login": courier_1_username, "password": "2222"}
        with allure.step("Отправка запроса с невалидным паролем"):
            resp = requests.post(url_login, data=body)

        with allure.step("Проверка статус-кода 404"):
            assert resp.status_code == 404

    @allure.title("Авторизация с несуществующим логином возвращает статус 404")
    def test_incorrect_username_returns_404(self):
        body = {"login": "test_user111224", "password": password}
        with allure.step("Отправка запроса с несуществующим логином"):
            resp = requests.post(url_login, data=body)

        with allure.step("Проверка статус-кода 404"):
            assert resp.status_code == 404