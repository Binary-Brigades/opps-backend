
from django.contrib import admin
from django.urls import path,include
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='OOPS API Documentation')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/account/',include('dj_rest_auth.urls')),
    path('api/v1/account/register/',include('dj_rest_auth.registration.urls')),
    path('api/v1/docs/',schema_view),
    path('api/v1/proposal/',include('proposals.urls'))
]
