from django.contrib import admin
from .models import Orders, Items, OrderItems

admin.site.register(Orders)
admin.site.register(Items)
admin.site.register(OrderItems)
