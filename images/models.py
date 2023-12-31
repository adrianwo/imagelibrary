from django.db import models
from django.conf import settings
from django.db.models.query import QuerySet
from django.utils import timezone
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    FileExtensionValidator,
)
from imagekit.models import ImageSpecField
from imagekit import ImageSpec, register
from imagekit.processors import Thumbnail
from imagekit.utils import get_field_info
import sys


User = settings.AUTH_USER_MODEL


class ThumbnailSpec1(ImageSpec):
    format = "JPEG"
    options = {"quality": 60}
    cachefile_storage = settings.SENDFILE_STORAGE

    @property
    def processors(self):
        model, field_name = get_field_info(self.source)
        return [Thumbnail(height=model.user.profile.height_1)]


register.generator("upload:uploaded_image:thumbnail_1", ThumbnailSpec1)


class ThumbnailSpec2(ImageSpec):
    format = "JPEG"
    options = {"quality": 60}
    cachefile_storage = settings.SENDFILE_STORAGE

    @property
    def processors(self):
        model, field_name = get_field_info(self.source)
        return [Thumbnail(height=model.user.profile.height_2)]


register.generator("upload:uploaded_image:thumbnail_2", ThumbnailSpec2)


class Image(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    file_extension_validator = FileExtensionValidator(
        allowed_extensions=["png", "jpg", "jpeg"], message="File extension not allowed."
    )

    image = models.ImageField(
        storage=settings.SENDFILE_STORAGE,
        validators=[
            file_extension_validator,
        ],
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    thumbnail_1 = ImageSpecField(source="image", id="upload:uploaded_image:thumbnail_1")
    thumbnail_2 = ImageSpecField(source="image", id="upload:uploaded_image:thumbnail_2")
    title = models.CharField(max_length=100, blank=True)

    def is_user_allowed(self, user):
        return self.user.pk == user.pk

    def save(self, *args, **kwargs):
        if not self.id and self.title == "":
            self.title = self.image.name
        super().save(*args, **kwargs)


class LinkManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(valid_till__gt=timezone.now())


class Link(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    valid = models.PositiveIntegerField(
        help_text="Valid for (seconds)",
        validators=[MinValueValidator(300), MaxValueValidator(30_000)],
    )
    valid_till = models.DateTimeField(blank=True, editable=False)

    objects = LinkManager()

    def save(self, *args, **kwargs):
        self.valid_till = timezone.now() + timezone.timedelta(seconds=self.valid)
        super().save(*args, **kwargs)
