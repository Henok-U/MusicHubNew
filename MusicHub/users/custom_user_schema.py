from drf_yasg import openapi

signup_return_schema = {
    "201": openapi.Response(
        description="Successfull creation of user",
        examples={
            "application/json": {
                "id": "uuid string",
                "email": "example@mail.com",
                "first_name": "example_name",
                "last_name": "example_surname",
            }
        },
    ),
    "400": openapi.Response(
        description="custom Error message",
        examples={
            "application/json": {"message": "error message", "status_code": "400"}
        },
    ),
}
google_oauth_backend = openapi.Parameter(
    "backend",
    openapi.IN_PATH,
    description="backend type - currently supporting only google-oauth2",
    type=openapi.TYPE_STRING,
)
google_oauth_return = {
    "200": openapi.Response(
        description="Successfull creation of user",
        examples={"application/json": {"token": "Authorization token"}},
    ),
    "400": openapi.Response(
        description="custom Error message",
        examples={
            "application/json": {"message": "error message", "status_code": "400"}
        },
    ),
}

reset_password_returns = {
    "200": openapi.Response(
        description="Successfull creation of user",
        examples={"application/json": {"data": "Success"}},
    ),
    "400": openapi.Response(
        description="custom Error message",
        examples={
            "application/json": {"message": "error message", "status_code": "400"}
        },
    ),
}


reset_password_query = openapi.Parameter(
    "code",
    openapi.IN_QUERY,
    description="String containing code from email link",
    type=openapi.TYPE_STRING,
)
