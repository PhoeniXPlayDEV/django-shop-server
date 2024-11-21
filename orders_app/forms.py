from django import forms
from django.forms import inlineformset_factory
from .models import Orders, OrderItems


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ["customer", "order_date"]


# Создаём inline formset для OrderItems
OrderItemFormSet = inlineformset_factory(
    Orders, OrderItems, fields=["item", "quantity"], extra=1, can_delete=True
)
