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
        description="Successfull password reset",
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

signin_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["email", "password"],
    properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING, description="email"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, description="password"),
    },
)
signin_return_schema = {
    "200": openapi.Response(
        description="User signed in successfully",
        examples={"application/json": {"token": "string"}},
    )
}

signup_verify_parameters = [
    openapi.Parameter(
        "Token",
        openapi.IN_QUERY,
        description="Successful verification\nGET api/accounts/signup/verify/?code=<token>",
        type=openapi.TYPE_STRING,
    ),
]
signup_verify_response = {
    "200": openapi.Response(
        description="User Verified!",
        examples={"application/json": {"message": "User verified succefully"}},
    ),
    "400": openapi.Response(
        description="custom Error message",
        examples={
            "application/json": {"message": "error message", "status_code": "400"}
        },
    ),
}

signout_parameters = [
    openapi.Parameter(
        name="token",
        in_=openapi.IN_HEADER,
        type=openapi.TYPE_STRING,
        description="Successful signout only possible if token is provided",
    ),
]

signout_verify_response = {
    "200": openapi.Response(
        description="User signed out",
        examples={"application/json": {"message": "User signed out succefully"}},
    ),
    "400": openapi.Response(
        description="custom Error message",
        examples={
            "application/json": {"message": "error message", "status_code": "400"}
        },
    ),
}

add_update_picture_body = openapi.Parameter(
    "picture",
    openapi.IN_FORM,
    type=openapi.TYPE_FILE,
    description="Picture to be uploaded",
)

add_update_picture_headear = openapi.Parameter(
    name="Authorization",
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    description="Authorization: token value",
)


add_update_picture_response = {
    "200": openapi.Response(
        description="Successful action",
        examples={"application/json": {"message": "Picture uploaded successfully"}},
    ),
    "400": openapi.Response(
        description="custom Error message",
        examples={
            "application/json": {"message": "error message", "status_code": "400"}
        },
    ),
}

profile_get_response = {
    "200": openapi.Response(
        description="User profile",
        examples={
            "application/json": {
                "email": "example@mail.com",
                "first_name": "example_name",
                "last_name": "example_surname",
            }
        },
    ),
    "401": openapi.Response(
        description="User profile",
        examples={"application/json": {"message": "Invalid token."}},
    ),
}


profile_parameters = [
    openapi.Parameter(
        name="Token",
        required=True,
        in_=openapi.IN_HEADER,
        type=openapi.TYPE_STRING,
        description="Profile endpoints are avaliable only with token",
    ),
]

profile_update_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["first_name", "last_name"],
    properties={
        "first_name": openapi.Schema(
            type=openapi.TYPE_STRING, description="first_name"
        ),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="last_name"),
    },
)

profile_update_responses = {
    "200": openapi.Response(
        description="Update successful",
        examples={"application/json": {"email": "User Updated succefully"}},
    ),
    "401": openapi.Response(
        description="User profile",
        examples={
            "application/json": {
                "message": "Authentication credentials were not provided."
            }
        },
    ),
}
authorization_token = [
    openapi.Parameter(
        name="Authorization",
        required=True,
        in_=openapi.IN_HEADER,
        type=openapi.TYPE_STRING,
        description="Header in format - Authorization: token <token>",
    ),
]
