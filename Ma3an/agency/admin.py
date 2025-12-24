from django.contrib import admin
from .models import TourSchedule

@admin.register(TourSchedule)
class TourScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "tour",
        "activity_title",
        "start_time",
        "latitude",
        "longitude",
    )

    fields = (
        "tour",
        "activity_title",
        "start_time",
        "latitude",
        "longitude",
    )