from core.drf import ModelSerializerBase
from timeline.models import Event, EventLang, Picture, Document, Video, \
    Article, PictureLang, DocumentLang, VideoLang, ArticleLang
from django.core.exceptions import ValidationError


class EventSerializer(ModelSerializerBase):
    class Meta:
        model = Event
        fields = ['title', 'date', 'tags']


class EventLangSerializer(ModelSerializerBase):
    class Meta:
        model = EventLang
        fields = ['title', 'description', 'event', 'language']


class PictureSerializer(ModelSerializerBase):
    class Meta:
        model = Picture
        fields = ['title', 'tags', 'event', 'image', 'photographer']


class DocumentSerializer(ModelSerializerBase):
    class Meta:
        model = Document
        fields = ['title', 'tags', 'event', 'image', 'doc']

    def validate(self, data):
        if 'image' not in data and 'doc' not in data:
            raise ValidationError("OneNotNothing")
        if 'image' in data and data['image'] and 'doc' in data and data['doc']:
            raise ValidationError("OneNotBoth")
        return data


class VideoSerializer(ModelSerializerBase):
    class Meta:
        model = Video
        fields = ['title', 'tags', 'event', 'video']


class ArticleSerializer(ModelSerializerBase):
    class Meta:
        model = Article
        fields = ['title', 'tags', 'event', 'link']


class PictureLangSerializer(ModelSerializerBase):
    class Meta:
        model = PictureLang
        fields = ['title', 'extra']


class DocumentLangSerializer(ModelSerializerBase):
    class Meta:
        model = DocumentLang
        fields = ['title', 'extra']


class VideoLangSerializer(ModelSerializerBase):
    class Meta:
        model = VideoLang
        fields = ['title', 'extra']


class ArticleLangSerializer(ModelSerializerBase):
    class Meta:
        model = ArticleLang
        fields = ['title', 'extra']
