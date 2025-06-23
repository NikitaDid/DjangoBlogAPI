from django.db import models
from tinymce.models import HTMLField

from apps.catalog.models import Product
from apps.main.mixins import MetaTagMixin


class Page(MetaTagMixin):
    name = models.CharField(verbose_name='Name', max_length=255)
    slug = models.SlugField(unique=True)
    text = HTMLField(verbose_name='Content', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Informational page'
        verbose_name_plural = 'Informational pages'


class ProductSet(models.Model):
    products = models.ManyToManyField(Product, verbose_name='Product')
    name = models.CharField(verbose_name='Name', max_length=255)
    sort = models.PositiveIntegerField(verbose_name='Sort', default=0)
    is_active = models.BooleanField(verbose_name='Activated', default=True)

    def __str__(self):
        return self.name


    class Meta:
        ordering = ['sort'] #sorting from small to bigger product Carousel
        verbose_name = 'Product Carousel'
        verbose_name_plural = 'Products Carousel'
