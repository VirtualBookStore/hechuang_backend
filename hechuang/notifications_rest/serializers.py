from rest_framework.serializers import ModelSerializer, RelatedField
from rest_framework import serializers
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from book.models import Book
from book.serializers import BookSerializer
from config.models import SiteConfiguration
from config.serializers import SiteConfigurationSerializer
from order.models import Order
from order.serializers import OrderSerializer
from recycle.serializers import RecycleRequestSerializer
from recycle.models import RecycleRequest
UserModel = get_user_model()


class UserSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = UserModel
        fields = ['id', ]


class ContentTypeSerializer(ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['app_label', 'model']


class GenericNotificationRelatedField(RelatedField):
    def to_representation(self, value):
        if isinstance(value, Book):
            serializer = BookSerializer(value)
        elif isinstance(value, Order):
            serializer = OrderSerializer(value)
        elif isinstance(value, RecycleRequest):
            serializer = RecycleRequestSerializer(value)
        elif isinstance(value, UserModel):
            serializer = UserSerializer(value)
        elif isinstance(value, SiteConfiguration):
            serializer = SiteConfigurationSerializer(value)
        elif isinstance(value, ContentType):
            serializer = ContentTypeSerializer(value)
        else:
            print(value)
            return None
        return serializer.data


class NotificationSerializer(ModelSerializer):
    recipient = UserSerializer()
    actor = GenericNotificationRelatedField(read_only=True)
    verb = serializers.CharField()
    level = serializers.CharField()
    description = serializers.CharField()
    timestamp = serializers.DateTimeField(read_only=True)
    unread = serializers.BooleanField()
    public = serializers.BooleanField()
    deleted = serializers.BooleanField()
    emailed = serializers.BooleanField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'target', 'verb', 'level', 'description', 'unread', 'public', 'deleted',
                  'emailed', 'timestamp']

    def create(self, validated_data):
        recipient_data = validated_data.pop('recipient')
        recipient = UserModel.objects.get_or_create(id=recipient_data['id'])
        actor_data = validated_data.pop('actor')
        actor = UserModel.objects.get_or_create(id=actor_data['id'])
        notification = Notification.objects.create(recipient=recipient[0], actor=actor[0], **validated_data)
        return notification
