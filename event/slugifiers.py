import logging

logger = logging.getLogger(__name__)


def get_eventpost_slug(instance):
    return f"{instance.title}"
