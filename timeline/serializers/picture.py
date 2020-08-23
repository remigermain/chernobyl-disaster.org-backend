from lib.serializers import ModelSerializerBase
from timeline.models import Picture, PictureLang
from rest_framework.serializers import SerializerMethodField


class PictureLangSerializer(ModelSerializerBase):
    class Meta:
        model = PictureLang
        fields = ['id', 'title', 'language']


class PictureSerializer(ModelSerializerBase):
    langs = PictureLangSerializer(many=True, required=False)

    class Meta:
        model = Picture
        fields = ['title', 'event', 'picture', 'photographer', 'langs', 'tags', 'date']

    def get_picture(self, obj):
        return {
            'full': obj.to_url('picture'),
            'thumbnail': obj.to_url('picture_thumbnail'),
        }


class PictureSerializerPost(PictureSerializer):
    langs = PictureLangSerializer(many=True, required=False)

    class Meta(PictureSerializer.Meta):
        pass


class PictureSerializerGet(PictureSerializerPost):
    picture = SerializerMethodField()

    class Meta(PictureSerializerPost.Meta):
        pass
