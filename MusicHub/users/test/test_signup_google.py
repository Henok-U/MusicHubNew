from rest_framework import status
from rest_framework.authtoken.models import Token as SigninToken
from rest_framework.test import APITestCase

from MusicHub.users.models import User
from .base_test import CustomApiTestCase


class TestUserSignInGoogleAPIView(APITestCase):
    """
    ! If you want to run this test with success you need to visit link below and
    ! create access token from google api and pase it to access_token variable - this should be done by front end part. link:
    ! https://developers.google.com/oauthplayground/#step1&apisSelect=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email%2Chttps%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&url=https%3A%2F%2F&content_type=application%2Fjson&http_method=GET&useDefaultOauthCred=unchecked&oauthEndpointSelect=Google&oauthAuthEndpointValue=https%3A%2F%2Faccounts.google.com%2Fo%2Foauth2%2Fv2%2Fauth&oauthTokenEndpointValue=https%3A%2F%2Foauth2.googleapis.com%2Ftoken&includeCredentials=unchecked&accessTokenType=bearer&autoRefreshToken=unchecked&accessType=offline&prompt=consent&response_type=code&wrapLines=on
    """

    data = {"access_token": ""}

    def sent_request_and_assert_equal(self, data, status_code):
        response = self.client.post("/api/user/signin-social/google-oauth2/", data)
        self.assertEqual(response.status_code, status_code)
        return response

    def test_create_user_pass(self):
        self.sent_request_and_assert_equal(self.data, 200)
        user = User.objects.all()
        self.assertEqual(len(user), 1)

    def test_login_user_pass(self):
        self.sent_request_and_assert_equal(self.data, 200)
        token = SigninToken.objects.all()
        token.delete()
        response = self.sent_request_and_assert_equal(self.data, 200)
        self.assertContains(response, "token")

    def test_create_user_fail(self):
        data = {"access_token": "test"}
        self.sent_request_and_assert_equal(data, 400)

        self.sent_request_and_assert_equal({}, 400)

        response = self.client.post(
            "/api/user/signin-social/facebook-oauth/", self.data
        )
        self.assertEqual(response.status_code, 404)

        data = {"access_token": ""}
        self.sent_request_and_assert_equal(data, 400)
