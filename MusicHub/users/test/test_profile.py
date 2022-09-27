from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from MusicHub.users.models import User


class TestProfileView(APITestCase):
    def setUp(self):
        self.verified_user = User.objects.create_user(
            first_name="verified",
            last_name="user",
            email="verified@email.com",
            password="abcABC123*",
            is_verified=True,
        )
        self.verified_user.save()

        self.profile_url = reverse("profile")
        self.signin_url = reverse("signin")

    def test_successful_profile_view_and_edit(self):
        # user signes in first to make any changes
        signin_response = self.client.post(
            self.signin_url,
            {
                "email": "verified@email.com",
                "password": "abcABC123*",
            },
        )
        token = signin_response.data["token"]
        # authorize user to make chages
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # user profile data is available
        get_response = self.client.get(self.profile_url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, "verified@email.com")
        self.assertContains(get_response, "verified")
        self.assertContains(get_response, "user")
        self.assertNotContains(get_response, "password")

        # user changes profile info
        data = {
            "first_name": "Sam",
            "last_name": "Harris",
        }
        patch_response = self.client.patch(self.profile_url, data)

        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data["message"], "Profile Updated successfully")

        # check profile data change
        get_response = self.client.get(self.profile_url)
        self.assertContains(get_response, "Sam")
        self.assertContains(get_response, "Harris")
