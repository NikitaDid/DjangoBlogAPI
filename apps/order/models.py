from django.db import models

from apps.catalog.models import Product
from apps.user.models import User


# Create your models here.
class Cart(models.Model):
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Quantity')
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
