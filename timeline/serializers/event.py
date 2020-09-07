from lib.serializers import ModelSerializerBase
from timeline.models import Event, EventLang
from timeline.serializers.picture import PictureSerializerGet
from timeline.serializers.video import VideoSerializerGet


class EventLangSerializer(ModelSerializerBase):
    class Meta:
        model = EventLang
        fields = ['title', 'description', 'language']


class EventSerializer(ModelSerializerBase):
    langs = EventLangSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = ['title', 'tags', 'date', 'langs']


class EventSerializerPost(EventSerializer):
    class Meta(EventSerializer.Meta):
        pass


class EventSerializerGet(EventSerializerPost):
    pictures = PictureSerializerGet(many=True, required=False)
    videos = VideoSerializerGet(many=True, required=False)

    class Meta(EventSerializerPost.Meta):
        fields = EventSerializerPost.Meta.fields + \
            ['pictures', 'videos', 'slug']