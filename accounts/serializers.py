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
    code = serializers.SerializerMethodField()

    class Meta:
        model = TradeLog
        exclude = (
            'id',
            'account',
        )

    def get_code(self, trade_log):
        if trade_log.code == TradeLog.TrageCodeChoice.DEPOSIT:
            rtn = "입금"
        if trade_log.code == TradeLog.TrageCodeChoice.WITHDRAW:
            rtn = "출금"
        return rtn


class TradeLogBodySerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    description = serializers.CharField(max_length=100)


class TradeLogQueryParamSerializer(serializers.Serializer):
    code = serializers.IntegerField(help_text="전체:미입력, 입금:1, 출금:2", required=False)
    order = serializers.IntegerField(help_text="asc or desc:default(-created_at)", required=False)
    start = serializers.IntegerField(help_text="ex) 2000-01-01", required=False)
    end = serializers.IntegerField(help_text="ex) 2000-01-01", required=False)
