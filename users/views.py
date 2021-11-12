from rest_framework             import serializers
from rest_framework.generics    import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import RegisterUserSerializer


class RegisterUsertView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class   = RegisterUserSerializer
