from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer

from user.models import HechuangUser


class HechuangUserSerializer(serializers.ModelSerializer):
    address = serializers.CharField(max_length=100)

    class Meta:
        model = HechuangUser
        fields = '__all__'


class PublicUserSerializer(serializers.ModelSerializer):
    address = serializers.CharField(max_length=100)

    class Meta:
        model = HechuangUser
        fields =('address', 'is_superuser', 'username', 'id', 'email',)