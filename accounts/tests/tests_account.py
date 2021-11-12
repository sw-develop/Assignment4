from rest_framework      import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from ..models            import Account


class AccountCreationTestCase(APITestCase):
    def setUp(self):
        self.eight_percent_user = get_user_model().objects.create_user(email="eight_percent@gmail.com", name="에잇퍼센트", password='12345678')

        self.eight_percent_account1 = Account.objects.create(user=self.eight_percent_user, name="일반통장", number="80-80-80-80", balance=40000)

    def test_create_account_success(self):
        self.client.force_authenticate(self.eight_percent_user)

        data = """{
            "number" : "84-84-84-84",
            "name"   : "비상금통장"
        }"""

        response = self.client.post(f'/accounts/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_account_fail_duto_no_duplicate_account_number(self):
        self.client.force_authenticate(self.eight_percent_user)

        data = """{
            "number" : "80-80-80-80",
            "name"   : "비상금통장"
        }"""

        response = self.client.post(f'/accounts/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_fail_duto_no_login(self):

        data = """{
            "number" : "84-84-84-84",
            "name"   : "비상금통장"
        }"""

        response = self.client.post(f'/accounts/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_account_fail_duto_no_body(self):
        self.client.force_authenticate(self.eight_percent_user)

        data = """{
        }"""

        response = self.client.post(f'/accounts/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_account_fail_duto_invalid_json_data(self):
        self.client.force_authenticate(self.eight_percent_user)

        data = """{
            "number" : "123456789012345678901",
            "name"   : "비상금통장"
        }"""

        response = self.client.post(f'/accounts/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_account_fail_duto_invalid_json_key(self):
        self.client.force_authenticate(self.eight_percent_user)

        data = """{
            "계좌번호" : 12345678910,
            "name"     : "비상금통장"
        }"""

        response = self.client.post(f'/accounts/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AccounListTestCase(APITestCase):
    def setUp(self):
        self.eight_percent_user = get_user_model().objects.create_user(email="eight_percent@gmail.com", name="에잇퍼센트", password='12345678')
        self.wanted_user        = get_user_model().objects.create_user(email="wanted@gmail.com", name="원티드", password='12345678')

        Account.objects.create(user=self.eight_percent_user, name="일반통장1", number="80-80-80-80", balance=40000)
        Account.objects.create(user=self.eight_percent_user, name="일반통장2", number="80-80-80-81", balance=40000)
        Account.objects.create(user=self.eight_percent_user, name="적금통장1", number="80-80-80-82", balance=40000)
        Account.objects.create(user=self.eight_percent_user, name="적금통장2", number="80-80-80-84", balance=40000)

    def test_get_account_list_success_have_account(self):
        self.client.force_authenticate(self.eight_percent_user)
        response = self.client.get(f'/accounts/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 4)
        
    def test_get_account_list_success_no_have_account(self):
        self.client.force_authenticate(self.wanted_user)
        response = self.client.get(f'/accounts/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)
