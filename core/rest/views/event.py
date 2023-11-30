from rest_framework import filters, generics

from event.models import EventPost, UserEventRegistration

from event.rest.serializers.event import EventSerializer


class MeEventPostList(generics.ListAPIView):
    serializer_class = EventSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    ordering_fields = ["title", "created_at"]
    search_fields = [
        "summary",
        "title",
    ]

    def get_queryset(self):
        user_event_ids = UserEventRegistration.objects.filter(
            user=self.request.user
        ).values_list("event_id", flat=True)
        return EventPost.objects.filter(id__in=user_event_ids)


class MeEventPostDetail(generics.RetrieveUpdateAPIView):
    queryset = EventPost.objects.get_status_active()
    serializer_class = EventSerializer
    lookup_field = "uid"
