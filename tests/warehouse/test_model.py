import pytest
from django.db.utils import IntegrityError
from _apps.warehouse.models import Product

@pytest.mark.django_db
def test_product_creation():
    product = Product.objects.create(
        sku='1234567890',
        name='Test Product',
        description='A test product',
        stock=50
    )
    assert product.sku == '1234567890'
    assert product.name == 'Test Product'
    assert product.description == 'A test product'
    assert product.stock == 50

@pytest.mark.django_db
def test_product_stock_default():
    product = Product.objects.create(
        sku='0987654321',
        name='Default Stock Product'
    )
    assert product.stock == 100

@pytest.mark.django_db
def test_product_sku_unique():
    Product.objects.create(
        sku='unique_sku',
        name='Product 1'
    )
    with pytest.raises(IntegrityError):
        Product.objects.create(
            sku='unique_sku',
            name='Product 2'
        )
