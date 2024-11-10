from rest_framework import serializers
from orders_app.models import Orders, Items, OrderItems
from django.contrib.auth.models import User


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ["id", "item_name", "price"]


class OrderItemReadSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = OrderItems
        fields = ["id", "item", "quantity"]


class OrderItemWriteSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Items.objects.all())

    class Meta:
        model = OrderItems
        fields = ["id", "item", "quantity"]


class OrderReadSerializer(serializers.ModelSerializer):
    order_items = OrderItemReadSerializer(many=True, read_only=True)
    customer = serializers.StringRelatedField()

    class Meta:
        model = Orders
        fields = ["id", "customer", "order_date", "order_items"]


class OrderWriteSerializer(serializers.ModelSerializer):
    order_items = OrderItemWriteSerializer(many=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Orders
        fields = ["id", "customer", "order_date", "order_items"]

    def create(self, validated_data):
        customer = validated_data.pop("customer")
        order_date = validated_data.pop("order_date")

        order = Orders.objects.create(customer=customer, order_date=order_date)

        order_items_data = validated_data.pop("order_items", [])
        for item_data in order_items_data:
            item = item_data["item"]
            quantity = item_data["quantity"]
            OrderItems.objects.create(order=order, item=item, quantity=quantity)

        return order

    def update(self, instance, validated_data):
        customer = validated_data.get("customer", instance.customer)
        order_date = validated_data.get("order_date", instance.order_date)

        instance.customer = customer
        instance.order_date = order_date

        order_items_data = validated_data.get("order_items", [])
        for item_data in order_items_data:
            item = item_data["item"]
            quantity = item_data["quantity"]
            OrderItems.objects.update_or_create(
                order=instance, item=item, defaults={"quantity": quantity}
            )

        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    orders = OrderReadSerializer(many=True, read_only=True, source="orders_set")

    class Meta:
        model = User
        fields = ["id", "username", "email", "orders"]
