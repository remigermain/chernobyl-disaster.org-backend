from lib.serializers import ModelSerializerBase
from timeline.models import Picture, PictureLang
from rest_framework.serializers import SerializerMethodField
import os
from django.conf import settings


class PictureLangSerializer(ModelSerializerBase):
    class Meta:
        model = PictureLang
        fields = ['id', 'title', 'language']

    def get_value(self, data):
        print("-=============== PictureLangSerializer")
        return ""


class PictureSerializer(ModelSerializerBase):
    langs = PictureLangSerializer(many=True, required=True)

    class Meta:
        model = Picture
        fields = ['title', 'event', 'picture', 'photographer', 'langs', 'tags', 'date']


class PictureSerializerPost(PictureSerializer):
    langs = PictureLangSerializer(many=True, required=True)

    class Meta(PictureSerializer.Meta):
        pass


class PictureSerializerGet(PictureSerializerPost):
    picture = SerializerMethodField()

    class Meta(PictureSerializerPost.Meta):
        pass

    def get_picture(self, obj):
        return os.path.join(settings.SITE_URL, obj.picture.url)
