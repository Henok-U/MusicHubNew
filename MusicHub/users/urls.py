from django.urls import path

from .views import (RecoverPassword, SignInView, SignOutView, SignUpVerifyView,
                    SignUpView, exchange_token)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signup/verify/", SignUpVerifyView.as_view(), name="signup-verify"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("signout/", SignOutView.as_view(), name="signout"),
    path("reset-password/", RecoverPassword.as_view(), name="reset-password"),
    path("signin-social/<str:backend>/", exchange_token, name="signin-google"),
]
