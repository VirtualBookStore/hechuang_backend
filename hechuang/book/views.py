from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from config.models import SiteConfiguration
from order.models import Order
from order.serializers import OrderSerializer
from notifications.signals import notify

from user.permissons import IsAdminUserOrReadOnly, IsCustomer
from .models import Book
from .serializers import DetailedBookSerializer

User = get_user_model()


class BookViewSet(ModelViewSet):
    """
        其中推荐倒序
    """
    permission_classes = (IsAdminUserOrReadOnly, )
    serializer_class = DetailedBookSerializer
    filter_backends = [SearchFilter]
    filterset_fields = ('recommended', )
    search_fields = ('$title', '=tags__label')

    schema = AutoSchema(
        tags=['book', 'customer']
    )

    def get_queryset(self):
        return Book.objects.all().order_by('-recommended')

    @action(methods=('patch',), detail=True, url_path='recommend', description="推荐书本，recommended参数：布尔值")
    def recommend(self, request: Request, pk=None) -> Response:
        recommended: bool = getattr(request.data, 'recommend', True)
        book: Book = self.get_object()
        serializer = self.get_serializer(book, data={'recommended': recommended}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('get',), detail=True, url_path='price', permission_classes=(AllowAny,), description='买书')
    def price(self, request: Request, pk=None) -> Response:
        purchase_total = int(request.data.get('total', 1))
        purchase_old = request.data.get('old', False)

        book: Book = self.get_object()
        price = self._calc_promotion(book, purchase_old, purchase_total)
        return Response(price, status=status.HTTP_200_OK)

    @action(methods=('post',), detail=True, url_path='purchase', permission_classes=(IsCustomer,), description='买书')
    def purchase(self, request: Request, pk=None) -> Response:
        user: User = request.user
        purchase_total = int(request.data.get('total', 1))
        purchase_old = request.data.get('old', False)

        book: Book = self.get_object()
        stock_total = book.old_total if purchase_old else book.new_total
        price = self._calc_promotion(book, purchase_old, purchase_total)
        if stock_total < purchase_total:
            conf: SiteConfiguration = SiteConfiguration.objects.get()
            if purchase_old:
                raise APIException('旧书不足,请考虑购买新书')
            else:
                manager = User.objects.get(is_staff=True)
                notify.send(book,
                            recipient=manager,
                            verb=f'{book.isbn}:{book.title} 书籍已缺货，请补货',
                            level='warning')
            order_status = Order.OrderStatus.OUT_OF_STOCK
        else:
            order_status = Order.OrderStatus.NOT_PAID

        order: Order = Order.objects.create(user=user, book=book, price=price, status=order_status, number=purchase_total, old=purchase_old)
        notify.send(order,
                    recipient=user,
                    verb=f'对 {book.isbn}:{book.title} 的订单 {order.id} 已创建',
                    level='success', )

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def _calc_promotion(book: Book, purchase_old: bool, purchase_total: int) -> int:
        discount_rate = SiteConfiguration.get_solo().discount_rate
        old_rate = SiteConfiguration.get_solo().old_rate
        res = book.price * purchase_total * (1 - discount_rate)
        if purchase_old:
            res *= 1 - old_rate
        return int(res)