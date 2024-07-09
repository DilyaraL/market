from django.contrib import admin

from .models import *


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'category', 'description', 'get_html_photo')
    fields = ('name', 'slug', 'price', 'category', 'quantity', 'description', 'image', 'get_html_photo')
    readonly_fields = ('get_html_photo',)
    prepopulated_fields = {"slug": ("name",)}

    def get_html_photo(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50>")
        else:
            return "No photo"

    get_html_photo.short_description = "Miniature"


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Products, ProductsAdmin)
