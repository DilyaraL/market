from django import forms
from django.core.exceptions import ValidationError

from .models import Order, OrderItem


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        product = self.cleaned_data['product']
        if quantity > product.quantity:
            raise ValidationError(f'Максимально возможный заказ {product.quantity}')
        if quantity <= 0:
            raise ValidationError(f'Количество должно быть больше 0')
        return quantity


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'phone']


OrderItemFormSet = forms.models.inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1, can_delete=False)