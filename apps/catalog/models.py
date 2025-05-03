from django.db import models
from django.utils.safestring import mark_safe
from imagekit.models import ProcessedImageField
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from pilkit.processors import ResizeToFill

from config.settings import MEDIA_ROOT


# Create your models here.

class Category(MPTTModel):
    name = models.CharField(verbose_name='Name', max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name='Description', null=True, blank=True)
    image = ProcessedImageField(
        verbose_name='Image',
        upload_to='catalog/category/',
        processors=[ResizeToFill(600, 400)],
        null=True,
        blank=True
    )
    parent = TreeForeignKey(
        'self',
        related_name='Parent',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def image_tag_thumbnail(self):
        if self.image:
            return mark_safe(f"<img src='/{MEDIA_ROOT}{self.image}' width='70'>")

    image_tag_thumbnail.short_description = 'Image'

    def image_tag(self):
        if self.image:
            return mark_safe(f"<img src='/{MEDIA_ROOT}{self.image}'>")

    def __str__(self):
        full_path = [self.name]
        parent = self.parent
        while parent is not None:
            full_path.append(parent.name)
            parent = parent.parent
        return ' -> '.join(full_path[::-1])

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Product(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255)
    slug = models.CharField(255)
    description = models.TextField(verbose_name='Description', null=True, blank=True)
    quantity = models.IntegerField(verbose_name='Quantity', null=True, blank=True)
    price = models.DecimalField(verbose_name='Price', max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(verbose_name='Created')
    updated_at = models.DateTimeField(verbose_name='Updated', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'