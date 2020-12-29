from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RecycleRequestViewSet

router = DefaultRouter()

router.register(r'', RecycleRequestViewSet, basename='recycle')
urlpatterns = router.urls
