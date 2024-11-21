import pytest
from django.urls import reverse
from .models import Items


@pytest.fixture
def create_items(db):
    Items.objects.create(item_name="Apple", price=1.0)


@pytest.mark.django_db
def test_user_list_view(client, create_items):
    url = reverse("item-list-app")
    response = client.get(url)
    assert response.status_code == 200
    assert b"Apple" in response.content
