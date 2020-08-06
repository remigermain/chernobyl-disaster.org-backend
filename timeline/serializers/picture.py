from lib.serializers import ModelSerializerBase
from timeline.models import Picture, PictureLang


class PictureLangSerializer(ModelSerializerBase):
    class Meta:
        model = PictureLang
        fields = ['id', 'title', 'language']


class PictureSerializer(ModelSerializerBase):
    langs = PictureLangSerializer(many=True, required=False)

    class Meta:
        model = Picture
        fields = ['title', 'event', 'picture', 'photographer', 'langs', 'tags']


class PictureSerializerPost(PictureSerializer):
    langs = PictureLangSerializer(many=True, required=False)

    class Meta(PictureSerializer.Meta):
        pass


class PictureSerializerGet(PictureSerializerPost):
    class Meta(PictureSerializerPost.Meta):
        pass
