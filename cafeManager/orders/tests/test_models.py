import pytest
from django.core.exceptions import ValidationError
from orders.models import Item, Order
from decimal import Decimal


@pytest.mark.django_db
def test_create_item():
    item = Item.objects.create(name='Burger', price=5.99)
    assert item.name == 'Burger'
    assert item.price == 5.99
    assert str(item) == 'Burger - $5.99'


@pytest.mark.django_db
def test_create_order():
    order = Order.objects.create(table_number=5, status='pending')
    assert order.table_number == 5
    assert order.status == 'pending'
    assert str(order) == f"Order {order.id} - Table 5"


@pytest.mark.django_db
def test_order_total_price_on_add_items():
    item1 = Item.objects.create(name='Burger', price=5.99)
    item2 = Item.objects.create(name='Fries', price=2.99)
    order = Order.objects.create(table_number=5)
    order.items.add(item1, item2)

    order.refresh_from_db()
    assert order.total_price == Decimal('8.98')



@pytest.mark.django_db
def test_order_total_price_on_remove_items():

    item1 = Item.objects.create(name='Burger', price=Decimal('5.99'))
    item2 = Item.objects.create(name='Fries', price=Decimal('2.99'))


    order = Order.objects.create(table_number=5)
    order.items.add(item1, item2)


    order.items.remove(item1)


    order.refresh_from_db()


    assert order.total_price == Decimal('2.99')


@pytest.mark.django_db
def test_order_total_price_on_clear_items():

    item1 = Item.objects.create(name='Burger', price=5.99)
    item2 = Item.objects.create(name='Fries', price=2.99)


    order = Order.objects.create(table_number=5)
    order.items.add(item1, item2)


    order.items.clear()


    order.refresh_from_db()
    assert order.total_price == 0.00


@pytest.mark.django_db
def test_order_invalid_status():

    with pytest.raises(ValidationError):
        order = Order.objects.create(table_number=5, status='invalid_status')
        order.full_clean()
