from django.urls import path


from .views import (
    SignUpVerifyView,
    SignInView,
    SignOutView,
    SignUpView,
    RecoverPassword,
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signup/verify/", SignUpVerifyView.as_view(), name="signup-verify"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("signout/", SignOutView.as_view(), name="signout"),
    path("reset-password/", RecoverPassword.as_view(), name="reset-password"),
]
