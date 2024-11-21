from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    ItemListView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
)
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # Orders URLs
    path("orders/", OrderListView.as_view(), name="order-list-app"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail-app"),
    path("orders/create/", OrderCreateView.as_view(), name="order-create-app"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order-update-app"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order-delete-app"),
    # Items URLs
    path("items/", ItemListView.as_view(), name="item-list-app"),
    path("items/<int:pk>/", ItemDetailView.as_view(), name="item-detail-app"),
    path("items/create/", ItemCreateView.as_view(), name="item-create-app"),
    path("items/<int:pk>/update/", ItemUpdateView.as_view(), name="item-update-app"),
    path("items/<int:pk>/delete/", ItemDeleteView.as_view(), name="item-delete-app"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("", views.home_page, name="home"),
]
