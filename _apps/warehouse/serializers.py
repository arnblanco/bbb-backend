from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializador para la lectura de datos básicos de la entidad Product.

    Este serializador incluye los campos esenciales que se exponen al cliente 
    cuando se solicita información básica de un producto.
    """
    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'description']
        read_only_fields = ['id']

    def validate_sku(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("El SKU debe tener al menos 4 caracteres.")
        return value

    def validate_name(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("El nombre debe tener al menos 5 caracteres.")
        return value

class ProductStockUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador para actualizar el stock de un producto.
    """
    class Meta:
        model = Product
        fields = ['stock']

    def validate_stock(self, value):
        """
        Validar que el stock sea un valor positivo y razonable.
        """
        if value <= 0:
            raise serializers.ValidationError("El stock debe ser un valor positivo.")
        if value > 10000:
            raise serializers.ValidationError("El stock no puede exceder los 10,000.")
        return value

class OrderSerializer(serializers.Serializer):
    """
    Serializador para realizar un pedido de un producto.
    """
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        fields = ['product_id', 'quantity']

    def validate(self, data):
        """
        Validar que el product_id existe en la base de datos.
        """
        product_id = data.get('product_id')
        if not Product.objects.filter(id=product_id).exists():
            raise serializers.ValidationError(f"El producto con ID {product_id} no existe.")
        return data
