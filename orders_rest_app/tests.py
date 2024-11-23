import pytest
from django.urls import reverse
from orders_app.models import Orders, Items, OrderItems
from django.contrib.auth.models import User
import json


@pytest.fixture
def create_users(db):
    user1 = User.objects.create(username="alan", email="alan@example.com")
    user2 = User.objects.create(username="ben", email="ben@example.com")
    return user1, user2


@pytest.fixture
def create_orders(db, create_users):
    user1, user2 = create_users
    order1 = Orders.objects.create(customer=user1, order_date="2024-11-20")
    order2 = Orders.objects.create(customer=user2, order_date="2024-11-21")
    return order1, order2


@pytest.fixture
def create_items(db):
    item1 = Items.objects.create(item_name="Apple", price=1.0)
    return item1


@pytest.fixture
def create_order_items(db, create_orders, create_items):
    order1, order2 = create_orders
    item = create_items
    order_item1 = OrderItems.objects.create(order=order1, item=item, quantity=1)
    order_item2 = OrderItems.objects.create(order=order2, item=item, quantity=2)
    return order_item1, order_item2


@pytest.mark.django_db
def test_order_list_api(client, create_orders):
    url = reverse("order-list")
    response = client.get(url)

    assert response.status_code == 200

    response_data = response.json()
    assert len(response_data) == 2
    assert all("customer" in order and "order_date" in order for order in response_data)

    expected_data = [
        {"customer": "alan", "order_date": "2024-11-20"},
        {"customer": "ben", "order_date": "2024-11-21"},
    ]
    for expected in expected_data:
        assert any(
            order["customer"] == expected["customer"]
            and order["order_date"] == expected["order_date"]
            for order in response_data
        )


@pytest.mark.django_db
def test_order_detail_api(client, create_orders):
    order = create_orders[0]
    url = reverse("order-detail", args=[order.id])
    response = client.get(url)

    assert response.status_code == 200

    response_data = response.json()
    assert response_data["customer"] == order.customer.username
    assert response_data["order_date"] == order.order_date


@pytest.mark.django_db
def test_order_creation_api(client, create_users, create_items):
    user = create_users[0]
    url = reverse("order-list")
    item = create_items
    data = {
        "customer": user.id,
        "order_date": "2024-11-23",
        "order_items": [{"item": item.id, "quantity": 3}],
    }

    response = client.post(url, data=json.dumps(data), content_type="application/json")

    assert response.status_code == 201

    response_data = response.json()

    assert response_data.get("customer") == user.id
    assert response_data.get("order_date") == "2024-11-23"

    order_items = response_data.get("order_items")

    assert len(order_items) == 1
    assert order_items[0].get("item") == item.id
    assert order_items[0].get("quantity") == 3


@pytest.mark.django_db
def test_order_update_api(client, create_users, create_items):
    user = create_users[0]
    item = create_items
    url = reverse("order-list")

    # Creating order
    data = {
        "customer": user.id,
        "order_date": "2024-11-22",
        "order_items": [{"item": item.id, "quantity": 2}],
    }
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    order_id = response.json().get("id")

    # Updating order
    updated_data = {
        "customer": user.id,
        "order_date": "2024-11-23",
        "order_items": [{"item": item.id, "quantity": 5}],
    }
    update_url = reverse("order-detail", args=[order_id])
    response = client.put(
        update_url, data=json.dumps(updated_data), content_type="application/json"
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data.get("order_date") == "2024-11-23"
    assert len(response_data.get("order_items")) == 1
    assert response_data.get("order_items")[0].get("quantity") == 5


@pytest.mark.django_db
def test_order_delete_api(client, create_users, create_items):
    user = create_users[0]
    item = create_items
    url = reverse("order-list")

    # Creating order
    data = {
        "customer": user.id,
        "order_date": "2024-11-22",
        "order_items": [{"item": item.id, "quantity": 2}],
    }
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    order_id = response.json().get("id")

    # Deleting order
    delete_url = reverse("order-detail", args=[order_id])
    response = client.delete(delete_url)

    assert response.status_code == 204

    # Checking that order has been deleted
    response = client.get(delete_url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_expensive_order_action(
    client, create_orders, create_items, create_order_items
):
    url = reverse("order-expensive")
    response = client.get(url)

    assert response.status_code == 200

    expensive_order = max(
        create_orders,
        key=lambda order: sum(
            item.item.price * item.quantity for item in order.order_items.all()
        ),
    )
    response_data = response.json()
    assert response_data["id"] == expensive_order.id
