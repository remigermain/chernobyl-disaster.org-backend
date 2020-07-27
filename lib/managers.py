from django.db import models
from .utils import contenttypes_uuid


class CherManager(models.Manager):
    def get_issue(self):
        """
            return all issues on this models
        """
        from common.models import Issue
        return Issue.objects.filter(uuid=contenttypes_uuid(Issue, self))

    @property
    def issue_count(self):
        return self.get_issue().count()

    def get_commit(self):
        """
            return all commits from this models
        """
        from common.models import Commit
        return Commit.objects.filter(uuid=contenttypes_uuid(Commit, self))

    @property
    def commit_count(self):
        return self.get_commit().count()