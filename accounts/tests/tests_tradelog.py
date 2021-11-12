from rest_framework      import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from ..models            import Account, TradeLog


class TradeLogTestCase(APITestCase):
    def setUp(self):
        self.eight_percent_user = get_user_model().objects.create_user(email="eight_percent@gmail.com", name="에잇퍼센트", password='12345678')
        self.wanted_user        = get_user_model().objects.create_user(email="wanted@gmail.com", name="원티드", password='12345678')

        self.eight_percent_account1 = Account.objects.create(user=self.eight_percent_user, name="일반통장", number="80-80-80-80", balance=40000)
        self.eight_percent_account2 = Account.objects.create(user=self.eight_percent_user, name="적금통장", number="81-81-81-81", balance=400000)
        self.wanted_account1  = Account.objects.create(user=self.wanted_user, name="일반통장", number="82-82-82-82", balance=5580000)

        TradeLog.objects.create(account=self.eight_percent_account1, amount=10000, balance=100000, description="점심 값", code=TradeLog.TrageCodeChoice.WITHDRAW)
        TradeLog.objects.create(account=self.eight_percent_account1, amount=10000, balance=90000, description="저녁 값", code=TradeLog.TrageCodeChoice.WITHDRAW)
        TradeLog.objects.create(account=self.eight_percent_account1, amount=50000, balance=40000, description="지인 결혼식", code=TradeLog.TrageCodeChoice.WITHDRAW)

        TradeLog.objects.create(account=self.eight_percent_account2, amount=100000, balance=100000, description="1월", code=TradeLog.TrageCodeChoice.DEPOSIT)
        TradeLog.objects.create(account=self.eight_percent_account2, amount=100000, balance=200000, description="2월", code=TradeLog.TrageCodeChoice.DEPOSIT)
        TradeLog.objects.create(account=self.eight_percent_account2, amount=100000, balance=300000, description="3월", code=TradeLog.TrageCodeChoice.DEPOSIT)
        TradeLog.objects.create(account=self.eight_percent_account2, amount=100000, balance=400000, description="4월", code=TradeLog.TrageCodeChoice.DEPOSIT)

        TradeLog.objects.create(account=self.wanted_account1, amount=50000, balance=5000000, description="조가 용돈", code=TradeLog.TrageCodeChoice.WITHDRAW)
        TradeLog.objects.create(account=self.wanted_account1, amount=500000, balance=4500000, description="부모님 용돈", code=TradeLog.TrageCodeChoice.WITHDRAW)
        TradeLog.objects.create(account=self.wanted_account1, amount=1000000, balance=5500000, description="알바비 입금", code=TradeLog.TrageCodeChoice.DEPOSIT)
        TradeLog.objects.create(account=self.wanted_account1, amount=20000, balance=5480000, description="배달음식", code=TradeLog.TrageCodeChoice.WITHDRAW)
        TradeLog.objects.create(account=self.wanted_account1, amount=100000, balance=5580000, description="용돈 입금", code=TradeLog.TrageCodeChoice.DEPOSIT)

    def test_get_tradelog_success(self):
        self.client.force_authenticate(self.eight_percent_user)
        response = self.client.get(f'/accounts/{self.eight_percent_account1.id}/tradelogs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    def test_get_tradelog_failed_duto_no_login(self):
        response = self.client.get(f'/accounts/{self.eight_percent_account1.id}/tradelogs/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_tradelog_failed_duto_diffent_user_account(self):
        self.client.force_authenticate(self.eight_percent_user)
        response = self.client.get(f'/accounts/{self.wanted_account1.id}/tradelogs/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)