from lib.drf import ModelSerializerBase
from timeline.models import Event, EventLang, Picture, Document, Video, \
    Article, PictureLang, DocumentLang, VideoLang, ArticleLang
from django.core.exceptions import ValidationError
from rest_framework.serializers import DateField


class PictureLangSerializer(ModelSerializerBase):
    class Meta:
        model = PictureLang
        fields = ['title', 'extra']


class PictureSerializer(ModelSerializerBase):
    class Meta:
        model = Picture
        fields = ['title', 'tags', 'event', 'picture', 'photographer']


class PictureSerializerSafe(ModelSerializerBase):
    langs = PictureLangSerializer(many=True)

    class Meta(PictureSerializer.Meta):
        fields = PictureSerializer.Meta.fields + ['langs']


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


class DocumentSerializerSafe(ModelSerializerBase):
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


class VideoSerializerSafe(ModelSerializerBase):
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


class ArticleSerializerSafe(ModelSerializerBase):
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


class EventSerializerSafe(EventSerializer):
    langs = EventLangSerializer(many=True)
    pictures = PictureSerializerSafe(many=True)
    documents = DocumentSerializerSafe(many=True)
    videos = VideoSerializerSafe(many=True)
    articles = ArticleSerializerSafe(many=True)

    class Meta(EventSerializer.Meta):
        fields = EventSerializer.Meta.fields + \
            ['langs', 'pictures', 'documents', 'videos', 'articles']
        depth = 5
