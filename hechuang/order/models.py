from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from notifications.signals import notify

from book.models import Book

User = get_user_model()


class Order(models.Model):
    class OrderStatus(models.IntegerChoices):
        ERROR = 0, '出错'
        OUT_OF_STOCK = 10, '缺货中'
        CANCELLED = 20, '已取消'
        NOT_PAID = 30, '待支付'
        PAID = 40, '已支付'
        FINISHED = 60, '已完成'
        REQUESTING_FOR_RECYCLE = 70, '申请回收中'
        RECYCLING = 90, '回收中'
        RECYCLED = 100, '已回收'

    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=False, null=False, related_name='books',
                             to_field='isbn', db_column='book_isbn')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name='users')
    time = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    status = models.SmallIntegerField(choices=OrderStatus.choices, default=OrderStatus.NOT_PAID)
    old = models.BooleanField(default=False)
    number = models.IntegerField(default=1)


@receiver(post_save, sender=Book, dispatch_uid="update_stock_count")
def update_stock(sender, instance: Book, created: bool, **kwargs):
    if created:
        return

    if instance.new_total <= 0:
        related_orders = Order.objects.filter(book=instance).filter(status=Order.OrderStatus.NOT_PAID)
        related_users = [order.user for order in related_orders]
        related_orders.update(status=Order.OrderStatus.OUT_OF_STOCK)
        try:
            notify.send(instance,
                        recipient=related_users,
                        verb=f'您的订单相关的书籍 {instance.isbn}: {instance.title} 书籍已缺货',
                        level='info', )
        finally:
            return
    if instance.new_total > 0:
        related_orders = Order.objects.filter(book=instance).filter(status=Order.OrderStatus.OUT_OF_STOCK)
        related_users = [order.user for order in related_orders]
        related_orders.update(status=Order.OrderStatus.NOT_PAID)
        try:
            notify.send(instance,
                        recipient=related_users,
                        verb=f'您的订单相关的书籍 {instance.isbn}: {instance.title} 已补货为{instance.new_total}本',
                        level='info', )
        finally:
            return
