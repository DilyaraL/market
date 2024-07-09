from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import OrderForm, OrderItemFormSet
from .models import *
from users.utils import *


class ShowOrder(DataMixin, DetailView):
    model = Order
    template_name = 'orders/order.html'
    context_object_name = 'order'

    def get_object(self):
        return Order.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        order_items = OrderItem.objects.filter(order=order)

        context['order_items'] = order_items
        c_def = self.get_user_context(title="Заказ")
        context.update(c_def)
        return context


class Orders(DataMixin, ListView):
    model = Order
    template_name = 'orders/orders.html'
    context_object_name = 'orders'
    ordering = 'status'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(customer=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Список заказов")
        context.update(c_def)
        return context


class CreateOrderView(DataMixin, View):
    model = Order

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Создание заказа")
        context.update(c_def)
        return context

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        order_form = OrderForm()
        order_item_formset = OrderItemFormSet()
        return render(request, 'orders/create_order.html', {
            'order_form': order_form,
            'order_item_formset': order_item_formset, })

    def post(self, request):
        order_form = OrderForm(request.POST)
        order_item_formset = OrderItemFormSet(request.POST)
        if order_form.is_valid() and order_item_formset.is_valid():
            with transaction.atomic():
                order = order_form.save(commit=False)
                order.customer = request.user  # предполагается, что пользователь аутентифицирован
                order.save()

                order_items = order_item_formset.save(commit=False)

                for item in order_items:
                    item.order = order
                    item.price = item.product.price * item.quantity  # расчет стоимости продукта в заказе

                    # Обновляем количество продуктов
                    item.product.quantity -= item.quantity
                    item.product.save()
                    item.save()
                return redirect('orders:orders')  # перенаправление на страницу с заказами после успешного создания
        return render(request, 'orders/create_order.html', {
            'order_form': order_form,
            'order_item_formset': order_item_formset,
        })


