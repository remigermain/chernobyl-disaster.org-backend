def contenttypes_uuid(obj):
    """
        function for Issue models to generate the content_str by
        models app label + model name and object primary key
        easy to filter in queryset
    """
    return f"{obj._meta.app_label}|{obj._meta.model_name}|{obj.pk}"
