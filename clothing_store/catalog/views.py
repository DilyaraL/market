from django.views.generic import ListView, DetailView, TemplateView

from .models import *
from users.utils import DataMixin



class Product(DataMixin, ListView):
    model = Products
    template_name = 'catalog/products.html'
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
    template_name = 'catalog/product.html'
    context_object_name = 'product'

    def get_object(self):
        # лучше использовать filter().first()
        return Products.objects.get(slug=self.kwargs['prod_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['product'].name)
        context.update(c_def)
        return context