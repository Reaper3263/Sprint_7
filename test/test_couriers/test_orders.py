import allure
import pytest
import requests

from config import url_order, url_accept_order, url_get_order_id


class TestOrders:
    @allure.title("Создание заказа с различными цветами: {color}")
    @pytest.mark.parametrize("color", [["BLACK", "GREY"], ["BLACK"], ["GREY"]])
    def test_color_creation_status_code(self, color):
        body = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": color
        }
        with allure.step("Отправка запроса на создание заказа"):
            resp = requests.post(url_order, json=body)

        with allure.step("Проверка статус-кода 201"):
            assert resp.status_code == 201


@pytest.mark.usefixtures("manage_courier")
class TestListOrders:
    courier_id: str = None

    @allure.title("Проверка отображения привязанного заказа в списке курьера")
    def test_get_list_orders_contains_courier_order(self):
        body = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2026-10-21",
            "comment": "Saske, come back to Konoha",
            "color": ['BLACK']
        }
        with allure.step("Создание нового заказа"):
            resp = requests.post(url_order, json=body)
            order_track = resp.json()['track']

        with allure.step("Получение числового ID заказа по его трек-номеру"):
            resp_with_id = requests.get(url_get_order_id.format(track=order_track))
            order_id = resp_with_id.json()['order']['id']

        with allure.step("Привязка созданного заказа к курьеру"):
            url_accept = url_accept_order.format(order_id=order_id)
            requests.put(url_accept, params={'courierId': self.courier_id})

        with allure.step("Запрос списка заказов курьера"):
            resp_with_list = requests.get(url_order, params={'courierId': self.courier_id})

        with allure.step("Проверка, что ID заказа присутствует в ответе"):
            assert any(item['id'] == order_id for item in resp_with_list.json()['orders'])