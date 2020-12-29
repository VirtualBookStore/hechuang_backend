# Generated by Django 3.1.4 on 2020-12-29 12:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('price', models.IntegerField()),
                ('status', models.SmallIntegerField(choices=[(0, '出错'), (10, '缺货中'), (20, '已取消'), (30, '待支付'), (40, '已支付'), (60, '已完成'), (70, '申请回收中'), (90, '回收中'), (100, '已回收')], default=30)),
                ('old', models.BooleanField(default=False)),
                ('number', models.IntegerField(default=1)),
                ('book', models.ForeignKey(db_column='book_isbn', on_delete=django.db.models.deletion.CASCADE, related_name='books', to='book.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
