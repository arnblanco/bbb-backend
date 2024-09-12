from django.urls import path
from .views import (
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    ProductStockUpdateView,
    OrderCreateView
)

urlpatterns = [
    # Ruta para listar y crear productos
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    
    # Ruta para recuperar, actualizar y eliminar productos por ID
    path('products/<uuid:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    
    # Ruta para actualizar el stock de un producto por ID
    path('inventories/product/<uuid:pk>/', ProductStockUpdateView.as_view(), name='product-update-stock'),
    
    # Ruta para crear órdenes
    path('orders/', OrderCreateView.as_view(), name='create-order'),
]
