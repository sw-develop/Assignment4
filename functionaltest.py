from django.contrib.auth    import get_user_model
from rest_framework         import status
from rest_framework.test    import APITestCase
from accounts.models        import Account
from datetime               import date


# 1. 입금 시나리오 : 회원가입 -> 사용자 로그인 -> 계좌 생성 -> 입금 -> 입금 거래 내역 조회
class DepositTest(APITestCase):
    def setUp(self):
        # a. 회원가입
        data = {
            "email"     : "test01@gmail.com",
            "password"  : "test01test01**",
            "name"      : "에잇퍼센트"
        }
        self.client.post(
            "/users/signup/", data=data
        )

    def test_deposit_success_scenario(self):  # 입금 성공 시나리오
        # b. 사용자 로그인
        data = {
            "email"     : "test01@gmail.com",
            "password"  : "test01test01**",
        }

        response = self.client.post(
            "/users/login/", data=data
        )

        token = response.data['key']
        self.client.credentials(HTTP_AUTHORIZATION='token ' + token)  # 토큰 인증을 위한 설정

        # c. 계좌 생성
        data = {
            "number": "1002-1002",
            "name"  : "8퍼센트 통장"
        }

        response = self.client.post(
            "/accounts/", data=data
        )

        account_id = response.data['id']

        # d. 입금
        data = {
            "amount"        : "10000",
            "description"   : "입금"
        }

        self.client.post(
            f"/accounts/{account_id}/deposit/", data=data
        )

        # e. 입금 거래 내역 조회
        search_date = date.today()
        response = self.client.get(
            f"/accounts/{account_id}/tradelogs/?start={search_date}&code=1&order=desc"
        )

        account = Account.objects.get(id=account_id)
        self.assertEqual(account.balance, response.data['results'][0]['balance'])  # 현재 계좌의 잔액과 입금 내역의 잔액이 동일해야 함


# 2. 거래 내역 조회 시나리오 : 로그인 -> 입금/출금 내역 생성 -> 내역 조회 (fixture : 사용자, 계좌)
class ListTradeLogsTest(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(  # 사용자 계정 생성
            email       =   "test01@gmail.com",
            password    =   "test01test01**",
            name        =   "에잇퍼센트"
        )

        self.account = Account.objects.create(  # 계좌 생성
            user    =   user,
            name    =   "8퍼센트 통장",
            number  =   "1002-1002"
        )

    def test_list_tradelogs_success_scenario(self):
        # a. 사용자 로그인
        data = {
            "email"     : "test01@gmail.com",
            "password"  : "test01test01**",
        }

        response = self.client.post(
            "/users/login/", data=data
        )

        token = response.data['key']
        self.client.credentials(HTTP_AUTHORIZATION='token ' + token)  # 토큰 인증을 위한 설정

        # b. 입금/출금 내역 생성
        data = {
            "amount"        : "10000",
            "description"   : "입금"
        }

        self.client.post(
            f"/accounts/{self.account.id}/deposit/", data=data
        )

        data = {
            "amount"        : "5000",
            "description"   : "출금"
        }

        self.client.post(
            f"/accounts/{self.account.id}/withdrawal/", data=data
        )

        # c. 거래 내역 조회
        search_date = date.today()
        response = self.client.get(
            f"/accounts/{self.account.id}/tradelogs/?start={search_date}&order=desc"
        )

        account = Account.objects.get(id=self.account.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)                          # 거래 내역 2개 조회
        self.assertEqual(account.balance, response.data['results'][0]['balance'])   # 현재 계좌의 잔액과 마지막 거래 내역의 잔액이 동일해야 함


# 3. 출금 시나리오 :  로그인 -> 출금 -> 조회 (fixture : 사용자, 계좌, 계좌의 돈)
class WithdrawalTest(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(  # 사용자 계정 생성
            email       =   "test01@gmail.com",
            password    =   "test01test01**",
            name        =   "에잇퍼센트"
        )

        self.account = Account.objects.create(  # 계좌 생성
            user    =   user,
            name    =   "8퍼센트 통장",
            number  =   "1002-1002",
            balance =   "10000"
        )

    def test_withdrawal_success_scenario(self):  # 출금 성공 시나리오
        # a. 사용자 로그인
        data = {
            "email"     : "test01@gmail.com",
            "password"  : "test01test01**",
        }

        response = self.client.post(
            "/users/login/", data=data
        )

        token = response.data['key']
        self.client.credentials(HTTP_AUTHORIZATION='token ' + token)  # 토큰 인증을 위한 설정

        # b. 출금
        data = {
            "amount"        : "3000",
            "description"   : "출금"
        }

        self.client.post(
            f"/accounts/{self.account.id}/withdrawal/", data=data
        )

        # c. 출금 내역 조회
        search_date = date.today()
        response = self.client.get(
            f"/accounts/{self.account.id}/tradelogs/?start={search_date}&code=2&order=desc"
        )

        account = Account.objects.get(id=self.account.id)
        self.assertEqual(account.balance, response.data['results'][0]['balance'])  # 현재 계좌의 잔액과 출금 내역의 잔액이 동일해야 함


