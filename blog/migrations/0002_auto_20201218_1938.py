# Generated by Django 3.1.3 on 2020-12-18 14:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(limit_value=300, message='Content should be at least 300 characters long!')]),
        ),
    ]
