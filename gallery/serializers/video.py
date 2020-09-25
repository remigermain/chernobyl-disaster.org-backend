from lib.serializers import ModelSerializerBase
from gallery.models import Video, VideoLang


class VideoLangSerializer(ModelSerializerBase):
    class Meta:
        model = VideoLang
        fields = ['id', 'title', 'language']


class VideoSerializer(ModelSerializerBase):
    langs = VideoLangSerializer(many=True, required=False)

    class Meta:
        model = Video
        fields = ['id', 'title', 'tags', 'event', 'video', 'langs']


class VideoSerializerEvent(VideoSerializer):
    class Meta(VideoSerializer.Meta):
        fields = ['title', 'video', 'langs']
