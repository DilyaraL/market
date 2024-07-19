from django.db.models import Count
from django.views.generic.base import ContextMixin

from catalog.models import *


menu = [
    {
    'title': "О сайте",
    'url_name': 'home'
    }
]


class DataMixin(ContextMixin):
    paginate_by = 4

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('products'))

        user_menu = menu.copy()

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Список заказов")
        context.update(c_def)
        return context