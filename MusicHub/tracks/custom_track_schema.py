from drf_yasg import openapi

# upload track
track_file = openapi.Parameter(
    name="file", in_=openapi.IN_FORM, type=openapi.TYPE_FILE, required=True
)
is_public = openapi.Parameter(
    name="is_public", in_=openapi.IN_FORM, type=openapi.TYPE_BOOLEAN, required=True
)


list_example = {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "filename": "string",
            "track_length": "02:00",
            "created_at": "05:51:2022",
            "public": "true",
            "playlist": "string",
        }
    ],
}
