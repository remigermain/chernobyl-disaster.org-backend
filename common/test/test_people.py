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

# langs

    @tag('serializer', 'langs')
    def test_create_serializer_langs(self):
        data = {
            'name': 'test',
            'born': self.date,
            'death': self.date2,
            'wikipedia': self.link,
            'profil': self.picture,
            'langs': [
                {
                    'biography': 'lallaalla',
                    'language': self.lang
                }
            ]
        }
        serializer = PeopleSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.langs.count(), 1)
        self.assertEqual(obj.langs.first().biography, data['langs'][0]['biography'])
        self.assertEqual(obj.langs.first().language, data['langs'][0]['language'])
        return obj

    @tag('serializer', 'langs')
    def test_create_serializer_langs2(self):
        data = {
            'name': 'test',
            'born': self.date,
            'death': self.date2,
            'wikipedia': self.link,
            'profil': self.picture,
            'langs': [
                {
                    'biography': 'lallaalla',
                    'language': self.lang
                },
                {
                    'biography': 'lallaalla egergergrte',
                    'language': self.lang2
                }
            ]
        }
        serializer = PeopleSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.langs.count(), 2)
        self.assertEqual(obj.langs.first().biography, data['langs'][0]['biography'])
        self.assertEqual(obj.langs.first().language, data['langs'][0]['language'])
        self.assertEqual(obj.langs.last().biography, data['langs'][1]['biography'])
        self.assertEqual(obj.langs.last().language, data['langs'][1]['language'])

    @tag('serializer', 'langs')
    def test_create_serializer_same_langs(self):
        data = {
            'name': 'test',
            'born': self.date,
            'death': self.date2,
            'wikipedia': self.link,
            'profil': self.picture,
            'langs': [
                {
                    'biography': 'lallaalla',
                    'language': self.lang
                },
                {
                    'biography': 'lallaalla egergergrte',
                    'language': self.lang
                }
            ]
        }
        serializer = PeopleSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer', 'langs')
    def test_create_serializer_update_langs(self):
        obj = self.test_create_serializer_langs()

        data = {
            'langs': [
                {
                    'biography': 'lallaalla',
                    'language': self.lang2
                }
            ]
        }

        serializer = PeopleSerializer(instance=obj, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())

    @tag('serializer', 'langs')
    def test_create_serializer_update_same_langs(self):
        obj = self.test_create_serializer_langs()

        data = {
            'langs': [
                {
                    'id': obj.langs.first().id,
                    'biography': 'lallaalla',
                    'language': self.lang2
                },
                {
                    'biography': 'lallaalla',
                    'language': self.lang
                }
            ]
        }
        serializer = PeopleSerializer(instance=obj, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())

    @tag('serializer', 'langs')
    def test_create_serializer_update_same2_langs(self):
        obj = self.test_create_serializer_langs()

        data = {
            'langs': [
                {
                    'id': obj.langs.first().id,
                    'biography': 'lallaalla',
                    'language': self.lang2
                },
                {
                    'biography': 'lallaalla',
                    'language': self.lang2
                }
            ]
        }

        serializer = PeopleSerializer(instance=obj, data=data, context=self.context, partial=True)
        self.assertFalse(serializer.is_valid())