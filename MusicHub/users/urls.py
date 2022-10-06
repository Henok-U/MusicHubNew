from django.urls import path

from MusicHub.users.views.profile_view import (
    AddUpdateProfilePicture,
    ChangePassword,
    ProfileView,
)

from .views.views import (
    RecoverPassword,
    SignInView,
    SignOutView,
    SignUpVerifyView,
    SignUpView,
    social_sign_google,
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signup/verify/", SignUpVerifyView.as_view(), name="signup-verify"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("signout/", SignOutView.as_view(), name="signout"),
    path("reset-password/", RecoverPassword.as_view(), name="reset-password"),
    path("signin-social/<str:backend>/", social_sign_google, name="signin-google"),
    # profile urls
    path("upload-photo/", AddUpdateProfilePicture.as_view(), name="upload-photo"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("change-password/", ChangePassword.as_view(), name="change-password"),
]
