import pytest
from django.urls import reverse
from orders_app.models import Orders
from django.contrib.auth.models import User


@pytest.fixture
def create_orders(db):
    user1 = User.objects.create(username="alan", email="alan@example.com")
    user2 = User.objects.create(username="ben", email="ben@example.com")
    Orders.objects.create(customer=user1, order_date="2024-11-20")
    Orders.objects.create(customer=user2, order_date="2024-11-21")


@pytest.mark.django_db
def test_order_list_api(client, create_orders):
    url = reverse("order-list")
    response = client.get(url)
    assert response.status_code == 200
    assert "alan" in response.json()[0]["customer"]
    assert "2024-11-20" in response.json()[0]["order_date"]
    assert "ben" in response.json()[1]["customer"]
    assert "2024-11-21" in response.json()[1]["order_date"]
