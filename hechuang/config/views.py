from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import *
from rest_framework.request import Request
from rest_framework.schemas.openapi import AutoSchema

from user.permissons import IsAdminUserOrReadOnly
from .models import SiteConfiguration
from .serializers import SiteConfigurationSerializer, PublicSiteConfigurationSerializer

config = SiteConfiguration.get_solo()


class SiteConfigurationView(RetrieveUpdateAPIView):
    """
    全局的设置


    publisher_email 出版商的电子邮箱

    discount_rate 折扣率，0-1,其中0代表没有折扣，1代表白送

    old_rate 折旧的折扣率，0-1,其中0代表没有折扣，1代表白送

    recycle_rate 回收的折扣率，0-1其中0代表没有折扣，1代表白送
    """
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = SiteConfigurationSerializer
    schema = AutoSchema(
        tags=['config', 'admin']
    )

    def get_object(self):
        return SiteConfiguration.get_solo()

    def get_queryset(self):
        return SiteConfiguration.get_solo()
