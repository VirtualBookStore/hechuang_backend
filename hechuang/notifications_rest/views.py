import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import ListModelMixin
from .serializers import NotificationSerializer
from notifications.models import Notification


class GlobalNotificationView(ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    schema = AutoSchema(
        component_name='GlobalNotification'
    )


class NotificationViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('unread',)

    schema = AutoSchema(
        component_name='Notification',
        operation_id_base='UserNotification'
    )

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(recipient=user)

    @action(methods=['get'], detail=False)
    def count(self, request, *args, **kwargs):
        count = self.queryset.count()
        data = {
            'count': count
        }
        return Response(data)

    @action(methods=['patch'], url_path='mark-all-read', detail=False)
    def mark_all_as_read(self, request, *args, **kwargs):
        self.queryset.update(unread=False)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['patch'], url_path='mark-all-unread', detail=False)
    def mark_all_as_unread(self, request, *args, **kwargs):
        self.queryset.update(unread=False)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['patch'], url_path='mark-read', detail=True)
    def mark_as_read(self, request, *args, **kwargs):
        notification: Notification = self.get_object()
        notification.unread = False
        notification.save()
        return Response(notification, status=status.HTTP_200_OK)

    @action(methods=['patch'], url_path='mark-unread', detail=True)
    def mark_as_unread(self, request, *args, **kwargs):
        notification: Notification = self.get_object()
        notification.unread = True
        notification.save()
        return Response(notification, status=status.HTTP_200_OK)
