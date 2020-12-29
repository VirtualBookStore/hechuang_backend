from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, schemas
import rest_framework.urls

from api.views import APIInfoViewSet
from drf_yasg.openapi import Info
from drf_yasg.views import get_schema_view

import dj_rest_auth.urls
import dj_rest_auth.registration.urls

import order.urls
import book.urls
import config.urls
import notifications_rest.urls
import recycle.urls
import user.urls
router = routers.DefaultRouter()
router.register('api_info', APIInfoViewSet)

schema_view = get_schema_view(
    Info(
        title='hechuang',
        default_version='1.0.0',
        description='API for bookstore',
        version='1.0.0'
    ), public=True
)

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', include(router.urls), name='api'),
    path(r'api/', include(rest_framework.urls)),
    path(r'api/v1/book/', include(book.urls), name='book'),
    path(r'api/v1/config/', include(config.urls), name='config'),
    path(r'api/v1/order/', include(order.urls), name='order'),
    path(r'api/v1/auth/', include(dj_rest_auth.urls), name='rest_auth'),
    path(r'api/v1/auth/register/', include(dj_rest_auth.registration.urls), name='rest_auth'),
    path(r'api/v1/recycle/', include(recycle.urls), name='recycle-request'),
    path(r'api/v1/profile/', include(user.urls), name='profile'),
    path(r'api/v1/notification/', include(notifications_rest.urls, namespace='notification')),
    path(r'openapi/', schemas.get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    path(r'swagger-ui/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]

