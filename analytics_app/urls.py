from django.urls import path
from .views import top_routes

urlpatterns = [
    path('top-routes/', top_routes),
]