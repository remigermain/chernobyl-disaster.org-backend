from lib.serializers import ModelSerializerBase
from timeline.models import Picture, PictureLang
from drf_writable_nested.mixins import UniqueFieldsMixin
from drf_writable_nested.serializers import WritableNestedModelSerializer


class PictureLangSerializer(UniqueFieldsMixin, ModelSerializerBase):
    class Meta:
        model = PictureLang
        fields = ['id', 'title', 'language']


class PictureSerializer(ModelSerializerBase):
    langs = PictureLangSerializer(many=True, required=False)

    class Meta:
        model = Picture
        fields = ['title', 'tags', 'event', 'picture', 'photographer', 'langs']


class PictureSerializerPost(UniqueFieldsMixin, WritableNestedModelSerializer, PictureSerializer):
    class Meta(PictureSerializer.Meta):
        pass


class PictureSerializerGet(PictureSerializerPost):
    class Meta(PictureSerializerPost.Meta):
        pass
