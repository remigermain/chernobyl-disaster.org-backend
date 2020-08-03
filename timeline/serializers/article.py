from lib.serializers import ModelSerializerBase
from timeline.models import Article, ArticleLang


class ArticleLangSerializer(ModelSerializerBase):
    class Meta:
        model = ArticleLang
        fields = ['title', 'language']


class ArticleSerializer(ModelSerializerBase):
    langs = ArticleLangSerializer(many=True, required=False)

    class Meta:
        model = Article
        fields = ['title', 'tags', 'event', 'link', 'langs']


class ArticleSerializerPost(ArticleSerializer):
    class Meta(ArticleSerializer.Meta):
        pass


class ArticleSerializerGet(ArticleSerializerPost):
    class Meta(ArticleSerializerPost.Meta):
        pass
