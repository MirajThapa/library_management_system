from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

class LibraryAPITest(TestCase):
    def setUp(self):
        self.base_url = 'http:/127.0.0.1:8000/api'
        self.client = APIClient()

    def test_create_user(self):
        url = f'{self.base_url}/users/'
        data = {
            "Name": "Eliza Thapa",
            "Email": "ethapa@gmail.com",
            "MembershipDate": "2002-01-01"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_all_users(self):
        url = f'{self.base_url}/users/all/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_user_by_id(self):
        user_id = 1
        url = f'{self.base_url}/users/{user_id}/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_new_book(self):
        url = f'{self.base_url}/books/'
        data = {
            "Title": "Harry putter",
            "ISBN": "123407890123",
            "PublishedDate": "2022-01-01",
            "Genre": "Romance"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_all_books(self):
        url = f'{self.base_url}/books/all/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_all_borrowed_books(self):
        url = f'{self.base_url}/borrowed-books/all/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
