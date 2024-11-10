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
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/create/", OrderCreateView.as_view(), name="order-create"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order-update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order-delete"),
    # Items URLs
    path("items/", ItemListView.as_view(), name="item-list"),
    path("items/<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
    path("items/create/", ItemCreateView.as_view(), name="item-create"),
    path("items/<int:pk>/update/", ItemUpdateView.as_view(), name="item-update"),
    path("items/<int:pk>/delete/", ItemDeleteView.as_view(), name="item-delete"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("", views.home_page, name="home"),
]
