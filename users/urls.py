from django.urls import path,include
from .views import get_user_details,CategoryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('',CategoryViewSet,basename='category')


urlpatterns = [
    path('', get_user_details),
    path('category/',include(router.urls))
]
