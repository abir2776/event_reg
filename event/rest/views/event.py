from rest_framework import filters, generics

from event.models import EventPost

from event.rest.serializers.event import EventSerializer


class EventPostList(generics.ListAPIView):
    queryset = EventPost.objects.get_status_active()
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


class EventPostDetail(generics.RetrieveUpdateAPIView):
    queryset = EventPost.objects.get_status_active()
    serializer_class = EventSerializer
    lookup_field = "uid"
