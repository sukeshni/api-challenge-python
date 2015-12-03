from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Users
import datetime

class UserTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('user-create')
        data = {'username': 'testing1', 'email': 'testing1@testing.com', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Users.objects.count(), 1)
        self.assertEqual(Users.objects.get().username, 'testing1')

        data = {'username': 'testing2', 'email': 'testing2@testing.com', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Users.objects.count(), 2)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)      

class LoginTests(APITestCase):
    def test_login(self):
        u = Users(username='testing3', email='testing3@testing.com', password='password')
        u.save()
        url = reverse('login')
        data = {'email': 'testing3@testing.com', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  

class LogoutTests(APITestCase):
    def test_logout(self) :
        u = Users(username='testing4', email='testing4@testing.com', password='password')
        u.save()
        url = reverse('login')
        data = {'email': 'testing4@testing.com', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('logout')   
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

class ShowUser(APITestCase):
    def test_show_user(self):
        u = Users(id=5, username='testing5', email='testing5@testing.com', password='password')
        u.save()
        url = reverse('show-user', args=[5])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_user_not_present(self):
        url = reverse('show-user', args=[5])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UpdateUser(APITestCase):
    def test_update_username_without_login(self):   
        u = Users(id=6, username='testing6', email='testing6@testing.com', password='password')
        u.save()
        url = reverse('show-user', args=[6])
        data = {'username': 'user6'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)     

    def test_update_user_with_login(self):   
        u = Users(id=7, username='testing7', email='testing7@testing.com', password='password', birthday='1997-04-17')
        u.save()

        url = reverse('login')
        data = {'email': 'testing7@testing.com', 'password': 'password'}
        response = self.client.post(url, data, format='json')


        if self.assertEqual(response.status_code, status.HTTP_200_OK):
            url = reverse('show-user', args=[7])
            data = {'username': 'user7', 'email':'user7@testing.com', 'password':'password7', 'birthday':'1994-04-13', 'company':'Givery', 'location':'Tokyo'}
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)     
            self.assertEqual(Users.objects.get().username, 'user7')
            self.assertEqual(Users.objects.get().email, 'user7@testing.com') 
            self.assertEqual(Users.objects.get().password, 'password7')
            self.assertEqual(Users.objects.get().birthday, datetime.date(1994, 4, 13))   
            self.assertEqual(Users.objects.get().company, 'Givery')   
            self.assertEqual(Users.objects.get().location, 'Tokyo')   

class DeleteUser(APITestCase):
    def test_delete_username_without_login(self):   
        u = Users(id=8, username='testing8', email='testing8@testing.com', password='password')
        u.save()
        url = reverse('show-user', args=[8])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)     

    def test_delete_user_with_login(self):   
        u = Users(id=9, username='testing9', email='testing9@testing.com', password='password', birthday='1997-04-17')
        u.save()

        url = reverse('login')
        data = {'email': 'testing9@testing.com', 'password': 'password'}
        response = self.client.post(url, data, format='json')

        if self.assertEqual(response.status_code, status.HTTP_200_OK):
            url = reverse('show-user', args=[9])
            response = self.client.delete(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)       






