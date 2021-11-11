from django.urls import path, include
from rest_framework.routers import SimpleRouter

from accounts.views import AccountViewSet

app_name = 'accounts'

router = SimpleRouter()

router.register('accounts', AccountViewSet, basename='accounts')

urlpatterns = [
    path('', include((router.urls, 'accounts')))
]
