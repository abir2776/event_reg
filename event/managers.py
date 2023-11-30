import logging

from django.db import models

from .choices import EventPostStatus

logger = logging.getLogger(__name__)


class EventPostQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=EventPostStatus.PUBLISHED)

    def get_status_editable(self):
        statuses = [
            EventPostStatus.ARCHIVED,
            EventPostStatus.DRAFT,
            EventPostStatus.HIDDEN,
            EventPostStatus.PUBLISHED,
            EventPostStatus.UNPUBLISHED,
        ]
        return self.filter(status__in=statuses)
