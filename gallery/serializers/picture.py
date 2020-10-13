from lib.serializers import ModelSerializerBase
from gallery.models import Picture, PictureLang
from rest_framework.serializers import SerializerMethodField
from common.serializers.tag import TagSerializerMini


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
        fields = ['id', 'title', 'event', 'picture', 'langs', 'tags', 'date']

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
    tags = TagSerializerMini(many=True, required=False)
    picture = None
    date = None

    class Meta(PictureSerializer.Meta):
        fields = PictureSerializer.Meta.fields + ['have_hour', 'have_minute', 'have_second']

    def validate(self, datas):
        if 'have_second' not in datas:
            datas['have_second'] = False
        elif datas['have_second']:
            datas['have_minute'] = True
            datas['have_hour'] = True

        if 'have_minute' not in datas:
            datas['have_minute'] = False
        elif datas['have_minute']:
            datas['have_hour'] = True

        if 'have_hour' not in datas:
            datas['have_hour'] = False

        return super().validate(datas)


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
