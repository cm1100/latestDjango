import os.path

from PIL import Image
from django.core.exceptions import ValidationError


def validate_icon_image_size(image):
    print(image)
    if image:
        with Image.open(image) as img:
            if img.height > 70 or img.width > 70:
                raise ValidationError(f"The maximum size allowed is 70*70")


def validate_image_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    if ext.lower() not in valid_extensions:
        raise ValidationError("This extension is not allowed")
