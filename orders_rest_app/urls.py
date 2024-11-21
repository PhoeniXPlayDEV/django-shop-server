from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, OrderViewSet

router = SimpleRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]
