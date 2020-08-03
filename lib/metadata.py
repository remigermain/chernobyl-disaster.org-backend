from rest_framework import metadata, relations


class MetadataBase(metadata.SimpleMetadata):

    def get_choices(self, field):
        if hasattr(field, 'child_relation'):
            queryset = field.child_relation.get_queryset()
        else:
            queryset = field.get_queryset()
        if queryset is None:
            return {}
        return [{'value': item.pk, 'display_name': str(item)} for item in queryset]

    from django.forms import ModelForm

    def get_field_info(self, field):
        meta = super().get_field_info(field)
        if field.__class__ is relations.ManyRelatedField:
            meta['type'] = "many field"
            meta['choices'] = self.get_choices(field)
            meta['model'] = field.child_relation.queryset.model.__name__.lower()
        elif field.__class__ is relations.PrimaryKeyRelatedField:
            meta['choices'] = self.get_choices(field)
            meta['model'] = field.queryset.model.__name__.lower()
        return meta
