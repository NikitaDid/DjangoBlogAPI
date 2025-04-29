from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFill

from config.settings import MEDIA_ROOT


# Create your models here.

class User(AbstractUser):
    phone = PhoneNumberField(verbose_name='Phone Number', blank=True, null=True)
    image = ProcessedImageField(
        verbose_name='Category Image',
        upload_to='user/',
        processors=[],
        null=True,
        blank=True
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(600, 400)],
    )

    def image_tag_thumbnail(self):
        if self.image:
            if not self.image_thumbnail:
                User.objects.get(id=self.id)
            return mark_safe(f"<img src='/{MEDIA_ROOT}{self.image.name}' width=70>")

    image_tag_thumbnail.short_description = 'Current avatar'

    def image_tag(self):
        if self.image:
            if not self.image_thumbnail:
                User.objects.get(id=self.id)
            return mark_safe(f"<img src='/{MEDIA_ROOT}{self.image.name}' >")

    image_tag.short_description = 'Current avatar'