from django.urls import path

from event.rest.views import event

urlpatterns = [
    path(
        "",
        event.EventPostList.as_view(),
        name="event-list",
    ),
    path("<uuid:uid>", event.EventPostDetail.as_view(), name="event-detail"),
]
