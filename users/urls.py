from django.urls        import path, include
from django.conf.urls   import url

from .views             import RegisterUsertView


urlpatterns = [
    url('/', include('rest_auth.urls')),
    path('/signup/', RegisterUsertView.as_view(), name='registration'),
]