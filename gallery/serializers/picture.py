from lib.serializers import ModelSerializerBase
from gallery.models import Picture, PictureLang
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
            'original_jpeg': obj.to_url('picture'),
            'original_webp': obj.to_url('picture_webp'),
            'thumbnail_webp': obj.to_url('picture_thumbnail_webp'),
            'thumbnail_jpeg': obj.to_url('picture_thumbnail_jpeg'),
        }


class PictureSerializerPost(PictureSerializer):
    langs = PictureLangSerializer(many=True, required=False)

    class Meta(PictureSerializer.Meta):
        pass


class PictureSerializerGet(PictureSerializerPost):
    picture = SerializerMethodField()

    class Meta(PictureSerializerPost.Meta):
        pass


class PictureSerializerMinGet(PictureSerializerGet):
    class Meta(PictureSerializerGet.Meta):
        fields = ['title', 'picture', 'langs']
