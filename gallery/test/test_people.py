from django.test import tag
from lib.test import BaseTest
from gallery.serializers.people import PeopleSerializerPost
from gallery.models import PeopleLang, People
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


@tag('people')
class PeopleTest(BaseTest):

    def setUp(self):
        super().setUp()
        image = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.picture = SimpleUploadedFile("image.gif", image, content_type="image/gif")

    def test_auth(self):
        instance = self.test_create_serializer()

        response = self.client.get(reverse("people-list"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("people-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        instance = self.test_create_serializer()
        response = self.client.delete(reverse("people-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 403)
        response = self.factory.delete(reverse("people-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 403)
        response = self.factory_admin.delete(reverse("people-detail", args=["wrong"]))
        self.assertEqual(response.status_code, 404)
        response = self.factory_admin.delete(reverse("people-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 204)

    def test_create_serializer(self):
        data = {
            'name': 'name',
            'profil': self.picture,
            'death': self.date,
            'born': self.date
        }
        serializer = PeopleSerializerPost(data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_created(instance)
        self.assertIsNotNone(instance.profil)
        return instance

    def test_create_serializer_langs(self):
        data = {
            'name': 'name',
            'langs': [{
                'biography': 'lala',
                'language': self.lang,
            }]
        }
        serializer = PeopleSerializerPost(data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_created(instance)
        self.assertEqual(instance.langs.count(), 1)
        return instance

    def test_create_serializer_langs2(self):
        data = {
            'name': 'name',
            'langs': [
                {
                    'biography': 'lala',
                    'language': self.lang,
                },
                {
                    'biography': 'lala',
                    'language': self.lang2,
                }
            ]
        }
        serializer = PeopleSerializerPost(data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_created(instance)
        self.assertEqual(instance.langs.count(), 2)
        return instance

    def test_create_client(self):
        data = {
            'name': 'name',
        }
        response = self.client.post(reverse('people-list'), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.post(reverse('people-list'), data=data)
        self.assertEqual(response.status_code, 201)

    def test_create_client_profil(self):
        data = {
            'name': 'name',
            'profil': self.picture
        }
        response = self.client.post(reverse('people-list'), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.post(reverse('people-list'), data=data)
        self.assertEqual(response.status_code, 201)

    def test_create_client_langs(self):
        data = {
            'name': 'name',
            'langs[0][biography]': 'lala',
            'langs[0][language]': self.lang,
        }
        response = self.client.post(reverse('people-list'), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.post(reverse('people-list'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PeopleLang.objects.count(), 1)

    def test_create_client_langs2(self):
        data = {
            'name': 'name',
            'langs[0][biography]': 'lala',
            'langs[0][language]': self.lang,
            'langs[1][biography]': 'lala',
            'langs[1][language]': self.lang2,
        }
        response = self.client.post(reverse('people-list'), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.post(reverse('people-list'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PeopleLang.objects.count(), 2)

    def test_update_client(self):
        instance = self.test_create_serializer()
        data = {
            'name': 'title title',
        }
        response = self.client.patch(reverse('people-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.patch(reverse('people-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 200)

    def test_update_client_langs(self):
        instance = self.test_create_serializer()
        data = {
            'name': 'title title',
            'langs[0][biography]': 'lala',
            'langs[0][language]': self.lang,
            'langs[1][biography]': 'lala',
            'langs[1][language]': self.lang2,
        }
        response = self.client.patch(reverse('people-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.patch(reverse('people-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(People.objects.count(), 1)
        self.assertEqual(PeopleLang.objects.count(), 2)

    def test_update_client_langs_change(self):
        instance = self.test_create_serializer_langs2()
        langs = instance.langs.all()
        data = {
            'name': 'title title',
            'langs[0][id]': langs[0].id,
            'langs[0][biography]': 'lala',
            'langs[0][language]': langs[1].language,
            'langs[1][id]': langs[1].id,
            'langs[1][biography]': 'lala',
            'langs[1][language]': langs[0].language,
        }
        response = self.client.patch(reverse('people-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.patch(reverse('people-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(People.objects.count(), 1)
        self.assertEqual(PeopleLang.objects.count(), 2)

    def test_create_client_no_biography(self):
        data = {
        }
        response = self.factory.post(reverse('people-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_empty_biography(self):
        data = {
            'name': '',
        }
        response = self.factory.post(reverse('people-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_same_langs(self):
        data = {
            'name': 'name',
            'langs[0][biography]': 'lala',
            'langs[0][language]': self.lang,
            'langs[1][biography]': 'lala',
            'langs[1][language]': self.lang,
        }
        response = self.factory.post(reverse('people-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_wrong_lang(self):
        data = {
            'name': 'name',
            'langs[0][biography]': 'lala',
            'langs[0][language]': "self.lang",
        }
        response = self.factory.post(reverse('people-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_no_langs(self):
        data = {
            'name': 'name',
            'langs[0][biography]': 'lala',
        }
        response = self.factory.post(reverse('people-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_langs_no_biography(self):
        data = {
            'name': 'name',
            'langs[0][language]': self.lang,
        }
        response = self.factory.post(reverse('people-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_langs_empty_biography(self):
        data = {
            'name': 'name',
            'langs[0][biography]': '',
            'langs[0][language]': self.lang,
        }
        response = self.factory.post(reverse('people-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_update_serializer(self):
        instance = self.test_create_serializer()
        data = {
            'name': 'title title',
        }
        serializer = PeopleSerializerPost(instance=instance, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.check_commit_update(obj, diff=['name', 'tags'])

    def test_update_serializer_langs(self):
        instance = self.test_create_serializer()
        data = {
            'langs': [
                {
                    'biography': 'name',
                    'language': self.lang
                },
                {
                    'biography': 'name',
                    'language': self.lang2
                }
            ]
        }
        serializer = PeopleSerializerPost(instance=instance, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.check_commit_update(obj, diff=['tags', 'langs'])
        self.assertEqual(obj.langs.count(), 2)

    def test_create_serializer_same_langs(self):
        data = {
            'name': 'name',
            'langs': [
                {
                    'biography': 'name',
                    'language': self.lang
                },
                {
                    'biography': 'title2',
                    'language': self.lang
                }
            ]
        }
        serializer = PeopleSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_wrong_lang(self):
        data = {
            'name': 'name',
            'langs': [
                {
                    'biography': 'lalala',
                    'language': "wrong"
                }
            ]
        }
        serializer = PeopleSerializerPost(data=data, context=self.context,)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_no_langs(self):
        data = {
            'name': 'name',
            'langs': [
                {
                    'biography': 'lalala',
                }
            ]
        }
        serializer = PeopleSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_langs_no_biography(self):
        data = {
            'name': 'name',
            'langs': [
                {
                    'language': self.lang
                }
            ]
        }
        serializer = PeopleSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_langs_empty_biography(self):
        data = {
            'name': 'name',
            'langs': [
                {
                    'biography': '',
                    'language': self.lang
                }
            ]
        }
        serializer = PeopleSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_wrong_death(self):
        data = {
            'name': 'name',
            'death': 'ffefer'
        }
        serializer = PeopleSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_wrong_born(self):
        data = {
            'name': 'name',
            'born': 'ffefer'
        }
        serializer = PeopleSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_empty_death(self):
        data = {
            'name': 'name',
            'death': ''
        }
        serializer = PeopleSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_empty_born(self):
        data = {
            'name': 'name',
            'born': ''
        }
        serializer = PeopleSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_empty_wiki(self):
        data = {
            'name': 'name',
            'wikipedia': ''
        }
        serializer = PeopleSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_wrong_wiki(self):
        data = {
            'name': 'name',
            'wikipedia': 'wrong_link'
        }
        serializer = PeopleSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
