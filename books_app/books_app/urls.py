from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="MyBookList API",
      default_version='v1',
      description="An API for manage books and reading",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@mybooklist.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api/user/', include('user.urls')),
    path('api/', include('books.urls')),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0),
      name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0),
      name='schema-redoc'),
]
