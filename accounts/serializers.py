from django.db                  import models
from rest_framework.serializers import ModelSerializer

from .models import TradeLog


class TradeLogSerializer(ModelSerializer):

    class Meta:
        model = TradeLog
        exclude = ('account', )