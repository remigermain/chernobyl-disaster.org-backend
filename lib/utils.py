def contenttypes_uuid(model, obj):
    """
        function for Issue models to generate the content_str by
        models app label + model name and object primary key
        easy to filter in queryset
    """
    return f"{model._meta.model_name}|{obj._meta.app_label}|{obj._meta.model_name}|{obj.pk}"
