from django.urls import path
from .views import create_booking, my_bookings

urlpatterns = [
    path('', create_booking),
    path('my/', my_bookings),
]