from drf_yasg import openapi


TOKEN_PARAMETER = openapi.Parameter(
    name="Authorization",
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    description="Authorization: token value",
    required=True,
)


def basic_response(success_status_code, success_message):
    return {
        success_status_code: openapi.Response(
            description="Successful action",
            examples={"application/json": {"message": success_message}},
        ),
        "400": openapi.Response(
            description="custom Error message",
            examples={
                "application/json": {"message": "error message", "status_code": "400"}
            },
        ),
    }
