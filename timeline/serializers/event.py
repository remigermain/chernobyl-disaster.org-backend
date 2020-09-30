from lib.serializers import ModelSerializerBase
from timeline.models import Event, EventLang
from gallery.serializers.picture import PictureSerializerEvent
from gallery.serializers.video import VideoSerializerEvent
from rest_framework.serializers import SerializerMethodField


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
    date = None

    class Meta(EventSerializer.Meta):
        fields = EventSerializer.Meta.fields + ['have_hour', 'have_minute', 'have_second']


class EventSerializerTimeline(EventSerializer):
    pictures = PictureSerializerEvent(many=True, required=False)
    videos = VideoSerializerEvent(many=True, required=False)

    class Meta(EventSerializer.Meta):
        fields = EventSerializer.Meta.fields + \
            ['pictures', 'videos', 'slug']
