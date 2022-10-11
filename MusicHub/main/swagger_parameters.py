from drf_yasg import openapi

TOKEN_PARAMETER = openapi.Parameter(
    name="Authorization",
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    description="Authorization: token value",
    required=True,
)


def basic_response(success_status_code, success_message, error_message):
    return {
        success_status_code: openapi.Response(
            description="Successful action",
            examples={"application/json": success_message},
        ),
        error_message: openapi.Response(
            description="custom Error message",
            examples={
                "application/json": {
                    "message": "error message",
                    "status_code": error_message,
                }
            },
        ),
    }


def success_only_response(status_code, message):
    return {
        status_code: openapi.Response(
            description="Successful action",
            examples={"application/json": message},
        )
    }
