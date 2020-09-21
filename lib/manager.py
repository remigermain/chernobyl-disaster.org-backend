from django.db import models
from django.db.models import Q, Count


class QuerySetBase(models.QuerySet):
    def completed(self, status=True):
        if not hasattr(self.model, 'langs'):
            return self
        _filter = {
            'available_langs': len(self.model.langs.field.model.lang_choices)
        }
        queryset = self.annotate(available_langs=Count('langs'))
        if status:
            return queryset.filter(**_filter)
        return queryset.filter(~Q(**_filter))

    def uncompleted(self):
        return self.completed(False)
