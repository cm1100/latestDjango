# Generated by Django 4.2.3 on 2023-08-06 10:53

from django.db import migrations, models
import server.models


class Migration(migrations.Migration):
    dependencies = [
        ("server", "0004_category_icon"),
    ]

    operations = [
        migrations.AddField(
            model_name="server",
            name="banner",
            field=models.ImageField(
                blank=True, null=True, upload_to=server.models.server_banner_path
            ),
        ),
        migrations.AddField(
            model_name="server",
            name="icon",
            field=models.ImageField(
                blank=True, null=True, upload_to=server.models.server_icon_upload_path
            ),
        ),
    ]