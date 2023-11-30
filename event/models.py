from django.conf import settings

from django.db import models

from autoslug import AutoSlugField

from versatileimagefield.fields import VersatileImageField

from common.models import BaseModelWithUID

from .managers import EventPostQuerySet

from .choices import EventPostStatus
from .paths import get_eventpost_image_path
from .slugifiers import get_eventpost_slug


class EventPost(BaseModelWithUID):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from=get_eventpost_slug, unique=True, db_index=True)
    summary = models.TextField(blank=True)
    image = VersatileImageField(
        upload_to=get_eventpost_image_path, blank=True, null=True
    )
    description = models.TextField(blank=True)
    slot = models.IntegerField()
    booked_slot = models.IntegerField()
    status = models.CharField(
        max_length=20, choices=EventPostStatus.choices, db_index=True
    )
    event_datetime = models.DateTimeField(blank=True, null=True)

    # FKs
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL
    )
    # custom managers use
    objects = EventPostQuerySet.as_manager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Title: {self.title}, Slug: {self.slug}"


class UserEventRegistration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(EventPost, on_delete=models.CASCADE)
    is_booked = models.BooleanField(default=True)
