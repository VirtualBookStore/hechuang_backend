from rest_framework.serializers import ModelSerializer
from .models import SiteConfiguration


class SiteConfigurationSerializer(ModelSerializer):
    class Meta:
        model = SiteConfiguration
        fields = '__all__'


class PublicSiteConfigurationSerializer(ModelSerializer):
    class Meta:
        model = SiteConfiguration
        fields = ('discount_rate', 'old_rate', 'recycle_rate', 'address')

