from lib.drf import ModelSerializerBase, ModelSerializerBaseSafe
from timeline.models import Event, EventLang, Picture, Document, Video, \
    Article, PictureLang, DocumentLang, VideoLang, ArticleLang
from rest_framework.serializers import SerializerMethodField
from common.serializer import TagSerializerSafe


class PictureLangSerializer(ModelSerializerBase):
    class Meta:
        model = PictureLang
        fields = ['title', 'extra']


class PictureSerializer(ModelSerializerBase):
    langs = PictureLangSerializer(many=True)
    tags = TagSerializerSafe(many=True)

    class Meta:
        model = Picture
        fields = ['title', 'tags', 'event', 'picture', 'photographer', 'langs']


class PictureSerializerSafe(ModelSerializerBaseSafe):
    picture = SerializerMethodField()
    date = SerializerMethodField()

    class Meta(PictureSerializer.Meta):
        fields = PictureSerializer.Meta.fields + ['date']

    def get_picture(self, obj):
        return obj.picture.url

    def get_date(self, obj):
        if obj.event:
            return obj.event.date
        return None


"""
    Document serializer
"""


class DocumentLangSerializer(ModelSerializerBase):
    class Meta:
        model = DocumentLang
        fields = ['title', 'extra']


class DocumentSerializer(ModelSerializerBase):
    class Meta:
        model = Document
        fields = ['title', 'tags', 'event', 'doc']


class DocumentSerializerSafe(ModelSerializerBaseSafe):
    langs = DocumentLangSerializer(many=True)

    class Meta(DocumentSerializer.Meta):
        fields = DocumentSerializer.Meta.fields + ['langs']


"""
    Video Serializer
"""


class VideoLangSerializer(ModelSerializerBase):
    class Meta:
        model = VideoLang
        fields = ['title', 'extra']


class VideoSerializer(ModelSerializerBase):
    class Meta:
        model = Video
        fields = ['title', 'tags', 'event', 'video']


class VideoSerializerSafe(ModelSerializerBaseSafe):
    langs = VideoLangSerializer(many=True)

    class Meta(VideoSerializer.Meta):
        fields = VideoSerializer.Meta.fields + ['langs']


"""
    Article serializer
"""


class ArticleLangSerializer(ModelSerializerBase):
    class Meta:
        model = ArticleLang
        fields = ['title', 'extra']


class ArticleSerializer(ModelSerializerBase):
    class Meta:
        model = Article
        fields = ['title', 'tags', 'event', 'link']


class ArticleSerializerSafe(ModelSerializerBaseSafe):
    langs = ArticleLangSerializer(many=True)

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + ['langs']


"""
    Event serializer
"""


class EventLangSerializer(ModelSerializerBase):
    class Meta:
        model = EventLang
        fields = ['title', 'description', 'event']


class EventSerializer(ModelSerializerBase):
    class Meta:
        model = Event
        fields = ['title', 'date', 'tags']


class EventSerializerSafe(ModelSerializerBaseSafe):
    langs = EventLangSerializer(many=True)
    pictures = PictureSerializerSafe(many=True)
    documents = DocumentSerializerSafe(many=True)
    videos = VideoSerializerSafe(many=True)
    articles = ArticleSerializerSafe(many=True)

    class Meta(EventSerializer.Meta):
        fields = EventSerializer.Meta.fields + \
            ['langs', 'pictures', 'documents', 'videos', 'articles']
        depth = 5
