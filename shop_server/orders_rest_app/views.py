from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from orders_app.models import Orders
from .serializers import UserSerializer, OrderReadSerializer, OrderWriteSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderReadSerializer

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return OrderWriteSerializer
        return OrderReadSerializer

    @action(detail=False, methods=["get"])
    def expensive(self, request):
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
