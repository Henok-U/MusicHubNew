from drf_yasg import openapi

TOKEN_PARAMETER = openapi.Parameter(
    name="Authorization",
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    description="Authorization: token value",
    required=True,
)

signup_verify_parameters = [
    openapi.Parameter(
        "Token",
        openapi.IN_QUERY,
        description="Token (url_path)/?code=<token>",
        type=openapi.TYPE_STRING,
        required=True,
    ),
]


google_oauth_backend = openapi.Parameter(
    "backend",
    openapi.IN_PATH,
    description="backend type - currently supporting only google-oauth2",
    type=openapi.TYPE_STRING,
)
