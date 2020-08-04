from lib.serializers import ModelSerializerBase
from timeline.models import Picture, PictureLang
from drf_writable_nested.mixins import UniqueFieldsMixin
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.serializers import PrimaryKeyRelatedField
from django.core.exceptions import ValidationError


class PictureLangSerializer(ModelSerializerBase):
    class Meta:
        model = PictureLang
        fields = ['id', 'title', 'language']


class PictureSerializer(ModelSerializerBase):
    langs = PictureLangSerializer(many=True, required=False)

    class Meta:
        model = Picture
        fields = ['title', 'tags', 'event', 'picture', 'photographer', 'langs']


class PictureSerializerPost(PictureSerializer):
    langs = PictureLangSerializer(many=True, required=False)

    class Meta(PictureSerializer.Meta):
        pass


class PictureSerializerGet(PictureSerializerPost):
    class Meta(PictureSerializerPost.Meta):
        pass
