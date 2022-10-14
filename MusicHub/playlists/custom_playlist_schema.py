from drf_yasg import openapi

# TODO This will be removed when branch from refactoring is merged
TOKEN_PARAMETER = openapi.Parameter(
    name="Authorization",
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    description="Authorization: token value",
    required=True,
)
