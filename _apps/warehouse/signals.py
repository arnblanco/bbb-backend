import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product

# Configurar el logger
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Product)
def check_product_stock(sender, instance, **kwargs):
    """
    Revisa si el stock de un producto es menor a 10 después de guardarse.
    """
    if instance.stock < 10:
        logger.warning(f"Alerta: El stock del producto '{instance.name}' es bajo ({instance.stock}).")
