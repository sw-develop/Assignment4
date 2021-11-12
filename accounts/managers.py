from django.db import transaction, IntegrityError
from rest_framework.exceptions import NotFound, PermissionDenied, APIException

from accounts.exceptions import BadRequestException
from accounts.models import Account, TradeLog


class AccountManager:

    def get_account(self, request_user, account_id):
        try:
            account = Account.objects.get(id=account_id)
        except Account.DoesNotExist:
            raise NotFound(detail="error: Account Does Not Exist")
        if account.user != request_user:
            raise PermissionDenied()
        return account

    def deposit(self, account, data):
        return self._deposit_or_withdrawal(account, data, TradeLog.TrageCodeChoice.DEPOSIT)

    def withdrawal(self, account, data):
        return self._deposit_or_withdrawal(account, data, TradeLog.TrageCodeChoice.WITHDRAW)

    def _deposit_or_withdrawal(self, account, data, code):
        amount = data.get('amount')
        description = data.get('description')
        print(description)
        if amount is None or description is None:
            raise BadRequestException('amount or description')
        try:
            amount = int(amount)
        except ValueError:
            raise BadRequestException('amount')
        if amount < 0:
            amount = amount * -1
        if code == TradeLog.TrageCodeChoice.DEPOSIT:
            balance = account.balance + amount
        if code == TradeLog.TrageCodeChoice.WITHDRAW:
            if account.balance < amount:
                raise APIException(detail="잔액부족")
            balance = account.balance - amount

        try:
            with transaction.atomic():
                trade_log = TradeLog(
                    amount=amount, balance=balance, description=description,
                    account=account, code=code
                )
                account.balance = balance
                trade_log.save()
                account.save()
        except IntegrityError:
            raise APIException(detail="오류가 발생했습니다. 입출금이 이뤄지지 않았습니다.")

        return account, trade_log
