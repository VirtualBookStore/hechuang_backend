from django.db import models
from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    address = models.TextField('地址', default='同济大学')
    publisher_email = models.EmailField('出版商的邮箱', default='1753764@tongji.edu.cn')
    discount_rate = models.FloatField('折扣率', default=0)
    old_rate = models.FloatField('折旧折扣率', default=0.3)
    recycle_rate = models.FloatField('回收折扣率', default=0.7)

    class Meta:
        verbose_name = "Site Configuration"