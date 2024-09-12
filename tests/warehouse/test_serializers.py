import pytest
from rest_framework.exceptions import ValidationError
from uuid import uuid4

from _apps.warehouse.models import Product
from _apps.warehouse.serializers import ProductSerializer, ProductStockUpdateSerializer, OrderSerializer

@pytest.mark.django_db
def test_product_serializer_valid():
    product = Product.objects.create(
        sku='1234567890',
        name='Test Product'
    )
    serializer = ProductSerializer(product)
    data = serializer.data
    assert data['id'] == str(product.id)
    assert data['sku'] == '1234567890'
    assert data['name'] == 'Test Product'
    assert 'description' in data

@pytest.mark.django_db
def test_product_stock_update_serializer_valid():
    data = {'stock': 50}
    serializer = ProductStockUpdateSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['stock'] == 50

@pytest.mark.django_db
def test_product_stock_update_serializer_invalid():
    data = {'stock': -10}
    serializer = ProductStockUpdateSerializer(data=data)
    assert not serializer.is_valid()
    assert 'stock' in serializer.errors

@pytest.mark.django_db
def test_order_serializer_valid():
    product = Product.objects.create(
        sku='1234567890',
        name='Test Product'
    )

    data = {'product_id': str(product.id), 'quantity': 5}
    serializer = OrderSerializer(data=data)
    assert serializer.is_valid(), f"Errors: {serializer.errors}"

@pytest.mark.django_db
def test_order_serializer_invalid_quantity():
    data = {'product_id': 'some-uuid', 'quantity': 0}
    serializer = OrderSerializer(data=data)
    assert not serializer.is_valid()
    assert 'quantity' in serializer.errors
