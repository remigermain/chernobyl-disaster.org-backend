from lib.serializers import ModelSerializerBase
from gallery.models import Picture, PictureLang
from rest_framework.serializers import SerializerMethodField


class PictureLangSerializer(ModelSerializerBase):
    class Meta:
        model = PictureLang
        fields = ['id', 'title', 'language']


class PictureSerializer(ModelSerializerBase):
    langs = PictureLangSerializer(many=True, required=False)
    picture = SerializerMethodField()
    date = SerializerMethodField()

    class Meta:
        model = Picture
        fields = ['id', 'title', 'event', 'picture', 'photographer', 'langs', 'tags', 'date']

    def get_picture(self, obj):
        return {
            'original_jpeg': obj.picture.url,
            'original_webp': obj.picture_webp.url,
            'thumbnail_webp': obj.picture_thumbnail_webp.url,
            'thumbnail_jpeg': obj.picture_thumbnail_jpeg.url,
        }

    def get_date(self, obj):
        return {
            'date': obj.date,
            'have_hour': obj.have_hour,
            'have_minute': obj.have_minute,
            'have_second': obj.have_second
        }


class PictureSerializerPost(PictureSerializer):
    picture = None
    date = None

    class Meta(PictureSerializer.Meta):
        fields = PictureSerializer.Meta.fields + ['have_hour', 'have_minute', 'have_second']


class PictureSerializerEvent(PictureSerializer):
    class Meta(PictureSerializer.Meta):
        fields = ['id', 'title', 'picture', 'langs']


class PictureSerializerMini(PictureSerializer):
    event = SerializerMethodField()

    class Meta(PictureSerializer.Meta):
        fields = ['id', 'title', 'event']

    def get_event(self, obj):
        if obj.event:
            return str(obj.event)
        return None
