from django.urls        import path, include
from django.conf.urls   import url

from .views             import RegisterUserView, UserDetailAPIView


urlpatterns = [
    url('/', include('rest_auth.urls')),
    path('/signup/', RegisterUserView.as_view(), name='registration'),
    path('/<int:pk>/', UserDetailAPIView.as_view(), name='user_info'),
]