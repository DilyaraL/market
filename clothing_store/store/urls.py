from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('products/', Product.as_view(), name='products'),
    path('products/categories/<slug:cat_slug>/', Product.as_view(), name='сat_products'),
    path('products/<slug:prod_slug>', ShowProduct.as_view(), name='one_product'),
    path('orders/<int:pk>', ShowOrder.as_view()),
    path('orders/', Orders.as_view(), name='orders'),
    path('orders/create/', CreateOrderView.as_view(), name='create_order'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),

]

handler404 = pageNotFound
