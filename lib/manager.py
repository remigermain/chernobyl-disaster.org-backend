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

    def prefetch_std(self, prefetch=None, select=None):
        query = self
        prefetch_lst = list() if not prefetch else prefetch
        select_lst = list() if not select else select

        if hasattr(self.model, "tags"):
            prefetch_lst.append("tags__langs")
        if hasattr(self.model, "langs"):
            prefetch_lst.append("langs")
        if hasattr(self.model, "prefetch_std"):
            print(self.model.prefetch_std, "iccc")
            prefetch_lst += self.model.prefetch_std
        if hasattr(self.model, "select_std"):
            select_lst += self.model.select_std
        if prefetch_lst:
            query = query.prefetch_related(*prefetch_lst)
        if select_lst:
            query = query.select_related(*select_lst)
        return query
