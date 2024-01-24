from django.urls import path
from .views import get_user_details

urlpatterns = [
    path('', get_user_details),
]
