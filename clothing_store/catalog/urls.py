from django.urls import path, re_path

from .views import *

app_name = 'catalog'

urlpatterns = [
    path('', Product.as_view(), name='products'),
    path('categories/<slug:cat_slug>/', Product.as_view(), name='cat_products'),
    path('<slug:prod_slug>/', ShowProduct.as_view(), name='one_product'),

]
