
# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import PublicUserSerializer
from .models import HechuangUser


class UserView(RetrieveUpdateAPIView):
    serializer_class = PublicUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

