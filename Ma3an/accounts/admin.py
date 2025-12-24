from django.contrib import admin
from .models import Notification, Traveler

# Register your models here.

@admin.register(Notification)
class TourScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "event",
        "message"
    )

    fields = (
        "user",
        "event",
        "message"
    )

@admin.register(Traveler)
class TravelerScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone_number",
        "date_of_birth"
    )

    fields = (
        "user",
        "phone_number",
        "date_of_birth"
    )