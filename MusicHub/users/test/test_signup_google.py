from rest_framework import status
from rest_framework.test import APITestCase

from MusicHub.users.models import User


class TestUserSignInGoogleAPIView(APITestCase):
    def test_create_user_pass(self):
        """
        ! If you want to run this test with success you need to visit link below and
        ! create access token from google api and pase it to access_token variable - this should be done by front end part. link:
        ! https://developers.google.com/oauthplayground/#step1&apisSelect=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email%2Chttps%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&url=https%3A%2F%2F&content_type=application%2Fjson&http_method=GET&useDefaultOauthCred=unchecked&oauthEndpointSelect=Google&oauthAuthEndpointValue=https%3A%2F%2Faccounts.google.com%2Fo%2Foauth2%2Fv2%2Fauth&oauthTokenEndpointValue=https%3A%2F%2Foauth2.googleapis.com%2Ftoken&includeCredentials=unchecked&accessTokenType=bearer&autoRefreshToken=unchecked&accessType=offline&prompt=consent&response_type=code&wrapLines=on
        """
        access_token = "ya29.a0AVA9y1uHx1wHUhkLCRuSCdRn5LNdiPoAvCAhTkQSxyi6Y9mNrTfngPHXB-Qm7vaGUIJ_KVwhJl4ycW6MUNkGl08lY_rBokCH1RedS_fXXl7H9c84z2rjLdIQHYN1tvjVLTqj40mn7-ZxrivNOzrJjP6FbfJ2aCgYKATASARESFQE65dr8Stb6IfaW6V2QZyTpMlA6Pg0163"
        data = {"access_token": access_token}
        response = self.client.post("/social/google-oauth2/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.all()
        self.assertEqual(len(user), 1)

    def test_create_user_fail(self):
        data = {"access_token": "test"}
        response = self.client.post("/social/google-oauth2/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data2 = {"not_access_token": "test"}
        response = self.client.post("/social/google-oauth2/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
