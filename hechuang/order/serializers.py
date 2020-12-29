from rest_framework import serializers
from book.serializers import BookSerializer
from user.serializers import PublicUserSerializer
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(many=False, read_only=True)
    book = BookSerializer(many=False, read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

