from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductSerializer, ProductStockUpdateSerializer, OrderSerializer
from django.shortcuts import get_object_or_404

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductStockUpdateView(APIView):
    """
    Vista para actualizar el stock de un producto.
    """

    @swagger_auto_schema(
        operation_description="Actualizar el stock de un producto",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'stock': openapi.Schema(type=openapi.TYPE_NUMBER, description='Cantidad de stock a añadir'),
            }
        ),
        responses={200: "Stock actualizado correctamente", 400: "Error en la solicitud"}
    )
    def patch(self, request, pk):
        """
        Manejar el PATCH request para actualizar el stock del producto.
        
        Params:
            pk (UUID): El ID del producto.
        
        Body (JSON):
            {
                "stock": cantidad_a_sumar
            }
        """
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductStockUpdateSerializer(data=request.data)

        if serializer.is_valid():
            stock_to_add = serializer.validated_data['stock']
            
            if stock_to_add <= 0:
                return Response({"error": "El stock a añadir debe ser un valor positivo."}, status=status.HTTP_400_BAD_REQUEST)

            product.stock += stock_to_add
            product.save()
            return Response({"message": "Stock actualizado correctamente", "new_stock": product.stock}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCreateView(APIView):
    """
    Vista para crear una orden de compra.
    
    Recibe un producto y una cantidad, y descuenta la cantidad del stock.
    """
    @swagger_auto_schema(
        operation_description="Crear una orden de compra",
        request_body=OrderSerializer,
        responses={200: "Compra realizada con éxito", 400: "No hay suficiente stock para completar la compra"}
    )
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            
            # Obtener el producto a través del ID
            product = get_object_or_404(Product, id=product_id)
            
            # Verificar si hay suficiente stock
            if product.stock < quantity:
                return Response(
                    {"error": "No hay suficiente stock para completar la compra."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Restar el stock
            product.stock -= quantity
            product.save()
            
            return Response(
                {"message": "Compra realizada con éxito", "remaining_stock": product.stock},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)