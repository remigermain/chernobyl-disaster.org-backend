from django.test import tag
from common.serializers.people import PeopleSerializer
from lib.test import BaseTest


@tag('model', 'people')
class PeopleTest(BaseTest):

    @tag('serializer')
    def test_create_serializer(self):
        data = {
            'name': 'test',
            'born': self.date,
            'death': self.date2,
            'wikipedia': self.link,
            'profil': self.picture
        }
        serializer = PeopleSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.name, data['name'])
        self.assertEqual(obj.born, data['born'])
        self.assertEqual(obj.death, data['death'])
        self.assertEqual(obj.wikipedia, data['wikipedia'])
        self.check_creator(obj)
        return obj

    @tag('serializer')
    def test_create_serializer_update(self):
        obj = self.test_create_serializer()
        old = {
            'id': obj.id,
            'name': obj.name,
            'born': obj.born,
            'death': obj.death,
            'wikipedia': obj.wikipedia,
            'profil': obj.profil
        }
        data = {
            'name': 'test-updated',
            'born': self.date2,
            'death': self.date,
            'wikipedia': self.link2,
        }
        serializer = PeopleSerializer(instance=obj, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.id, old['id'])
        self.assertNotEqual(obj.name, old['name'])
        self.assertEqual(obj.name, data['name'])
        self.assertNotEqual(obj.born, old['born'])
        self.assertEqual(obj.born, data['born'])
        self.assertNotEqual(obj.death, old['death'])
        self.assertEqual(obj.death, data['death'])
        self.assertNotEqual(obj.wikipedia, old['wikipedia'])
        self.assertEqual(obj.wikipedia, data['wikipedia'])
        self.check_commit(obj)

    @tag('serializer')
    def test_create_serializer_empty(self):
        data = {}

        serializer = PeopleSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_wrong_url(self):
        data = {
            'name': 'test',
            'born': self.date,
            'death': self.date2,
            'wikipedia': self.link_wrong,
            'profil': self.picture
        }

        serializer = PeopleSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_create_same_name(self):
        self.test_create_serializer()
        data = {
            'name': 'test'
        }

        serializer = PeopleSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())