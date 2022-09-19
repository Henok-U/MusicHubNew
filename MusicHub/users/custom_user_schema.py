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
        examples={"application/json": {"message": "error message"}},
    ),
}
