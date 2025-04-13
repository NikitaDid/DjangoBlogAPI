from django.db import models

# Create your models here.

class BlogCategory(models.Model):
    name = models.CharField(verbose_name='Category Name', max_length=255)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'


class Article(models.Model):
    category = models.ForeignKey(to=BlogCategory, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title', max_length=255)
    text_preview = models.TextField(verbose_name='Text Preview', null=True, blank=True)
    text = models.TextField(verbose_name='Text field')
    publish_date = models.DateTimeField(verbose_name='Publish Date')
    updated_at = models.DateTimeField(verbose_name='Updated Date', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Updated Date', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
