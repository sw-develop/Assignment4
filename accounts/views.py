from drf_yasg                   import openapi
from drf_yasg.utils             import swagger_auto_schema
from rest_framework             import viewsets, status
from rest_framework.decorators  import action
from rest_framework.response    import Response
from rest_framework.pagination  import CursorPagination
from django_filters             import utils

from accounts.managers import AccountManager
from accounts.models   import Account, TradeLog
from .permissions import IsOwner
from .serializers import TradeLogSerializer, TradeLogBodySerializer, TradeLogQueryParamSerializer
from .filters          import TradeLogListFilter
from accounts.serializers import AccountSerializer

from global_variable import DEFAULT_TOKEN

class AccountViewSet(viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsOwner]
    parameter_token = openapi.Parameter (
                                        "Authorization", 
                                        openapi.IN_HEADER, 
                                        description = "access_token", 
                                        type        = openapi.TYPE_STRING,
                                        default     = DEFAULT_TOKEN
    )
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        responses         = {
            "200": AccountSerializer,
            "401": "UNAUTHORIZED"
        },
        operation_id="계좌등록",
        operation_description = "header에 토큰이 필요합니다."
    )
    def create(self, request):
        """
        계좌생성
        POST /accounts/

        data params
        - name
        - number
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = Account.objects.create(
            name=request.data.get('name'),
            number=request.data.get('number'),
            user=request.user
        )
        return Response(self.get_serializer(account).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        responses         = {
            "200": AccountSerializer,
            "401": "UNAUTHORIZED",
            "404": "NOT FOUND"
        },
        operation_id="계좌 목록 조회",
        operation_description = "header에 토큰이 필요합니다."
    )
    def list(self, request):
        """
        계좌 리스트 조회
        GET /accounts/
        """
        accounts = Account.objects.filter(user=request.user).all()
        return Response(self.get_serializer(accounts, many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        request_body=TradeLogBodySerializer,
        responses={
            "200": TradeLogSerializer,
            "400": "BAD_REQUEST",
            "403": "PERMISSION_DENIED",
            "404": "NOT_FOUND",
        },
        operation_id="입금",
        operation_description="계좌에 입금을 합니다."
    )
    @action(methods=['POST'], detail=True)
    def deposit(self, request, pk):
        """
        입금
        POST /accounts/{account_id}/deposit/
        """
        manager = AccountManager()
        account = manager.get_account(request.user, pk)
        account, trade_log = manager.deposit(account, request.data)
        return Response(TradeLogSerializer(trade_log).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        request_body=TradeLogBodySerializer,
        responses={
            "200": TradeLogSerializer,
            "400": "BAD_REQUEST",
            "403": "PERMISSION_DENIED",
            "404": "NOT_FOUND",
        },
        operation_id="출금",
        operation_description="계좌에서 출금을 합니다."
    )
    @action(methods=['POST'], detail=True)
    def withdrawal(self, request, pk):
        """
        출금
        POST /accounts/{account_id}/withdrawal/
        """
        manager = AccountManager()
        account = manager.get_account(request.user, pk)
        account, trade_log = manager.withdrawal(account, request.data)
        return Response(TradeLogSerializer(trade_log).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        query_serializer=TradeLogQueryParamSerializer,
        responses={
            "200": TradeLogSerializer,
            "400": "BAD_REQUEST",
            "403": "PERMISSION_DENIED",
            "404": "NOT_FOUND",
        },
        operation_id="입출금 기록 조회",
        operation_description="계좌의 입출금 기록을 조회합니다."
    )
    @action(methods=['GET'], detail=True)
    def tradelogs(self, request, pk):
        """
        계좌 리스트 조회
        GET /accounts/{account_id}/tradelogs/
        """
        account = self.get_object()
        tradelogs = TradeLog.objects.filter(account_id=account.id)

        filter_set = {
            'data': request.query_params,
            'queryset': tradelogs,
            'request': request,
        }

        filterset = TradeLogListFilter(**filter_set)

        if not filterset.is_valid() and self.raise_exception:
            raise utils.translate_validation(filterset.errors)

        cursorPaginator = CursorPagination()
        cursorPaginator.page_size = 20

        ordering_filter = {'desc': '-created_at', 'asc': 'created_at'}
        cursorPaginator.ordering = ordering_filter.get(filter_set['data'].get('order'), '-created_at')

        paginated_tradelogs = cursorPaginator.paginate_queryset(filterset.qs, request)
        result = TradeLogSerializer(paginated_tradelogs, many=True)

        return cursorPaginator.get_paginated_response(result.data)
