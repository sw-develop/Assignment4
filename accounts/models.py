from django.db   import models
from django.conf import settings


class Account(models.Model): 

    class Meta: 
        db_table = 'accounts'

    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name       = models.CharField(max_length=20)
    number     = models.TextField(max_length=20)
    balance    = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TradeLog(models.Model): 

    class TrageCodeChoice(models.IntegerChoices): 
        DEPOSIT  = 1
        WITHDRAW = 2

    class Meta: 
        db_table = 'trade_logs'

    account     = models.ForeignKey(Account, on_delete=models.CASCADE, db_index=True)
    amount      = models.PositiveBigIntegerField()
    balance     = models.PositiveBigIntegerField()
    description = models.CharField(max_length=100)
    created_at  = models.DateTimeField(auto_now_add=True, db_index=True)
    code        = models.PositiveSmallIntegerField(choices=TrageCodeChoice.choices)