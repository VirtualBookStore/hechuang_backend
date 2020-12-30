import json
from time import time

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

# Create your tests here.
from rest_framework.response import Response
from rest_framework.test import APIClient

from book.models import Book
from order.models import Order
User = get_user_model()

class AllTest(TestCase):
    @staticmethod
    def _print_res(response: Response):
        print(json.dumps(response.json(enconding='utf-8'), indent=4,encoding='utf-8'))


    @staticmethod
    def _make_test(client: APIClient, method: str, path: str, data: dict = {}):
        method = method.lower()
        if method == 'get':
            response = client.get(path, data=data)
        elif method == 'post':
            response = client.post(path, data=data)
        elif method == 'patch':
            response = client.patch(path, data=data)
        elif method == 'put':
            response = client.put(path, data=data)
        else:
            response = client.delete(path, data=data)
        print(json.dumps(response.json(), indent=4))
        return response

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command('loaddata', 'data.yaml', verbosity=0)

    def setUp(self) -> None:
        self.customer_client = APIClient()
        self.customer_client.login(username='rand1925', password='rand1925')

        self.admin_client = APIClient()
        self.admin_client.login(username='admin', password='admin123')

    def test_post_save(self):
        isbn = '7302244752'
        book = Book.objects.get(isbn=isbn)
        orders = Order.objects.filter(book=book)
        print(Order.objects.filter(book=book).first())
        response_post_save = self._make_test(self.admin_client, 'patch', f'/api/v1/book/{isbn}/', data={
            'new_total': 0
        })
        book = Book.objects.get(isbn=isbn)
        print(Order.objects.filter(book=book).filter(status=Order.OrderStatus.OUT_OF_STOCK).all())

    def test_list_recycle(self):
        orders = Order.objects.filter(status=100)
        response_allow_true = self._make_test(self.admin_client, 'get', '/api/v1/order/?status=30')

    def test_list_recycle_saus(self):
        response_list_recycle = self._make_test(self.customer_client, 'get', '/api/v1/profile/')


    def test_list_recycle_satus(self):
        response_list_recycle = self._make_test(self.admin_client, 'get', '/api/v1/recycle/?status=100')

    def test_list_book(self):
        response_list_book = self._make_test(self.customer_client, 'get', '/api/v1/book/')

    def test_purchase(self):
        response_purchase = self._make_test(self.customer_client, 'post', '/api/v1/book/7302244752/purchase/', data={
            'old': False,
            'total': 1
        })
        response_order_mine = self._make_test(self.customer_client, 'get', '/api/v1/order/')
        all_orders = response_order_mine.data
        order = all_orders[-1]
        order_id = order['id']
        response_order_detail = self._make_test(self.customer_client, 'get', f'/api/v1/order/{order_id}/')
        response_order_pay = self._make_test(self.customer_client, 'patch', f'/api/v1/order/{order_id}/pay/')

        response_list_paid = self._make_test(self.admin_client, 'get', f'/api/v1/order/?status=40')
        response_order_receive = self._make_test(self.customer_client, 'patch', f'/api/v1/order/{order_id}/receive/')
        response_order_recycle_request = self._make_test(self.customer_client, 'post',
                                                         f'/api/v1/order/{order_id}/recycle/',
                                                         data={"message": "申请回收"})
        response_order_recycle_check = self._make_test(self.admin_client, 'patch',
                                                         f'/api/v1/order/{order_id}/recycle/check/',
                                                         data={"allowed": True})
        response_order_recycle_receive = self._make_test(self.admin_client, 'patch',
                                                       f'/api/v1/order/{order_id}/recycle/receive/')

        response_noti = self._make_test(self.customer_client, 'get', '/api/v1/notification/')
        response_noti = self._make_test(self.admin_client, 'get', '/api/v1/notification/')
        print(response_noti.data)