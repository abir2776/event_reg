from rest_framework import serializers

from rest_framework.exceptions import ValidationError

from versatileimagefield.serializers import VersatileImageFieldSerializer

from event.models import EventPost, UserEventRegistration


class EventSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400x400", "crop__400x400"),
        ],
        required=False,
        read_only=True,
    )
    book = serializers.BooleanField(write_only=True)
    is_booked = serializers.SerializerMethodField()

    class Meta:
        model = EventPost
        fields = [
            "uid",
            "slug",
            "title",
            "summary",
            "description",
            "image",
            "slot",
            "booked_slot",
            "status",
            "book",
            "is_booked",
            "created_at",
        ]
        read_only_fields = [
            "uid",
            "slug",
            "title",
            "summary",
            "description",
            "image",
            "slot",
            "booked_slot",
            "status",
            "created_at",
        ]

    def get_is_booked(self, object_):
        user_event = UserEventRegistration.objects.filter(
            user=self.context["request"].user, event=object_
        ).first()
        if user_event is not None:
            return user_event.is_booked
        else:
            return False

    def update(self, instance, validated_data):
        book = self.validated_data.pop("book", None)
        user = self.context["request"].user
        if book is not None:
            user_event, created = UserEventRegistration.objects.get_or_create(
                user=user, event=instance, defaults={"is_booked": True}
            )
            if not created:
                if user_event.is_booked:
                    raise ValidationError("You are already registred for this event")

            if instance.booked_slot + 1 > instance.slot:
                if created:
                    user_event.delete()
                raise ValidationError("all slots are booked!")

            if user_event.is_booked == False:
                user_event.is_booked = True
                user_event.save()

        return instance
