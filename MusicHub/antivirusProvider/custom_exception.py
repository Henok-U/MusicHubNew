from rest_framework.exceptions import APIException


class CustomAntiVirusException(APIException):
    status_code = 400
    default_detail = "Error during scanning file"
