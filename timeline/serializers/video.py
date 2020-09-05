from lib.serializers import ModelSerializerBase
from timeline.models import Video, VideoLang


class VideoLangSerializer(ModelSerializerBase):
    class Meta:
        model = VideoLang
        fields = ['title', 'language']


class VideoSerializer(ModelSerializerBase):
    langs = VideoLangSerializer(many=True, required=False)

    class Meta:
        model = Video
        fields = ['title', 'tags', 'event', 'video', 'langs']


class VideoSerializerPost(VideoSerializer):
    class Meta(VideoSerializer.Meta):
        pass


class VideoSerializerGet(VideoSerializerPost):
    class Meta(VideoSerializerPost.Meta):
        pass
