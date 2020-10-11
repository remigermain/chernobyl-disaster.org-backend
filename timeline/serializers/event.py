from lib.serializers import ModelSerializerBase
from timeline.models import Event, EventLang
from gallery.serializers.picture import PictureSerializerEvent
from gallery.serializers.video import VideoSerializerEvent
from rest_framework.serializers import SerializerMethodField
from common.serializers.tag import TagSerializerMini


class EventLangSerializer(ModelSerializerBase):
    class Meta:
        model = EventLang
        fields = ['id', 'title', 'description', 'language']


class EventSerializer(ModelSerializerBase):
    langs = EventLangSerializer(many=True, required=False)
    date = SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'tags', 'date', 'langs']

    def get_date(self, obj):
        return {
            'date': obj.date,
            'have_hour': obj.have_hour,
            'have_minute': obj.have_minute,
            'have_second': obj.have_second
        }


class EventSerializerPost(EventSerializer):
    tags = TagSerializerMini(many=True, required=False)
    date = None

    class Meta(EventSerializer.Meta):
        fields = EventSerializer.Meta.fields + ['have_hour', 'have_minute', 'have_second']

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


class EventSerializerTimeline(EventSerializer):
    pictures = PictureSerializerEvent(many=True, required=False)
    videos = VideoSerializerEvent(many=True, required=False)

    class Meta(EventSerializer.Meta):
        fields = EventSerializer.Meta.fields + \
            ['pictures', 'videos', 'slug']


class EventSerializerMini(EventSerializer):
    class Meta(EventSerializer.Meta):
        fields = ['id', 'title', 'date']
