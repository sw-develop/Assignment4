from django.db import transaction, IntegrityError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.models import Account, TradeLog


class AccountViewSet(viewsets.GenericViewSet):
    queryset = Account.objects.all()
    # serializer_class =
    # todo: User 구현 되고 IsAuthenticated 로 변경
    permission_classes = [AllowAny]

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
        try:
            account = Account.objects.get(id=pk)
        except Account.DoesNotExist:
            return Response({"error": "account does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if account.user != request.user:
            return Response({"error": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        # todo: amount int value validation
        amount = request.data.get('amount')
        description = request.data.get('description')

        if account.balance < amount:
            return Response({"error": "잔액 부족"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                trade_log = TradeLog(
                    amount=amount, balance=account.balance - amount, description=description,
                    account=account, code=TradeLog.TrageCodeChoice.DEPOSIT
                )
                account.balance = account.balance - amount
                trade_log.save()
                account.save()
        except IntegrityError:
            # todo: 적정에러처리
            return Response({'error': '오류발생'},status=status.HTTP_409_CONFLICT)
        # todo: 성공 리스폰스 처리
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def withdrawal(self, request, pk):
        """
        출금
        POST /accounts/{account_id}/withdrawal/
        """
        pass
