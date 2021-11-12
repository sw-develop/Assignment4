from rest_framework             import generics
from rest_framework.generics    import CreateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth        import get_user_model

from .permissions               import IsOwner
from users.models               import User
from .serializers               import RegisterUserSerializer, UserSerializer


class RegisterUserView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class   = RegisterUserSerializer


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset           = get_user_model().objects.all()
    serializer_class   = UserSerializer
    permission_classes = [IsOwner]