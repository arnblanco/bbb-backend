import json
import pytest
from rest_framework import status
from django.urls import reverse
from _apps.warehouse.models import Product
from _apps.warehouse.serializers import ProductSerializer

@pytest.mark.django_db
def test_product_list_create_view(client):
    url = reverse('product-list-create')
    response = client.post(url, {'sku': '1234567890', 'name': 'Test Product'}, content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Product.objects.count() == 1
    assert Product.objects.get().name == 'Test Product'

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

@pytest.mark.django_db
def test_product_retrieve_update_destroy_view(client):
    product = Product.objects.create(sku='1234567890', name='Test Product')
    url = reverse('product-detail', args=[product.id])

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Test Product'

    response = client.patch(url, {'name': 'Updated Product'}, content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Updated Product'

    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Product.objects.count() == 0

@pytest.mark.django_db
def test_product_stock_update_view(client):
    # Crear un producto con stock inicial
    product = Product.objects.create(sku='1234567890', name='Test Product', stock=10)
    url = reverse('product-update-stock', args=[product.id])
    
    # Actualizar el stock con una cantidad positiva
    response = client.patch(url, {'stock': 20}, content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['new_stock'] == 30
    
    # Intentar actualizar el stock con una cantidad negativa
    response = client.patch(url, {'stock': -5}, content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'stock' in response.data
    assert response.data['stock'][0] == 'El stock debe ser un valor positivo.'

@pytest.mark.django_db
def test_order_create_view(client):
    # Crear un producto con stock inicial
    product = Product.objects.create(sku='1234567890', name='Test Product', stock=20)
    url = reverse('create-order')
    
    # Realizar una orden que debería reducir el stock
    response = client.post(url, {'product_id': str(product.id), 'quantity': 5}, content_type='application/json')
    
    # Verificar que la respuesta es correcta
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Compra realizada con éxito'
    
    # Volver a obtener el producto para verificar el stock actualizado
    product.refresh_from_db()
    assert product.stock == 15
