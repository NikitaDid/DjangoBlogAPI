from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFill
from django.utils.safestring import mark_safe
from config.settings import MEDIA_ROOT


# Create your models here.

class BlogCategory(models.Model):
    name = models.CharField(verbose_name='Category Name', max_length=255)
    # image = models.ImageField(verbose_name='Category Image', upload_to='blog/category/', null=True)
    image = ProcessedImageField(
        verbose_name='Category Image',
        upload_to='blog/category/',
        processors=[ResizeToFill(600, 400)],
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'

    def image_tag_thumbnail(self):
        if self.image:
            return mark_safe(f"<img src='/{MEDIA_ROOT}{self.image}' width='70'>")

    image_tag_thumbnail.short_description = 'Image'

    def image_tag(self):
        if self.image:
            return mark_safe(f"<img src='/{MEDIA_ROOT}{self.image}'>")

    image_tag.short_description = 'Image'


class Article(models.Model):
    category = models.ForeignKey(to=BlogCategory, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title', max_length=255)
    text_preview = models.TextField(verbose_name='Text Preview', null=True, blank=True)
    text = models.TextField(verbose_name='Text Field')
    publish_date = models.DateTimeField(verbose_name='Publish Date')
    tags = models.ManyToManyField(to='Tag', verbose_name='Tags',
                                  blank=True)  # blank for admin panel. We can now save article without a tag
    image = ProcessedImageField(
        verbose_name='Category Image',
        upload_to='blog/article/',
        processors=[],
        null=True,
        blank=True
    )
    image_thumnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(600, 400)],
    )
    updated_at = models.DateTimeField(verbose_name='Updated Date', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Created Date', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'


class Tag(models.Model):
    name = models.CharField(verbose_name='Tag Name', max_length=255)

    def __str__(self):  # using to show it is in a normal way in admin
        return self.name

    class Meta:  # Human-readable singular name for admin panel
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
