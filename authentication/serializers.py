from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserDetailsSerializer(serializers.ModelSerializer):
    scope = serializers.SerializerMethodField()
    """
    User model w/o password
    """
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'email', 'scope')
        read_only_fields = ('email', 'scope')

    def get_scope(self, obj):
        return {
            'staff': obj.is_staff or obj.is_superuser,
            'admin': obj.is_superuser,
        }
