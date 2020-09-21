from lib.serializers import ModelSerializerBase
from timeline.models import Event, EventLang
from gallery.serializers.picture import PictureSerializerMinGet
from gallery.serializers.video import VideoSerializerMinGet


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
    pictures = PictureSerializerMinGet(many=True, required=False)
    videos = VideoSerializerMinGet(many=True, required=False)

    class Meta(EventSerializerPost.Meta):
        fields = EventSerializerPost.Meta.fields + \
            ['pictures', 'videos', 'slug']
