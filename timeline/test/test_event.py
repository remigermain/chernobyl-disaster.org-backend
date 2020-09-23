from django.test import tag
from lib.test import BaseTest
from timeline.serializers.event import EventSerializer
from django.urls import reverse


@tag('event')
class EventTest(BaseTest):

    @tag('auth')
    def test_auth(self):
        instance = self.test_create_serializer()
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('event-detail', args=[instance.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('event-list'))
        self.assertEqual(response.status_code, 403)
        response = self.client.patch(reverse('event-detail', args=[instance.id]))
        self.assertEqual(response.status_code, 403)

    @tag('serializer')
    def test_create_serializer(self):
        data = {
            'title': 'test-title',
            'date': str(self.time)
        }
        serializer = EventSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.check_commit_created(obj)
        return obj

    @tag('serializer')
    def test_create_serializer_langs(self):
        data = {
            'title': 'test-title',
            'date': str(self.time),
            'langs': [
                {
                    'title': 'title',
                    'description': 'desription',
                    'language': self.lang
                }
            ]
        }
        serializer = EventSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.check_commit_created(obj)
        return obj

    @tag('serializer')
    def test_create_serializer_langs2(self):
        data = {
            'title': 'test-title',
            'date': str(self.time),
            'langs': [
                {
                    'title': 'title',
                    'description': 'desription',
                    'language': self.lang
                },
                {
                    'title': 'title',
                    'description': 'desription',
                    'language': self.lang2
                }
            ]
        }
        serializer = EventSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.check_commit_created(obj)
        return obj

    @tag('serializer')
    def test_create_serializer_wrong_langs2(self):
        data = {
            'title': 'test-title',
            'date': str(self.time),
            'langs': [
                {
                    'title': 'title',
                    'description': 'desription',
                    'language': self.lang2
                },
                {
                    'title': 'title',
                    'description': 'desription',
                    'language': self.lang2
                }
            ]
        }
        serializer = EventSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_wrong_langs_empty_description(self):
        data = {
            'title': 'test-title',
            'date': str(self.time),
            'langs': [
                {
                    'title': 'title',
                    'language': self.lang
                },
                {
                    'title': 'title',
                    'language': self.lang2
                }
            ]
        }
        serializer = EventSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_update_serializer(self):
        instance = self.test_create_serializer()
        data = {
            'id': instance.id,
            'title': 'test-title22',
            'date': str(self.time)
        }
        serializer = EventSerializer(instance=instance, data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.check_commit_update(obj, diff=['title'])

    @tag('serializer')
    def test_create_serializer_empty_title(self):
        data = {
            'title': '',
            'date': str(self.time)
        }
        serializer = EventSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_no_title(self):
        data = {
            'date': str(self.time)
        }
        serializer = EventSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_no_time(self):
        data = {
            'title': 'title',
        }
        serializer = EventSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_wrong_time(self):
        data = {
            'title': 'title',
            'date': str(self.time) + 'aa'
        }
        serializer = EventSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_empty_time(self):
        data = {
            'title': 'title',
            'date': ''
        }
        serializer = EventSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('client')
    def test_create_client(self):
        data = {
            'title': 'test-title',
            'date': str(self.time)
        }
        response = self.factory.post(reverse("event-list"), data=data)
        self.assertEqual(response.status_code, 201)

    @tag('client')
    def test_create_client_no_title(self):
        data = {
            'date': str(self.time)
        }
        response = self.factory.post(reverse("event-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client')
    def test_create_client_empty_title(self):
        data = {
            'title': '',
            'date': str(self.time)
        }
        response = self.factory.post(reverse("event-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client')
    def test_create_client_no_time(self):
        data = {
            'title': 'title',
        }
        response = self.factory.post(reverse("event-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client')
    def test_create_client_empty_time(self):
        data = {
            'title': 'title',
            'date': ''
        }
        response = self.factory.post(reverse("event-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client')
    def test_create_client_wrong_date(self):
        data = {
            'title': 'title',
            'date': 'wrongdate'
        }
        response = self.factory.post(reverse("event-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client')
    def test_update_client(self):
        instance = self.test_create_serializer()
        data = {
            'title': 'title',
            'date': self.time
        }
        response = self.factory.patch(reverse("event-detail", args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 200)

    @tag('client')
    def test_update_client_empty_title(self):
        instance = self.test_create_serializer()
        data = {
            'title': '',
            'date': self.time
        }
        response = self.factory.patch(reverse("event-detail", args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client')
    def test_update_client_langs(self):
        instance = self.test_create_serializer()
        data = {
            'title': 'title',
            'date': self.time,
            'langs[0][title]': 'title',
            'langs[0][description]': 'description',
            'langs[0][language]': self.lang,
        }
        response = self.factory.patch(reverse("event-detail", args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 200)

    @tag('client')
    def test_update_client_langs2(self):
        instance = self.test_create_serializer()
        data = {
            'title': 'title',
            'date': self.time,
            'langs[0][title]': 'title',
            'langs[0][description]': 'description',
            'langs[0][language]': self.lang,
            'langs[1][title]': 'title',
            'langs[1][description]': 'description',
            'langs[1][language]': self.lang2,
        }
        response = self.factory.patch(reverse("event-detail", args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 200)

    @tag('client')
    def test_update_client_same_langs(self):
        instance = self.test_create_serializer()
        data = {
            'title': 'title',
            'date': self.time,
            'langs[0][title]': 'title',
            'langs[0][description]': 'description',
            'langs[0][language]': self.lang,
            'langs[1][title]': 'title',
            'langs[1][description]': 'description',
            'langs[1][language]': self.lang,
        }
        response = self.factory.patch(reverse("event-detail", args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client')
    def test_update_client_langs_empty_title(self):
        instance = self.test_create_serializer()
        data = {
            'title': '',
            'date': self.time,
            'langs[0][title]': 'title',
            'langs[0][description]': 'description',
            'langs[0][language]': self.lang,
        }
        response = self.factory.patch(reverse("event-detail", args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client')
    def test_update_client_langs_change_lang(self):
        instance = self.test_create_serializer_langs2()
        data = EventSerializer(instance=instance).data
        data = {
            'title': 'title',
            'date': self.time,
            'langs[0][id]': data['langs'][0]['id'],
            'langs[0][title]': 'title',
            'langs[0][description]': 'description',
            'langs[0][language]': data['langs'][1]['language'],
            'langs[1][id]': data['langs'][1]['id'],
            'langs[1][title]': 'title',
            'langs[1][description]': 'description',
            'langs[1][language]': data['langs'][0]['language']
        }
        response = self.factory.patch(reverse("event-detail", args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 200)

    @tag('client')
    def test_update_client_langs_create_same_lang(self):
        instance = self.test_create_serializer_langs2()
        data = EventSerializer(instance=instance).data
        data = {
            'title': 'title',
            'date': self.time,
            'langs[0][id]': data['langs'][0]['id'],
            'langs[0][title]': 'title',
            'langs[0][description]': 'description',
            'langs[0][language]': data['langs'][0]['language'],
            'langs[1][id]': data['langs'][1]['id'],
            'langs[1][title]': 'title',
            'langs[1][description]': 'description',
            'langs[1][language]': data['langs'][1]['language'],
            'langs[2][title]': 'title',
            'langs[2][description]': 'description',
            'langs[2][language]': data['langs'][1]['language']

        }
        response = self.factory.patch(reverse("event-detail", args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client')
    def test_update_client_create_lang(self):
        data = {
            'title': 'title',
            'date': self.time,
            'langs[0][title]': 'title',
            'langs[0][description]': 'description',
            'langs[0][language]': self.lang,
            'langs[1][title]': 'title',
            'langs[1][description]': 'description',
            'langs[1][language]': self.lang2,

        }
        response = self.factory.post(reverse("event-list"), data=data)
        self.assertEqual(response.status_code, 201)
