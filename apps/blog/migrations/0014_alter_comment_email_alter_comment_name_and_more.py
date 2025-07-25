# Generated by Django 5.2 on 2025-06-26 12:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(default='', max_length=254, verbose_name='Author Email'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(default='', max_length=100, verbose_name='Author Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
