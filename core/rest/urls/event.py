from django.urls import path

from core.rest.views import event

urlpatterns = [
    path(
        "",
        event.MeEventPostList.as_view(),
        name="me-event-list",
    ),
    path("<uuid:uid>", event.MeEventPostDetail.as_view(), name="me-event-detail"),
]
