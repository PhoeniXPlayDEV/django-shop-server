from django.db import models
from django.contrib.auth.models import User


class Orders(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="User who placed the order."
    )
    order_date = models.DateField(help_text="Date when the order was placed.")

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"


class Items(models.Model):
    item_name = models.CharField(max_length=50, help_text="Name of the item.")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price of the item (up to 10 digits with 2 decimal places).",
    )

    def __str__(self):
        return self.item_name


class OrderItems(models.Model):
    order = models.ForeignKey(
        Orders,
        on_delete=models.CASCADE,
        help_text="Order that contains this item.",
        related_name="order_items",
    )
    item = models.ForeignKey(
        Items, on_delete=models.CASCADE, help_text="Item included in the order."
    )
    quantity = models.IntegerField(help_text="Quantity of this item in the order.")

    class Meta:
        unique_together = (("order", "item"),)

    def __str__(self):
        return f"{self.quantity} x {self.item.item_name} in Order {self.order.id}"
