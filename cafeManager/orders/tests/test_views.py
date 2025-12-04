import pytest
from django.urls import reverse
from django.shortcuts import get_object_or_404
from orders.models import Order, Item
from orders.forms import OrderForm, ItemForm
from rest_framework import status
import pytest


@pytest.fixture
def item_data():

    item1 = Item.objects.create(name="Item 1", price=10)
    item2 = Item.objects.create(name="Item 2", price=20)
    return item1, item2

@pytest.mark.django_db
def test_home_page(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assert 'items' in response.context

@pytest.mark.django_db
def test_add_item_get(client):
    url = reverse('add_item')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_add_item_post(client):
    url = reverse('add_item')
    form_data = {
        'name': 'New Item',
        'price': 15.50,
    }
    response = client.post(url, form_data)
    assert response.status_code == 302
    assert Item.objects.count() == 1

@pytest.mark.django_db
def test_edit_item_get(client):
    item = Item.objects.create(name="Item 1", price=10)
    url = reverse('edit_item', args=[item.id])
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['item'] == item

@pytest.mark.django_db
def test_edit_item_post(client):
    item = Item.objects.create(name="Item 1", price=10)
    url = reverse('edit_item', args=[item.id])
    form_data = {
        'name': 'Updated Item',
        'price': 20,
    }
    response = client.post(url, form_data)
    item.refresh_from_db()
    assert response.status_code == 302
    assert item.name == 'Updated Item'
    assert item.price == 20

@pytest.mark.django_db
def test_order_list(client):
    url = reverse('order_list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'orders' in response.context

@pytest.mark.django_db
def test_add_order_get(client):
    url = reverse('add_order')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_add_order_post(client, item_data):
    item1, item2 = item_data
    form_data = {
        'table_number': '1',
        'items': [item1.id, item2.id],
        'status': 'pending',
    }
    url = reverse('add_order')
    response = client.post(url, form_data)
    assert response.status_code == 302
    assert Order.objects.count() == 1

@pytest.mark.django_db
def test_delete_order(client):
    order = Order.objects.create(table_number='1', status='pending')
    url = reverse('delete_order', args=[order.id])
    response = client.get(url)
    assert response.status_code == 302
    assert Order.objects.count() == 0

@pytest.mark.django_db
def test_search_orders(client):
    order = Order.objects.create(table_number='1', status='pending')
    url = reverse('search_orders') + '?query=1'
    response = client.get(url)
    assert response.status_code == 200
    assert 'orders' in response.context
    assert order in response.context['orders']

@pytest.mark.django_db
def test_update_status_get(client):
    order = Order.objects.create(table_number='1', status='pending')
    url = reverse('update_status', args=[order.id])
    response = client.get(url)
    assert response.status_code == 200
    assert 'order' in response.context

@pytest.mark.django_db
def test_update_status_post(client):
    order = Order.objects.create(table_number='1', status='pending')
    url = reverse('update_status', args=[order.id])
    form_data = {'status': 'paid'}
    response = client.post(url, form_data)
    order.refresh_from_db()
    assert response.status_code == 302
    assert order.status == 'paid'

@pytest.mark.django_db
def test_revenue_report(client):
    Order.objects.create(table_number='1', status='paid', total_price=50)
    url = reverse('revenue_report')
    response = client.get(url)
    assert response.status_code == 200
    assert 'total_revenue' in response.context
    assert 'shift_revenue' in response.context

@pytest.mark.django_db
def test_item_viewset_api(client):
    item = Item.objects.create(name="Item 1", price=10)
    url = reverse('item-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0

@pytest.mark.django_db
def test_order_viewset_api(client):
    order = Order.objects.create(table_number='1', status='pending')
    url = reverse('order-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
