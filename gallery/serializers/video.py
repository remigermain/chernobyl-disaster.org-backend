from lib.serializers import ModelSerializerBase
from gallery.models import Video, VideoLang
from rest_framework.serializers import SerializerMethodField
from common.serializers.tag import TagSerializerMini


class VideoLangSerializer(ModelSerializerBase):
    class Meta:
        model = VideoLang
        fields = ['id', 'title', 'language']


class VideoSerializer(ModelSerializerBase):
    langs = VideoLangSerializer(many=True, required=False)
    date = SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'tags', 'event', 'video', 'langs', 'date']

    def get_date(self, obj):
        return {
            'date': obj.date,
            'have_hour': obj.have_hour,
            'have_minute': obj.have_minute,
            'have_second': obj.have_second
        }


class VideoSerializerPost(VideoSerializer):
    tags = TagSerializerMini(many=True, required=False)
    date = None

    class Meta(VideoSerializer.Meta):
        fields = VideoSerializer.Meta.fields + ['have_hour', 'have_minute', 'have_second']


class VideoSerializerEvent(VideoSerializer):
    class Meta(VideoSerializer.Meta):
        fields = ['id', 'title', 'video', 'langs']


class VideoSerializerMini(VideoSerializer):
    event = SerializerMethodField()

    class Meta(VideoSerializer.Meta):
        fields = ['id', 'title', 'event']

    def get_event(self, obj):
        if obj.event:
            return str(obj.event)
        return None
