from django.contrib import admin

from .models import EventPost, UserEventRegistration

admin.site.register(EventPost)
admin.site.register(UserEventRegistration)
