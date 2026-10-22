import json

import pytest
import requests

from config import url_order, url_courier, url_login, url_accept_order, url_get_order_id


class TestOrders:
    @pytest.mark.parametrize("color", [["BLACK", "GREY"], ["BLACK"], ["GREY"], []])
    def test_color(self, color):
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
        resp = requests.post(url_order, json.dumps(body))
        assert resp.status_code == 201
        assert "track" in resp.json()


class TestListOrders:
    courier_id: str = None

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def set_up_test(cls):
        payload = {
            "login": "test1",
            "password": "123",
        }
        resp_create_user = requests.post(url_courier, data=payload)
        resp_login_user = requests.post(url_login, data=payload)
        cls.courier_id = str(resp_login_user.json()['id'])
        yield

        body = {
            "login": "test1",
            "password": "123"
        }
        resp = requests.post(url_login, body)
        if resp.status_code == 200:
            id = resp.json()['id']
            url_delete = url_courier + f"/{id}"
            resp = requests.delete(url_delete)
            pass

    def test_get_list_orders(self):
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
        resp = requests.post(url_order, json.dumps(body))
        if resp.status_code != 201:
            assert False
        order_track = resp.json()['track']

        resp_with_id = requests.get(url_get_order_id.format(track=order_track))
        if resp_with_id.status_code != 200:
            assert False
        order_id = resp_with_id.json()['order']['id']

        resp_accepted = requests.put(url_accept_order.format(order_id=order_id) + f"?courierId={self.courier_id}")
        if resp_accepted.status_code != 200:
            assert False

        resp_with_list = requests.get(url_order, params={'courierId': self.courier_id})
        if resp_with_list.status_code != 200:
            assert False

        assert any(item['id'] == order_id for item in resp_with_list.json()['orders'])
