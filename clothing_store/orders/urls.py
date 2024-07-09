from django.urls import path, re_path

from .views import *

app_name = 'orders'

urlpatterns = [
    path('<int:pk>/', ShowOrder.as_view(), name='one_order'),
    path('', Orders.as_view(), name='orders'),
    path('create/', CreateOrderView.as_view(), name='create_order'),

]
