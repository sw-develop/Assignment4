from django.conf                import settings
from django.contrib.auth        import get_user_model
from rest_framework.serializers import ModelSerializer

class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ('last_login', 'is_admin', 'username', 'first_name', 'last_name')
        read_only_fields = ('is_staff', 'last_login', 'is_admin', 'id')
        extra_kwargs = {'password' : {'write_only' : True}}

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)

class UserSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        exclude = ['password', 'is_admin']