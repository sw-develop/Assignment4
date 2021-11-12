from rest_framework             import serializers, generics
from rest_framework.generics    import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework             import permissions
from .permissions               import IsOwner

from users.models               import User
from .serializers               import RegisterUserSerializer, UserSerializer


class RegisterUserView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class   = RegisterUserSerializer

class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]
