from rest_framework import serializers

from accounts.exceptions import BadRequestException
from accounts.models import Account, TradeLog


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'name',
            'number',
        )

    def validate(self, data):
        name = data.get('name')
        number = data.get('number')
        if name is None or number is None:
            raise BadRequestException('name or number')
        if Account.objects.filter(number=number).exists():
            raise BadRequestException('number')
        return data


class TradeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeLog
        exclude = ('account',)
