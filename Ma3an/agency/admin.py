from django.contrib import admin
from .models import Subscription, AgencyPayment, Tour, TourSchedule

# تسجيل الموديلات لتظهر في لوحة الإدارة
admin.site.register(Subscription)
admin.site.register(AgencyPayment)
admin.site.register(Tour)
admin.site.register(TourSchedule)
