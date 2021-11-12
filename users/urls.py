from django.urls        import path, include
from django.conf.urls   import url

from .views             import RegisterUserView, UserDetailAPIView

from rest_auth.views   import LoginView, LogoutView


urlpatterns = [
    path('/login/', LoginView.as_view(), name="user-login"),
    path('/logout/', LogoutView.as_view(), name='user-logout'),
    path('/signup/', RegisterUserView.as_view(), name='registration'),
    path('/<int:pk>/', UserDetailAPIView.as_view(), name='user_info'),
]