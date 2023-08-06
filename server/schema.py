from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from server.serializers import ServerSerializer, ChannelSerilaizer


server_list_docs = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="category_id",
            type=OpenApiTypes.INT,
            description="Category of service to retrieve",
            location=OpenApiParameter.QUERY,
        )
    ],
)
