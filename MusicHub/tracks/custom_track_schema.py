from drf_yasg import openapi

from drf_yasg.inspectors import SwaggerAutoSchema


class CustomAutoSchema(SwaggerAutoSchema):
    def get_request_body_parameters(self, consumes):
        result = super().get_request_body_parameters(consumes)
        result.pop(0)
        return result


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
