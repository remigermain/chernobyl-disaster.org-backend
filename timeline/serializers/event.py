from lib.serializers  import ModelSerializerBase
from timeline.models import Event, EventLang
from timeline.serializers.picture import PictureSerializerGet
from timeline.serializers.document import DocumentSerializerGet
from timeline.serializers.video import VideoSerializerGet
from timeline.serializers.article import ArticleSerializerGet


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
    pictures = PictureSerializerGet(many=True)
    documents = DocumentSerializerGet(many=True)
    videos = VideoSerializerGet(many=True)
    articles = ArticleSerializerGet(many=True)

    class Meta(EventSerializerPost.Meta):
        fields = EventSerializerPost.Meta.fields + \
            ['pictures', 'documents', 'videos', 'articles']
