import pytest
from django.forms import modelform_factory
from orders.models import Order, Item
from orders.forms import OrderForm, ItemForm

@pytest.fixture
def item_data():
    item1 = Item.objects.create(name="Item 1", price=10)
    item2 = Item.objects.create(name="Item 2", price=20)
    return item1, item2

@pytest.mark.django_db
def test_order_form_valid(item_data):
    item1, item2 = item_data
    form_data = {
        'table_number': '1',
        'items': [item1.id, item2.id],
        'status': 'pending',
    }
    form = OrderForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_order_form_invalid(item_data):
    form_data = {
        'table_number': '1',
        'status': 'pending',
    }
    form = OrderForm(data=form_data)
    assert not form.is_valid()
    assert 'items' in form.errors

@pytest.mark.django_db
def test_items_field(item_data):
    form = OrderForm()
    assert form.fields['items'].queryset.count() == Item.objects.count()

@pytest.mark.django_db
def test_item_form_valid():
    form_data = {
        'name': 'New Item',
        'price': 15.50,
    }
    form = ItemForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_item_form_invalid():
    form_data = {
        'name': 'New Item',
    }
    form = ItemForm(data=form_data)
    assert not form.is_valid()
    assert 'price' in form.errors

@pytest.mark.django_db
def test_item_form_field_classes():
    form = ItemForm()
    assert 'form-control' in form.fields['name'].widget.attrs['class']
    assert 'form-control' in form.fields['price'].widget.attrs['class']
    assert 'form-control' in form.fields['image'].widget.attrs['class']
