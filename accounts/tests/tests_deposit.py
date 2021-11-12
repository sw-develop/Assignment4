from rest_framework      import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from ..models            import Account


class DepositTestCase(APITestCase):

    def setUp(self):
        self.eight_percent_user = get_user_model().objects.create_user(email="eight_percent@gmail.com", name="에잇퍼센트", password='12345678')
        self.wanted_user        = get_user_model().objects.create_user(email="wanted@gmail.com", name="원티드", password='12345678')

        self.eight_percent_account1 = Account.objects.create(user=self.eight_percent_user, name="일반통장", number="80-80-80-80", balance=40000)
        self.eight_percent_account2 = Account.objects.create(user=self.eight_percent_user, name="적금통장", number="81-81-81-81", balance=400000)
        self.wanted_account1  = Account.objects.create(user=self.wanted_user, name="일반통장", number="82-82-82-82", balance=5580000)

    def test_deposit_success(self):
        self.client.force_authenticate(self.eight_percent_user)

        data = """{
            "amount"      : "100000",
            "description" : "5월"
        }"""

        response = self.client.post(f'/accounts/{self.eight_percent_account2.id}/deposit/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['balance'], 500000)

    def test_deposit_failed_duto_no_login(self):
        data = """{
            "amount"      : "100000",
            "description" : "5월"
        }"""

        response = self.client.post(f'/accounts/{self.eight_percent_account2.id}/deposit/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deposit_failed_duto_invalid_json_data(self):
        self.client.force_authenticate(self.eight_percent_user)
        data = """{
            "amount"      : "만원",
            "description" :  "5월"
        }"""

        response = self.client.post(f'/accounts/{self.eight_percent_account2.id}/deposit/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_deposit_failed_duto_invalid_json_key(self):
        self.client.force_authenticate(self.eight_percent_user)
        data = """{
            "금액"        : "10000",
            "description" :  "5월"
        }"""

        response = self.client.post(f'/accounts/{self.eight_percent_account2.id}/deposit/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_deposit_failed_duto_no_body(self):
        self.client.force_authenticate(self.eight_percent_user)
        data = """{
        }"""

        response = self.client.post(f'/accounts/{self.eight_percent_account2.id}/deposit/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deposit_failed_duto_diffent_user_account(self):
        self.client.force_authenticate(self.wanted_user)

        data = """{
            "amount"      : "100000",
            "description" : "해킹"
        }"""

        response = self.client.post(f'/accounts/{self.eight_percent_account2.id}/deposit/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)