from django.urls import path, include

from .views import UserView

urlpatterns = [
    path(r'', UserView.as_view(), name='profile')
]

