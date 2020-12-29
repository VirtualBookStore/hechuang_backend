import django_filters
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from order.models import Order
from .models import RecycleRequest
from .serializers import RecycleRequestSerializer


class StatusFilter(django_filters.FilterSet):
    orders = django_filters.ModelChoiceFilter(field_name="order__status",
                                              to_field_name='status',
                                              queryset=Order.objects.all())

    class Meta:
        model = RecycleRequest
        fields = ('order',)


class RecycleRequestViewSet(ReadOnlyModelViewSet):
    """
    管理员能看到所有的请求，用户智能看到自己的请求

    list : 获得所有
    查询字段 /?allowed 是否同意
           /?read  是否未新书
    """

    serializer_class = RecycleRequestSerializer
    queryset = RecycleRequest.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['allowed', 'read' 'order__status']
    filter_class = StatusFilter

