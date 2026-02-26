from django.urls import path
from .views import create_train, search_trains

urlpatterns = [
    path('', create_train),
    path('search/', search_trains),
]