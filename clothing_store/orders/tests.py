from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import Products


class GetOrdersTestCase(TestCase):
    def setUp(self):
        "Инициализация перед выполнением каждого теста"

    def test_redirect_create_order(self):
        path = reverse('orders:create_order')
        redirect_uri = reverse('users:login')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_form_create_order_error(self):
        product = Products.objects.create(name='Test Product', quantity=10, price=10.0)

        data = {
            'address': 'jgjhgj',
            'phone': '534543534',
            'orderitem_set-0-product': product.pk,
            'orderitem_set-0-quantity': -1,
            'orderitem_set-TOTAL_FORMS': '1',
            'orderitem_set-INITIAL_FORMS': '0',
            'orderitem_set-MIN_NUM_FORMS': '0',
            'orderitem_set-MAX_NUM_FORMS': '1000',
        }

        path = reverse('orders:create_order')
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST) # Не уверена, что такая ошибка
        self.assertContains(response, "Количество должно быть больше 0")

    def tearDown(self):
        "Действия после выполнения каждого теста"
