from rest_framework             import viewsets, status
from rest_framework.decorators  import action
from rest_framework.permissions import AllowAny
from rest_framework.response    import Response
from rest_framework.pagination  import CursorPagination
from django_filters             import utils

from accounts.managers import AccountManager
from accounts.models   import Account, TradeLog
from .serializers      import TradeLogSerializer
from .filters          import TradeLogListFilter


class AccountViewSet(viewsets.GenericViewSet):
    queryset = Account.objects.all()
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
        manager = AccountManager()
        account = manager.get_account(request.user, pk)
        pass

    @action(methods=['GET'], detail=True)
    def tradelogs(self, request, pk):
        """
        계좌 리스트 조회
        GET /accounts/{account_id}/tradelogs/
        """
        tradelogs = TradeLog.objects.filter(account_id=pk)
        
        filter_set = {
            'data'    : request.query_params,
            'queryset': tradelogs,
            'request' : request,
        }

        filterset = TradeLogListFilter(**filter_set)

        if not filterset.is_valid() and self.raise_exception:
            raise utils.translate_validation(filterset.errors)
            
        cursorPaginator = CursorPagination()
        cursorPaginator.page_size = 20

        ordering_filter           = {'desc' :'-created_at', 'asc' : 'created_at'}
        cursorPaginator.ordering = ordering_filter.get(filter_set['data'].get('order'), '-created_at')
        
        paginated_tradelogs = cursorPaginator.paginate_queryset(filterset.qs, request)
        result              = TradeLogSerializer(paginated_tradelogs, many=True)

        return cursorPaginator.get_paginated_response(result.data)


    @action(methods=['POST'], detail=True)
    def deposit(self, request, pk):
        """
        입금
        POST /accounts/{account_id}/deposit/
        """
        manager = AccountManager()
        account = manager.get_account(request.user, pk)
        account, trade_log = manager.deposit(account, request.data)
        # todo: 성공 리스폰스 처리
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def withdrawal(self, request, pk):
        """
        출금
        POST /accounts/{account_id}/withdrawal/
        """
        manager = AccountManager()
        account = manager.get_account(request.user, pk)
        account, trade_log = manager.withdrawal(account, request.data)
        # todo: 성공 리스폰스 처리
        return Response(status=status.HTTP_200_OK)