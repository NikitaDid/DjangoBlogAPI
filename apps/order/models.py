from django.db import models

from apps.catalog.models import Product
from apps.user.models import User
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Cart(models.Model):
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Quantity')
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    total = models.DecimalField(verbose_name='Total', max_digits=10, decimal_places=2)
    first_name = models.CharField(verbose_name='First Name', max_length=255)
    last_name = models.CharField(verbose_name='Last Name', max_length=255)
    email = models.EmailField(verbose_name='Email', max_length=255)
    phone = PhoneNumberField(verbose_name='Phone', max_length=255)
    address = models.TextField(verbose_name='Address')
    comment = models.TextField(verbose_name='Comment', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated date', auto_now=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
