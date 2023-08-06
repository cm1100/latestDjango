# Generated by Django 4.2.3 on 2023-08-04 10:16

from django.db import migrations, models
import server.models


class Migration(migrations.Migration):
    dependencies = [
        ("server", "0003_rename_categories_server_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="icon",
            field=models.FileField(
                blank=True, null=True, upload_to=server.models.category_icon_upload_path
            ),
        ),
    ]
