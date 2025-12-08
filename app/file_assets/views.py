from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import uuid

from base_assets.views import BaseAssetViewSet
from . import models
from . import serializers
from .services.s3storage import S3StorageService


class FileAssetViewSet(BaseAssetViewSet):
    queryset = models.FileAsset.objects.all()
    serializer_class = serializers.FileAssetSerializer

    def __init__(self, **kwargs):
        self.s3_service = S3StorageService()
        super().__init__(**kwargs)

    @action(methods=['post'], detail=False, serializer_class=serializers.PresignRequestSerializer)
    def presign(self, request):
        """ Generate a presigned URL for direct upload to S3.

        Expected input: {"filename": "example.ipynb", "content_type": "application/json"}

        Returns:
            `key`: S3 object key (i.e. the path in the bucket)
            `url`: a presigned upload URL
        Return example:
            {
                "key": "files/383fecda-bc11-418c-ae81-d277c1bfd0d9_example.ipynb",
                "url": "http://localhost:9000/dev-bucket/files/383fecda-bc11-418c-ae81-d277c1bfd0d9_example.ipynb?AWSAccessKeyId=..."
            }
        """
        serializer = serializers.PresignRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        filename = serializer.validated_data["filename"]
        content_type = serializer.validated_data["content_type"]

        filename = filename.replace('/', '_')
        filename = models.FileAsset.file.field.generate_filename(
            None,
            f"{uuid.uuid4()}_{filename}",
            )

        key, url = self.s3_service.generate_presigned_upload_url(
            filename,
            content_type,
            )

        models.FileAssetCreationRequest.objects.create(file=key)

        return Response({
            "key": key,
            "url": url,
        })

    def perform_create(self, serializer):
        super().perform_create(serializer)
        related_creation_request = models.FileAssetCreationRequest.objects.filter(
            file=serializer.validated_data['key']
            )
        if related_creation_request:
            related_creation_request.delete()
