from django.http.response import Http404
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:

        if isinstance(exc, ValidationError):
            response.data["message"] = "Invalid: " + " ".join(
                f"{key} - {value[0]}" for key, value in exc.detail.items()
            )
        elif isinstance(exc, Http404):
            return response
        else:
            response.data["message"] = exc.detail
            response.data.pop("detail")
        response.data["status_code"] = response.status_code
    return response


class CustomUserException(APIException):
    status_code = 400
    default_detail = "Invalid data"


class CustomException(APIException):
    status_code = 400
    default_detail = "Invalid data"
