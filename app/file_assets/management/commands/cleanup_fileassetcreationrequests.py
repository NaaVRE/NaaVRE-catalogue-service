import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone

from file_assets.models import FileAssetCreationRequest
from file_assets.services.s3storage import S3StorageService


class Command(BaseCommand):
    help = "Cleanup expired FileAssetCreationRequest instances for which no FileAsset was created."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.s3_service = S3StorageService()

    def handle(self, *args, **options):
        expire = self.s3_service.storage.querystring_expire
        cutoff_time = timezone.now() - datetime.timedelta(seconds=expire)

        # Query instances that match criteria
        instances = FileAssetCreationRequest.objects.with_fileasset_created().filter(
            fileasset_created=False,
            request_creation_date__lt=cutoff_time,
        )

        count = instances.count()
        if count == 0:
            self.stdout.write("No dangling FileAssetCreationRequest instances found.")
            return

        for obj in instances:
            # Delete the file if it exists
            if obj.file and obj.file.name and self.s3_service.exists(obj.file.name):
                try:
                    obj.file.storage.delete(obj.file.name)
                    self.stdout.write(f"Deleted s3 object: {obj.file.name}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error deleting S3 object: {obj.file.name}: {e}"))

            # Delete the model instance
            obj.delete()
            self.stdout.write(f"Deleted FileAssetCreationRequest: {obj}")

        self.stdout.write(self.style.SUCCESS(f"Cleanup complete. {count} instance(s) removed."))
