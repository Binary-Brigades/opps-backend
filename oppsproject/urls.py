from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

schema_view = get_schema_view(
    openapi.Info(
        title="OOPS API Documentation",
        default_version='v1',
    ),
) 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/account/', include('dj_rest_auth.urls')),
    path('api/v1/account/register/', include('dj_rest_auth.registration.urls')),
    path('api/v1/docs/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-swagger-ui'),
    path('api/v1/proposal/', include('proposals.urls')),
    path('api/v1/user/', include('users.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()