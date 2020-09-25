from lib.serializers import ModelSerializerBase
from timeline.models import Event, EventLang
from gallery.serializers.picture import PictureSerializerEvent
from gallery.serializers.video import VideoSerializerEvent


class EventLangSerializer(ModelSerializerBase):
    class Meta:
        model = EventLang
        fields = ['id', 'title', 'description', 'language']


class EventSerializer(ModelSerializerBase):
    langs = EventLangSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = ['id', 'title', 'tags', 'date', 'langs']


class EventSerializerTimeline(EventSerializer):
    pictures = PictureSerializerEvent(many=True, required=False)
    videos = VideoSerializerEvent(many=True, required=False)

    class Meta(EventSerializer.Meta):
        fields = EventSerializer.Meta.fields + \
            ['pictures', 'videos', 'slug']
