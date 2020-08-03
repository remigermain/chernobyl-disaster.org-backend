from django.test import tag
from lib.test import BaseTest
from common.models import People
from common.serializers.people import PeopleLangSerializer


@tag('model', 'lang', 'people')
class PeopleLangTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.people = People.objects.create(
            name='test',
            born=self.date,
            death=self.date2,
            wikipedia=self.link,
            profil=self.picture,
            creator=self.user
        )

    @tag('serializer')
    def test_create_serializer(self):
        data = {
            'biography': 'test',
            'people': self.people.pk,
            'language': self.lang
        }
        serialiser = PeopleLangSerializer(data=data, context=self.context)
        self.assertTrue(serialiser.is_valid())
        obj = serialiser.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.biography, data['biography'])
        self.assertEqual(obj.people, self.people)
        self.check_creator(obj)
        return obj

    @tag('serializer')
    def test_create_serializer_update(self):
        obj = self.test_create_serializer()
        old_biography = obj.biography
        old_language = obj.language
        data = {
            'biography': 'update-biography',
            'language': self.lang2
        }

        serialiser = PeopleLangSerializer(instance=obj, data=data, context=self.context, partial=True)
        self.assertTrue(serialiser.is_valid())
        updated = serialiser.save()
        self.assertEqual(updated.id, obj.id)
        self.assertNotEqual(updated.biography, old_biography)
        self.assertEqual(updated.biography, data['biography'])
        self.check_update_language(updated, old_language, data['language'])
        self.check_commit(updated)

    @tag('serializer')
    def test_create_serializer_update_wrong_lang(self):
        obj = self.test_create_serializer()
        data = {
            'language': self.lang_wrong
        }

        serialiser = PeopleLangSerializer(instance=obj, data=data, context=self.context, partial=True)
        self.assertFalse(serialiser.is_valid())

    @tag('serializer')
    def test_create_serializer_same_lang(self):
        obj = self.test_create_serializer()
        data = {
            'biography': 'biography',
            'people': obj.people.pk,
            'language': obj.language
        }
        serializer = PeopleLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_empty(self):
        data = {}

        serialiser = PeopleLangSerializer(data=data, context=self.context)
        self.assertFalse(serialiser.is_valid())
