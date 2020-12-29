from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import *
from rest_framework.request import Request
from rest_framework.schemas.openapi import AutoSchema
from .models import SiteConfiguration
from .serializers import SiteConfigurationSerializer, PublicSiteConfigurationSerializer


class IsAdminUserOrReadOnly(BasePermission):
    def has_object_permission(self, request: Request, view, obj):

        if IsAuthenticated  and request.user.is_staff:
            return True
        else:
            if request.method in SAFE_METHODS:
                return True
        return False


class SiteConfigurationView(RetrieveUpdateAPIView):
    """
    全局的设置
    manager_email 管理员的电子邮箱

    publisher_email 出版商的电子邮箱

    discount_rate 折扣率，0-1,其中0代表没有折扣，1代表白送

    old_rate 折旧的折扣率，0-1,其中0代表没有折扣，1代表白送

    recycle_rate 回收的折扣率，0-1其中0代表没有折扣，1代表白送
    """
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = SiteConfigurationSerializer
    schema = AutoSchema(
        tags=['config', 'admin']
    )

    def get_object(self):
        return SiteConfiguration.get_solo()

    def get_queryset(self):
        return SiteConfiguration.get_solo()
