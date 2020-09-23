from utils.function import contenttypes_uuid
from utils.models import Commit


def delete_commit(sender, **kwargs):
    uuid = contenttypes_uuid(kwargs['instance'])
    Commit.objects.filter(uuid=uuid).delete()
