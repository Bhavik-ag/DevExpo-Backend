from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Profile
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
import json

class RegestrationTestCase(APITestCase):
    
    def test_registration(self):
        data = {
            "username": "testcase",
            "email": "test@gmail.com",
            "password" : "dummypassword"
        }
        
        response = self.client.post("/user/register/", data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class LoginTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testcase", password="dummypassword", email="test@gmail.com")
        self.user.profile = Profile.objects.create(user=self.user)
        
    def test_username_login(self):
        data = {
            "username": "testcase",
            "password" : "dummypassword"
        }
        
        response = self.client.post("/user/login/", data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_email_login(self):
        data = {
            "username": "test@gmail.com",
            "password" : "dummypassword"
        }
        
        response = self.client.post("/user/login/", data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_wrong_password(self):
        data = {
            "username": "testcase",
            "password" : "wrongpassword"
        }
        
        response = self.client.post("/user/login/", data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_wrong_username(self):
        data = {
            "username": "wrongusername",
            "password" : "dummypassword"
        }
        
        response = self.client.post("/user/login/", data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
class ProfileTestCase(APITestCase):
        
    def setUp(self):
        self.user = User.objects.create_user(username="testcase", password="dummypassword", email="test@gmail.com")
        self.user.profile = Profile.objects.create(user=self.user)
        
        self.detail_url = reverse("profile-detail", kwargs={"username": self.user.username})
        
        self.token = RefreshToken.for_user(self.user).access_token
        
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        
    def test_profile_detail_get(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_profile_detail_patch(self):
        data = {
            "username": "testcase"
        }
        
        response = self.client.patch(self.detail_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_profile_detail_delete_unauthenticated(self):
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_profile_update_unauthenticated(self):
        data = {
            "bio" : "This is a test bio"
        }
        
        response = self.client.patch(reverse("profile-update",kwargs={"username": self.user.username}), data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_profile_detail_delete_authenticated(self):
        self.api_authentication()
        
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_profile_update_authenticated(self):
        self.api_authentication()
        
        data = {
            "first_name" : "test",
            "last_name" : "case",
            "bio" : "This is a updated test bio",
            "github" : "https://github.com/dummygithub",
            "linkedin" : "https://linkedin.com/dummylinkedin",
            "twitter" : "https://twitter.com/dummytwitter",
            "website" : "dummywebsite.com"
        }
        
        response = self.client.patch(reverse("profile-update",kwargs={"username": self.user.username}), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(json.loads(response.content),
                         {
                            "id" : self.user.id,
                            "username": "testcase",
                            "first_name" : "test",
                            "last_name" : "case",
                            "profile" : {
                                "bio" : "This is a updated test bio",
                                "github" : "https://github.com/dummygithub",
                                "linkedin" : "https://linkedin.com/dummylinkedin",
                                "twitter" : "https://twitter.com/dummytwitter",
                                "website" : "dummywebsite.com",
                                "profile_pic" : "https://res.cloudinary.com/dvj784usp/image/upload/v1687582654/profiles/user-default.jpg"
                            },
                            "projects" : []
                         })
         
class LogoutTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testcase", password="dummypassword", email="test@gmail.com")
        self.user.profile = Profile.objects.create(user=self.user)
        
        self.token = RefreshToken.for_user(self.user).access_token
        
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
    
    def test_logout(self):
        self.api_authentication()
        self.client.post(reverse("logout"))
        
        self.assertEqual(self.client.cookies["refresh"].value, "")
        self.assertEqual(self.client.cookies["access"].value, "")
        
