from django.db import models
from django.utils.safestring import mark_safe
from imagekit.models import ProcessedImageField, ImageSpecField
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from pilkit.processors import ResizeToFill

from apps.main.mixins import MetaTagMixin
from config.settings import MEDIA_ROOT


# Create your models here.

class Category(MPTTModel, MetaTagMixin):
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

    def get_absolute_url(self):
        return reverse('Categories', args=[self.slug])

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ProductImage(models.Model):
    image = ProcessedImageField(
        verbose_name='Category Image',
        upload_to='catalog/product/',
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(600, 400)],
    )
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    is_main = models.BooleanField(verbose_name='Main image', default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.is_main:
            ProductImage.objects.filter(product=self.product).update(is_main=False)
        super().save(force_insert, force_update, using, update_fields)

    def image_tag_thumbnail(self):
        if not self.image_thumbnail:
            ProductImage.objects.get(id=self.id)
        return mark_safe(f"<img src='/{MEDIA_ROOT}{self.image.name}' width=70>")

    image_tag_thumbnail.short_description = 'Current Image'

    def image_tag(self):
        if not self.image_thumbnail:
            ProductImage.objects.get(id=self.id)
        return mark_safe(f"<img src='/{MEDIA_ROOT}{self.image.name}' >")

    image_tag.short_description = 'Current Image'

    def __str__(self):
        return ''

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'


class Product(MetaTagMixin):
    name = models.CharField(verbose_name='Name', max_length=255)
    slug = models.CharField(unique=True, verbose_name='Slug')
    description = models.TextField(verbose_name='Description', null=True, blank=True)
    quantity = models.IntegerField(verbose_name='Quantity', null=True, blank=True)
    price = models.DecimalField(verbose_name='Price', max_digits=12, decimal_places=2, default=0)
    categories = models.ManyToManyField(Category, verbose_name='Categories', through='ProductCategory', blank=True)
    created_at = models.DateTimeField(verbose_name='Created')
    updated_at = models.DateTimeField(verbose_name='Updated', null=True, blank=True)


    def images(self):
        return ProductImage.objects.filter(product=self.id)

    def main_image(self):
        image = ProductImage.objects.filter(product=self.id, is_main=True).first()
        if not image:
            image = self.images().first()
        return image

    def image_tag(self):
        image = self.main_image()
        if image:
            return image.image_tag_thumbnail()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', args=[self.slug])

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductCategory(models.Model):  # Connecting product to different categories
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    is_main = models.BooleanField(verbose_name='Main Category', default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.is_main:
            ProductCategory.objects.filter(product=self.product).update(is_main=False)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return ''

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'
