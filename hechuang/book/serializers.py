import os

from django.core.files import File
import base64
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('isbn', 'title', 'description', 'tag', 'price', 'new_total', 'old_total', 'recommended')


class DetailedBookSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_cover(self, obj):
        isbn = obj.isbn
        try:
            with open(os.path.join('img', isbn + '.png'), 'rb') as f:
                image = File(f)
                data = base64.b64encode(image.read())
                return data
        except Exception as e:
            try:
                with open(os.path.join('img', 'img.png'), 'rb') as f:
                    image = File(f)
                    data = base64.b64encode(image.read())
                    return data
            except Exception as e:
                return ''
