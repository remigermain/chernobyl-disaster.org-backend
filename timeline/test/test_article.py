from django.test import TestCase, tag
from timeline.models import Article, ArticleLang, Event
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


@tag('models', 'article')
class ArticleTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get_or_create(username="test", password="test")[0]
        self.event = Event.objects.create(title="test", creator=self.user, date=timezone.now())

    def test_create(self):
        obj = Article.objects.create(
            title="test",
            event=self.event,
            creator=self.user,
            link="https://test.fr"
            )
        self.assertIsNotNone(obj.id)

    def test_link(self):
        obj = Article(
            title="test",
            event=self.event,
            creator=self.user,
            link="wrong_link"
            )

        try:
            obj.save()
        except Exception as e:
            self.assertNotEqual(e, ValidationError)
            self.assertIsNotNone(e.error_dict['link'])


@tag('models', 'article', 'lang')
class ArticleLangTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get_or_create(username="test", password="test")[0]
        self.event = Event.objects.create(title="test", creator=self.user, date=timezone.now())
        self.article = Article.objects.create(
            title="test",
            event=self.event,
            creator=self.user,
            link="https://test.fr"
            )

    def test_create(self):
        obj = ArticleLang.objects.create(
            title="test",
            creator=self.user,
            extra=self.article
            )
        self.assertIsNotNone(obj.id)
        self.assertIsNotNone(obj.language, ArticleLang.lang_default)

    def test_same_lang(self):
        self.test_create()
        lang = ArticleLang.objects.first()
        lang.id = None

        try:
            lang.save()
            self.assertIsNotNone(lang.id)
        except Exception as e:
            self.assertNotEqual(e, ValidationError)
            self.assertIsNotNone(e.error_dict['__all__'])

    def test_lang_not_exist(self):
        self.test_create()
        lang = ArticleLang.objects.first()
        lang.id = None
        lang.language = "xx",

        try:
            lang.save()
            self.assertIsNotNone(lang.id)
        except Exception as e:
            self.assertNotEqual(e, ValidationError)
            self.assertIsNotNone(e.error_dict['language'])

    def test_new_lang(self):
        self.test_create()
        lang = ArticleLang.objects.first()
        lang.id = None
        lang.language = "fr"

        lang.save()
        self.assertIsNotNone(lang.id)
        self.assertEqual(lang.language, "fr")
