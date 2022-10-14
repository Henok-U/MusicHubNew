from drf_yasg import openapi

# TODO This will be removed when branch from refactoring is merged
TOKEN_PARAMETER = openapi.Parameter(
    name="Authorization",
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    description="Authorization: token value",
    required=True,
)

optional_track_id = openapi.Parameter(
    name="track",
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    description="Track id to exclude playlist associated with this track",
    required=False,
)
