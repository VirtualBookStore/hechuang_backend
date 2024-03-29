from typing import *

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import  ReadOnlyModelViewSet
from rest_framework.schemas.openapi import AutoSchema

from notifications.signals import notify

from config.models import SiteConfiguration
from recycle.models import RecycleRequest
from book.models import Book
from recycle.serializers import RecycleRequestSerializer

from .models import Order
from user.permissons import IsOwner
from .serializers import OrderSerializer

User = get_user_model()


class OrderViewSet(ReadOnlyModelViewSet):
    """
    订单功能，顾客只能查看自己的订单，管理员可以查看所有订单那
    """
    serializer_class = OrderSerializer
    permission_classes = (IsAdminUser | IsOwner, )
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('status',)
    schema = AutoSchema(
        tags=('order', 'customer')
    )

    def get_queryset(self):
        queryset = Order.objects.all()
        user: User = self.request.user
        if not user.is_staff:
            queryset = queryset.filter(user=user)
        return queryset

    @staticmethod
    def _change_status(order: Order, new_status: Order.OrderStatus,
                       satisfied_old_status: Sequence[Order.OrderStatus]) -> Response:
        if order.status not in satisfied_old_status:
            raise APIException(detail='当前订单状态有误')
        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)

    '''
    取消订单
    '''
    @action(methods=['PATCH'], detail=True, url_name='cancelOrder', url_path='cancel',
            permission_classes=(IsOwner, ), description='取消订单')
    def cancel(self, request, *args, **kwargs):
        order: Order = self.get_object()
        return self._change_status(order, Order.OrderStatus.CANCELLED,
                                   (Order.OrderStatus.PAID, Order.OrderStatus.NOT_PAID))

    '''
    退款
    '''
    @action(methods=['PATCH'], detail=True, url_name='refundOrder', url_path='refund',
            permission_classes=(IsOwner, ), description='退款')
    def refund(self, request, *args, **kwargs):
        order: Order = self.get_object()
        return self._change_status(order, Order.OrderStatus.CANCELLED,
                                   (Order.OrderStatus.PAID,))

    '''
    支付
    '''
    @action(methods=['PATCH'], detail=True, url_name='payOrder', url_path='pay',
            permission_classes=(IsOwner, ), description='支付')
    def pay(self, request, *args, **kwargs):
        order: Order = self.get_object()
        book = order.book
        if order.old:
            book.old_total -= order.number
        else:
            book.new_total -= order.number
        book.save()
        return self._change_status(order, Order.OrderStatus.PAID,
                                   (Order.OrderStatus.NOT_PAID,))

    """
    收货
    """
    @action(methods=['PATCH'], detail=True, url_name='receiveOrder', url_path='receive',
            permission_classes=(IsOwner, ), description='确认收货')
    def receive(self, request, *args, **kwargs):
        order: Order = self.get_object()
        return self._change_status(order, Order.OrderStatus.FINISHED,
                                   (Order.OrderStatus.PAID, ))

    """
    申请回收
    "message" : 额外信息
    "number" : 回收数量
    """
    @action(methods=['POST'], detail=True, url_name='requestRecycle', url_path='recycle',
            permission_classes=(IsOwner, ), description='申请回收')
    def create_recycle_request(self, request, *args, **kwargs):
        message: str = request.data.get('message', '')
        order: Order = self.get_object()
        number: int = request.data.get('number', order.number)
        config: SiteConfiguration = SiteConfiguration.get_solo()
        price = int(order.price / order.number * number * (1 - config.recycle_rate))
        # notification = notify.send(user, manager, verb=f"{user.id} push  a recycle request for order {order.id}.")
        recycle_request: RecycleRequest = RecycleRequest.objects.create(
            order=order,
            message=message,
            price=price,
            number=number
        )
        manager = User.objects.get(is_staff=True)
        try:
            notify.send(sender=recycle_request,
                    recipient=manager,
                    verb=f'用户 {order.user.username} 对 {order.id} ({order.book.isbn} : {order.book.title}) 发送了回收请求: {recycle_request.message}',
                    level='info')
        finally:
            pass
        self._change_status(order, Order.OrderStatus.REQUESTING_FOR_RECYCLE, (Order.OrderStatus.FINISHED,))
        return Response(RecycleRequestSerializer(recycle_request).data, status=status.HTTP_201_CREATED)

    '''
    回收价格
    '''
    @action(methods=['GET'], detail=True, url_name='requestPrice', url_path='recycle/price',
            permission_classes=(IsOwner, ), description='申请回收')
    def create_recycle_price(self, request, *args, **kwargs):
        order: Order = self.get_object()
        number: int = request.data.get('number', order.number)
        config: SiteConfiguration = SiteConfiguration.get_solo()
        price = int(order.price / order.number * number * (1 - config.recycle_rate))
        return Response(price)


    '''
    审核回收
    "allowed": 结果, bool
    "price": 重新设定的价格
    '''
    @action(methods=['PATCH'], detail=True, url_name='requestRecycle', url_path='recycle/check',
            permission_classes=(IsAdminUser, ), description='审核回收')
    def check_recycle_request(self, request, *args, **kwargs):
        order: Order = self.get_object()
        if order.old:
            raise APIException("不能再次回收二手书")
        recycle_request: RecycleRequest = RecycleRequest.objects.get(order=order)
        try:
            result: bool = request.data.get('allowed').lower() == 'true'
        except Exception:
            raise APIException("allowed 字段未定义")
        price: int = int(request.data.get('price', recycle_request.price))
        recycle_request.price = price
        recycle_request.read = True
        recycle_request.allowed = result
        recycle_request.save()
        try:
            notify.send(recycle_request,
                    recipient=recycle_request.order.user,
                    verb=f'您的对 {order.id} ({order.book.isbn} : {order.book.title}) 的回收请求已审批，结果为{"通过" if result else "否决"}',
                    level='info')
        finally:
            pass
        new_status = Order.OrderStatus.RECYCLING if result else Order.OrderStatus.FINISHED
        self._change_status(order, new_status, (Order.OrderStatus.REQUESTING_FOR_RECYCLE,))
        return Response(RecycleRequestSerializer(recycle_request).data)

    '''
    回收收货
    '''
    @action(methods=['PATCH'], detail=True, url_name='recycle-receive', url_path='recycle/receive',
            permission_classes=(IsAdminUser,), description='回收收货')
    def receive_recycle(self, request, *args, **kwargs):
        order: Order = self.get_object()
        book: Book = order.book
        book.old_total += order.number
        book.save()
        self._change_status(order, Order.OrderStatus.RECYCLED, (Order.OrderStatus.RECYCLING,))
        recycle_request: RecycleRequest = RecycleRequest.objects.get(order=order)
        return Response(RecycleRequestSerializer(recycle_request).data)
