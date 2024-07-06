import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cat_products', kwargs={'cat_slug': self.slug})


class Products(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products/%Y/%m/%d/')
    quantity = models.IntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")
        else:
            return "Нет фото"

    def get_absolute_url(self):
        return reverse('one_product', kwargs={'slug': self.slug})


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('ready', 'Готов'),
        ('received', 'Получен'),
    ]
    ORDER_STATUS_DICT = dict(ORDER_STATUS_CHOICES)

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='new')

    def __str__(self):
        return f'{self.customer.username} / {self.product.name} / {self.quantity}'

    @property
    def status_display(self):
        return self.ORDER_STATUS_DICT.get(self.status)

    @property
    def product_name(self):
        return self.product.name
