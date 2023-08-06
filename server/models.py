from django.db import models
from django.conf import settings
import uuid
from django.dispatch import receiver
from server.validators import validate_icon_image_size, validate_image_file_extension


# Create your models here.


def category_icon_upload_path(instance, filename):
    return f"category/{uuid.uuid4()}/category_icon/{filename}"


def server_icon_upload_path(instance, filename):
    return f"server/{instance.name}/server_icons/{filename}"


def server_banner_path(instance, filename):
    return f"server/{instance.name}/server_banners/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(upload_to=category_icon_upload_path, null=True, blank=True)

    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender, instance, **kwargs):
        file = getattr(instance, "icon")
        if file:
            file.delete(save=False)

    def __str__(self):
        return self.name


class Server(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="server_category"
    )
    description = models.CharField(max_length=250, null=True, blank=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)
    icon = models.ImageField(
        upload_to=server_icon_upload_path,
        null=True,
        blank=True,
        validators=[validate_image_file_extension, validate_icon_image_size],
    )
    banner = models.ImageField(upload_to=server_banner_path, null=True, blank=True)

    def __str__(self):
        return self.name

    @receiver(models.signals.pre_delete, sender="server.Server")
    def server_delete_files(sender, instance, **kwargs):
        icon = getattr(instance, "icon")
        banner = getattr(instance, "banner")
        if icon:
            icon.delete(save=False)
        if banner:
            banner.delete(save=False)


# Associate Channels with Servers
class Channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner"
    )
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name="channel_server"
    )

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Channel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
