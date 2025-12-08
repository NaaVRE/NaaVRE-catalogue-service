from base_assets.models import VersioningMixin
from file_assets.models import FileAsset


class WorkflowFile(FileAsset, VersioningMixin):
    pass
