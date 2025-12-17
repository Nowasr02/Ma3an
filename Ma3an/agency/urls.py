from django.urls import path
from . import views
from .views import add_tour_view


urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('subscription/', views.subscription, name='subscription'),
    path('add-tour/', add_tour_view, name='add_tour'),
]
