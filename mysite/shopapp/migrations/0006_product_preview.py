# Generated by Django 5.1.7 on 2025-03-31 08:54

import shopapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopapp", "0005_order_receipt"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="preview",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=shopapp.models.product_preview_directory_path,
            ),
        ),
    ]
