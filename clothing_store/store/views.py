from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from .forms import OrderForm
from .models import *
from .utils import *


class Home(DataMixin, TemplateView):
    template_name = 'store/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context.update(c_def)
        return context


class Product(DataMixin, ListView):
    model = Products
    template_name = 'store/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        cat_slug = self.kwargs.get('cat_slug')
        if cat_slug:
            return Products.objects.filter(category__slug=cat_slug)
        else:
            return Products.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_slug = self.kwargs.get('cat_slug')
        if cat_slug:
            category = Category.objects.filter(slug=cat_slug).first()
            cat_selected = category.id if category else 0
            c_def = self.get_user_context(title='Категория - ' + str(category.name), cat_selected=cat_selected)
        else:
            c_def = self.get_user_context(title='Все продукты', cat_selected=0)
        context.update(c_def)
        return context


class ShowProduct(DataMixin, DetailView):
    model = Products
    template_name = 'store/product.html'
    context_object_name = 'product'

    def get_object(self):
        return Products.objects.get(slug=self.kwargs['prod_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['product'].name)
        context.update(c_def)
        return context


class ShowOrder(DataMixin, DetailView):
    model = Order
    template_name = 'store/order.html'
    context_object_name = 'order'

    def get_object(self):
        order = Order.objects.get(pk=self.kwargs['pk'])
        return order

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Заказ")
        context.update(c_def)
        return context


class Orders(DataMixin, ListView):
    model = Order
    template_name = 'store/orders.html'
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


class CreateOrderView(View):

    def get(self, request):
        form = OrderForm()
        return render(request, 'store/create_order.html', {'form': form})

    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.customer = request.user  # предполагается, что пользователь аутентифицирован
                order.price = order.product.price * order.quantity  # предполагается, что цена продукта хранится в объекте product
                order.product.quantity -= order.quantity
                order.product.save()
                order.save()
                return redirect('orders')  # перенаправление на страницу с заказами после успешного создания
        return render(request, 'store/create_order.html', {'form': form})


class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'store/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        context.update(c_def)
        return context


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'store/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        context.update(c_def)
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
