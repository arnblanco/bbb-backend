import uuid
from django.db import models

class Product(models.Model):
    """
    Modelo que representa un producto en el sistema.

    Atributos:
        id (UUID): Identificador único del producto, generado automáticamente.
        sku (str): Codigo del producto.
        name (str): Nombre del producto.
        description (str): Descripción corta del producto.
        stock (str): Existencia del producto, valor inicial 100.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sku = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=100)


    def __str__(self):
        """
        Retorna una representación en cadena del objeto producto.

        Returns:
            str: El nombre del producto.
        """
        return self.name