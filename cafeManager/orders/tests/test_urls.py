import pytest
from django.urls import reverse
from rest_framework import status
from orders.models import Item, Order

@pytest.mark.django_db
def test_home_page(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_order_list(client):
    url = reverse('order_list')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_item(client):
    url = reverse('add_item')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_item(client):

    item = Item.objects.create(name="Test Item", price=10.99)
    item_id = item.id

    url = reverse('edit_item', args=[item_id])
    response = client.get(url)

    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['item'] == item

@pytest.mark.django_db
def test_add_order(client):
    url = reverse('add_order')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_order(client):

    item = Item.objects.create(name="Test Item", price=10.99)
    order = Order.objects.create(table_number=5)
    order.items.add(item)

    order_id = order.id
    url = reverse('delete_order', args=[order_id])


    response = client.post(url)


    assert response.status_code == 302
    assert not Order.objects.filter(id=order_id).exists()


@pytest.mark.django_db
def test_search_orders(client):
    url = reverse('search_orders')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_status(client):

    item = Item.objects.create(name="Test Item", price=10.99)
    order = Order.objects.create(table_number=5, status='pending')
    order.items.add(item)

    order_id = order.id
    url = reverse('update_status', args=[order_id])


    response = client.get(url)


    assert response.status_code == 200
    assert 'order' in response.context
    assert response.context['order'] == order

@pytest.mark.django_db
def test_revenue_report(client):
    url = reverse('revenue_report')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_api_items(client):
    url = reverse('item-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_api_orders(client):
    url = reverse('order-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
