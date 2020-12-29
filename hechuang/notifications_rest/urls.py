from django.urls import re_path as url, path
from .views import GlobalNotificationView, NotificationViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', NotificationViewSet, basename='Notification')

urlpatterns = router.urls
urlpatterns += [
    path('all/', GlobalNotificationView.as_view(), )
]
app_name = 'notifications_rest'

