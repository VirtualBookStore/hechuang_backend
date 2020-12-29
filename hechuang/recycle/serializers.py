from rest_framework import serializers
from .models import RecycleRequest
from order.serializers import OrderSerializer


class RecycleRequestSerializer(serializers.ModelSerializer):
    order = OrderSerializer(many=False, read_only=False)
    message = serializers.CharField(max_length=200)

    class Meta:
        model = RecycleRequest
        fields = '__all__'

