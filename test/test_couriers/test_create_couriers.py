import allure
import pytest
import requests

from config import url_login, url_courier
from test.test_data import courier_1_username, courier_2_username, courier_3_username, password


@pytest.mark.usefixtures("clean_data_before_test")
class TestCreateCourier:
    @allure.title("Запрос авторизации несуществующего пользователя возвращает 404")
    def test_check_exist_username_returns_error_message(self):
        body = {"login": courier_1_username, "password": password}
        with allure.step("Отправка запроса авторизации курьера"):
            resp = requests.post(url_login, data=body)

        with allure.step("Проверка сообщения о ненахождении учетной записи"):
            assert resp.json().get('message') == 'Учетная запись не найдена'

    @allure.title("Создание курьера с дублирующимся логином возвращает ошибку")
    def test_create_two_same_username_returns_conflict_message(self):
        payload = {"login": courier_1_username, "password": password, "firstName": "test1"}
        with allure.step("Создание первого курьера"):
            requests.post(url_courier, data=payload)
        with allure.step("Повторная попытка создания курьера с тем же логином"):
            resp_repeated = requests.post(url_courier, data=payload)

        with allure.step("Проверка сообщения о занятом логине"):
            assert resp_repeated.json().get('message') == 'Этот логин уже используется. Попробуйте другой.'

    @allure.title("Создание курьера без пароля возвращает ошибку")
    def test_create_user_without_password_returns_bad_request_message(self):
        payload = {"login": courier_1_username}
        with allure.step("Создание курьера без передачи обязательного поля password"):
            resp = requests.post(url_courier, data=payload)

        with allure.step("Проверка сообщения о недостаточном количестве данных"):
            assert resp.json().get('message') == 'Недостаточно данных для создания учетной записи'

    @allure.title("Успешное создание курьера возвращает статус 201")
    def test_success_creation_new_user_returns_201(self):
        payload = {"login": courier_2_username, "password": password, "firstName": "test1"}
        with allure.step("Отправка корректного запроса на создание курьера"):
            resp = requests.post(url_courier, data=payload)

        with allure.step("Проверка статус-кода 201"):
            assert resp.status_code == 201

    @allure.title("Успешное создание курьера возвращает валидный json-ответ")
    def test_success_creation_new_user_returns_ok_true(self):
        payload = {"login": courier_3_username, "password": password, "firstName": "test1"}
        with allure.step("Отправка корректного запроса на создание курьера"):
            resp = requests.post(url_courier, data=payload)

        with allure.step("Проверка тела ответа на соответствие {'ok': true}"):
            assert resp.text == '{"ok":true}'