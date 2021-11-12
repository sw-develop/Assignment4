from django.db import transaction, IntegrityError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotFound, server_error, APIException
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.models import Account, TradeLog


class AccountViewSet(viewsets.GenericViewSet):
    queryset = Account.objects.all()
    # serializer_class =
    # todo: User 구현 되고 IsAuthenticated 로 변경
    permission_classes = [AllowAny]

    def get_account(self, request_user, account_id):
        try:
            account = Account.objects.get(id=account_id)
        except Account.DoesNotExist:
            raise NotFound(detail="error: Account Does Not Exist")
        if account.user != request_user:
            raise PermissionDenied()
        return account

    def deposit_or_withdrawal(self, account, data, code):
        # todo:에러 처리
        if code not in TradeLog.TrageCodeChoice.choices:
            raise APIException(detail="fdfdf")
        # todo: amount int value validation
        amount = data.get('amount')
        description = data.get('description')

        if code == TradeLog.TrageCodeChoice.DEPOSIT:
            if amount < 0:
                amount = amount * -1
        if code == TradeLog.TrageCodeChoice.WITHDRAW:
            if amount > 0:
                if account.balance < amount:
                    # todo: 에러처리
                    raise APIException(detail="잔액부족")
                amount = amount * -1

        try:
            with transaction.atomic():
                trade_log = TradeLog(
                    amount=amount, balance=account.balance + amount, description=description,
                    account=account, code=code
                )
                account.balance = account.balance + amount
                trade_log.save()
                account.save()
        except IntegrityError:
            # todo: 적정에러처리
            pass
        return account, trade_log

    def create(self, request):
        """
        계좌생성
        POST /accounts/
        """
        pass

    def retrieve(self, request, pk):
        """
        계좌 단건 조회
        GET /accounts/{account_id}/
        """
        account = self.get_account(request.user, pk)
        pass

    def list(self, request):
        """
        todo: 필요 없으면 삭제, 유저 정보 조회에서 처리할 수도?
        계좌 리스트 조회
        GET /accounts/
        """
        pass

    @action(methods=['POST'], detail=True)
    def deposit(self, request, pk):
        """
        입금
        POST /accounts/{account_id}/deposit/
        """
        account = self.get_account(request.user, pk)
        account, trade_log = self.deposit_or_withdrawal(account, request.data, TradeLog.TrageCodeChoice.DEPOSIT)
        # todo: 성공 리스폰스 처리
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def withdrawal(self, request, pk):
        """
        출금
        POST /accounts/{account_id}/withdrawal/
        """
        account = self.get_account(request.user, pk)
        account, trade_log = self.deposit_or_withdrawal(account, request.data, TradeLog.TrageCodeChoice.WITHDRAW)
        # todo: 성공 리스폰스 처리
        return Response(status=status.HTTP_200_OK)
