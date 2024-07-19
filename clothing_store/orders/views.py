from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import OrderForm, OrderItemFormSet
from .models import *
from users.utils import *

from catalog.models import Products


class ShowOrder(DataMixin, DetailView):
    model = Order
    template_name = 'orders/order.html'
    context_object_name = 'order'

    def get_object(self):
        return Order.objects.filter(pk=self.kwargs['pk']).first()

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


    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        order_form = OrderForm()
        order_item_formset = OrderItemFormSet()
        context = self.get_context_data(order_form=order_form, order_item_formset=order_item_formset)
        return render(request, 'orders/create_order.html', context)

    def post(self, request):
        order_form = OrderForm(request.POST)
        order_item_formset = OrderItemFormSet(request.POST)
        if order_form.is_valid() and order_item_formset.is_valid():
            try:
                with transaction.atomic():
                    order = order_form.save(commit=False)
                    if request.user.is_authenticated:
                        order.customer = request.user
                        order.save()
                    else:
                        return redirect('users:login')

                    order_items = order_item_formset.save(commit=False)

                    product_quantities = {}

                    for item in order_items:
                        item.order = order
                        item.price = item.product.price * item.quantity  # расчет стоимости продукта в заказе

                        # Обновляем количество продуктов
                        if item.product.id in product_quantities:
                            product_quantities[item.product.id] += item.quantity
                        else:
                            product_quantities[item.product.id] = item.quantity

                    for product_id, quantity in product_quantities.items():
                        product = Products.objects.get(id=product_id)
                        if product.quantity < quantity:
                            raise ValidationError(f'Недостаточное количество продукта "{product.name}" на складе.')

                    # Сохраняем все items после проверки доступного количества
                    for item in order_items:
                        item.save()

                    # Обновляем количество продуктов на складе
                    for product_id, quantity in product_quantities.items():
                        product = Products.objects.get(id=product_id)
                        product.quantity -= quantity
                        product.save()

                    return redirect('orders:orders')  # перенаправление на страницу с заказами после успешного создания

            except ValidationError as e:
                # seen_products = set()
                # for item in order_item_formset.forms:
                #     if item.cleaned_data and not item.cleaned_data.get('DELETE'):
                #         product_id = item.cleaned_data['product'].id
                #         if product_id in seen_products:
                #             item.cleaned_data['DELETE'] = True
                #         else:
                #             item.cleaned_data['quantity'] = 1
                #             seen_products.add(product_id)

                context = self.get_context_data(order_form=order_form, order_item_formset=OrderItemFormSet(), error=e.message)
                return render(request, 'orders/create_order.html', context)

        context = self.get_context_data(order_form=order_form, order_item_formset=order_item_formset)
        return render(request, 'orders/create_order.html', context)

