import datetime

from django.contrib.auth.models import User
from django.db import models

from catalog.models import Products


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('ready', 'Готов'),
        ('received', 'Получен'),
    ]
    ORDER_STATUS_DICT = dict(ORDER_STATUS_CHOICES)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='new')

    def __str__(self):
        return f'Order {self.id} by {self.customer.username}'

    @property
    def status_display(self):
        return self.ORDER_STATUS_DICT.get(self.status)

    @property
    def product_name(self):
        return self.product.name

    @property
    def total_price(self):
        return sum(item.price for item in self.orderitem_set.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.product.name} (x{self.quantity}) for order {self.order.id}'