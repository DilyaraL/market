from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Products, Category


class ProductListViewTests(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name="Category 1", slug="category-1")
        self.category2 = Category.objects.create(name="Category 2", slug="category-2")

        self.product1 = Products.objects.create(
            name="Product 1",
            slug="product-1",
            quantity=10,
            price=100.0,
            category=self.category1,
            image=SimpleUploadedFile(name='test_image1.jpg', content=b'', content_type='image/jpeg')
        )
        self.product2 = Products.objects.create(
            name="Product 2",
            slug="product-2",
            quantity=7,
            price=20.0,
            category=self.category2,
            image=SimpleUploadedFile(name='test_image2.jpg', content=b'', content_type='image/jpeg')
        )

    def test_product_list(self):
        response = self.client.get(reverse('catalog:products'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)

    def test_product_list_by_category(self):
        response = self.client.get(reverse('catalog:cat_products', kwargs={'cat_slug': 'category-1'}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)