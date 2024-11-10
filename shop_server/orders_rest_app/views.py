from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from orders_app.models import Orders, OrderItems
from .serializers import UserSerializer, OrderSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=["get"])
    def expensive(self, request):
        # Находим самый дорогой заказ
        expensive_order = max(
            self.queryset,
            key=lambda order: sum(
                item.item.price * item.quantity for item in order.order_items.all()
            ),
            default=None,
        )
        if expensive_order is None:
            return Response({"detail": "No orders found."}, status=404)

        serializer = self.get_serializer(expensive_order)
        return Response(serializer.data)
