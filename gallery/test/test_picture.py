from django.test import tag
from lib.test import BaseTest
from gallery.serializers.picture import PictureSerializerPost
from gallery.models import PictureLang, Picture
from django.urls import reverse
from django.utils import timezone
from timeline.models import Event
from django.core.files.uploadedfile import SimpleUploadedFile


@tag('picture')
class VideoTest(BaseTest):

    def setUp(self):
        super().setUp()
        self.picture = SimpleUploadedFile(
            'small.png',
            (
                b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
                b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
                b'\x02\x4c\x01\x00\x3b'
            ),
            content_type='image/png'
        )
        self.event = Event.objects.create(title="title", date=timezone.now())

    def test_auth(self):
        instance = self.test_create_serializer()

        response = self.client.get(reverse("picture-list"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("picture-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        instance = self.test_create_serializer()
        response = self.client.delete(reverse("picture-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 403)
        response = self.factory.delete(reverse("picture-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 403)
        response = self.factory_admin.delete(reverse("picture-detail", args=["wrong"]))
        self.assertEqual(response.status_code, 404)
        response = self.factory_admin.delete(reverse("picture-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 204)

    def test_create_serializer(self):
        data = {
            'title': 'title',
            'picture': self.picture
        }
        serializer = PictureSerializerPost(data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_created(instance)
        return instance

    def test_create_serializer_langs(self):
        data = {
            'title': 'title',
            'picture': self.picture,
            'langs': [{
                'title': 'lala',
                'language': self.lang,
            }]
        }
        serializer = PictureSerializerPost(data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_created(instance)
        self.assertEqual(instance.langs.count(), 1)
        return instance

    def test_create_serializer_langs2(self):
        data = {
            'title': 'title',
            'picture': self.picture,
            'langs': [
                {
                    'title': 'lala',
                    'language': self.lang,
                },
                {
                    'title': 'lala',
                    'language': self.lang2,
                }
            ]
        }
        serializer = PictureSerializerPost(data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_created(instance)
        self.assertEqual(instance.langs.count(), 2)
        return instance

    def test_create_client(self):
        data = {
            'title': 'title',
            'picture': self.picture
        }
        response = self.client.post(reverse('picture-list'), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.post(reverse('picture-list'), data=data, format='multipart')
        print(response.content)
        self.assertEqual(response.status_code, 201)

    def test_create_client_langs(self):
        data = {
            'title': 'title',
            'picture': self.picture,
            'langs[0][title]': 'lala',
            'langs[0][language]': self.lang,
        }
        response = self.client.post(reverse('picture-list'), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.post(reverse('picture-list'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PictureLang.objects.count(), 1)

    def test_create_client_langs2(self):
        data = {
            'title': 'title',
            'picture': self.picture,
            'langs[0][title]': 'lala',
            'langs[0][language]': self.lang,
            'langs[1][title]': 'lala',
            'langs[1][language]': self.lang2,
        }
        response = self.client.post(reverse('picture-list'), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.post(reverse('picture-list'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PictureLang.objects.count(), 2)
    
    # def test_create_serializer(self):
    #     instance = self.test_create_serializer()
    #     data = {
    #         'title': 'title title',
    #     }
    #     serializer = PictureSerializerPost(instance=instance, data=data, context=self.context, partial=True)
    #     print(serializer.is_valid(), serializer.errors)
    #     self.assertTrue(serializer.is_valid())
    #     instance = serializer.save()
    #     self.check_commit_update(instance, diff=['title'])

    def test_update_client(self):
        instance = self.test_create_serializer()
        data = {
            'title': 'title title',
        }
        response = self.client.patch(reverse('picture-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.patch(reverse('picture-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 200)

    def test_update_client_langs(self):
        instance = self.test_create_serializer()
        data = {
            'title': 'title title',
            'langs[0][title]': 'lala',
            'langs[0][language]': self.lang,
            'langs[1][title]': 'lala',
            'langs[1][language]': self.lang2,
        }
        response = self.client.patch(reverse('picture-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.patch(reverse('picture-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Picture.objects.count(), 1)
        self.assertEqual(PictureLang.objects.count(), 2)

    def test_update_client_langs_change(self):
        instance = self.test_create_serializer_langs2()
        langs = instance.langs.all()
        data = {
            'title': 'title title',
            'langs[0][id]': langs[0].id,
            'langs[0][title]': 'lala',
            'langs[0][language]': langs[1].language,
            'langs[1][id]': langs[1].id,
            'langs[1][title]': 'lala',
            'langs[1][language]': langs[0].language,
        }
        response = self.client.patch(reverse('picture-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.patch(reverse('picture-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Picture.objects.count(), 1)
        self.assertEqual(PictureLang.objects.count(), 2)

    def test_create_client_no_title(self):
        data = {
            'picture': self.picture
        }
        response = self.factory.post(reverse('picture-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_empty_title(self):
        data = {
            'title': '',
            'picture': self.picture
        }
        response = self.factory.post(reverse('picture-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_no_video(self):
        data = {
            'title': 'title',
        }
        response = self.factory.post(reverse('picture-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_empty_video(self):
        data = {
            'title': 'title',
            'picture': ''
        }
        response = self.factory.post(reverse('picture-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_wrong_video(self):
        data = {
            'title': 'title',
            'picture': 'worng_url'
        }
        response = self.factory.post(reverse('picture-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_same_langs(self):
        data = {
            'title': 'title',
            'picture': self.picture,
            'langs[0][title]': 'lala',
            'langs[0][language]': self.lang,
            'langs[1][title]': 'lala',
            'langs[1][language]': self.lang,
        }
        response = self.factory.post(reverse('picture-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_wrong_lang(self):
        data = {
            'title': 'title',
            'picture': self.picture,
            'langs[0][title]': 'lala',
            'langs[0][language]': "self.lang",
        }
        response = self.factory.post(reverse('picture-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_no_langs(self):
        data = {
            'title': 'title',
            'picture': self.picture,
            'langs[0][title]': 'lala',
        }
        response = self.factory.post(reverse('picture-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_langs_no_title(self):
        data = {
            'title': 'title',
            'picture': self.picture,
            'langs[0][language]': self.lang,
        }
        response = self.factory.post(reverse('picture-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_langs_empty_title(self):
        data = {
            'title': 'title',
            'picture': self.picture,
            'langs[0][title]': '',
            'langs[0][language]': self.lang,
        }
        response = self.factory.post(reverse('picture-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_update_serializer(self):
        instance = self.test_create_serializer()
        data = {
            'title': 'title title',
        }
        serializer = PictureSerializerPost(instance=instance, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.check_commit_update(obj, diff=['title'])

    def test_update_serializer_langs(self):
        instance = self.test_create_serializer()
        data = {
            'title': 'title title',
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
        serializer = PictureSerializerPost(instance=instance, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.check_commit_update(obj, diff=['title', 'langs'])
        self.assertEqual(obj.langs.count(), 2)

    def test_create_serializer_no_title(self):
        data = {
            'picture': self.picture
        }
        serializer = PictureSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_empty_title(self):
        data = {
            'title': '',
            'picture': self.picture
        }
        serializer = PictureSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_no_video(self):
        data = {
            'title': 'title',
        }
        serializer = PictureSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_empty_video(self):
        data = {
            'title': 'title',
            'picture': ''
        }
        serializer = PictureSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_wrong_video(self):
        data = {
            'title': 'title',
            'picture': 'worng_url'
        }
        serializer = PictureSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_same_langs(self):
        data = {
            'title': 'title',
            'picture': self.picture,
            'langs': [
                {
                    'title': 'title',
                    'language': self.lang
                },
                {
                    'title': 'title2',
                    'language': self.lang
                }
            ]
        }
        serializer = PictureSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_wrong_lang(self):
        data = {
            'title': 'title',
            'picture': self.picture,
            'langs': [
                {
                    'title': 'lalala',
                    'language': "wrong"
                }
            ]
        }
        serializer = PictureSerializerPost(data=data, context=self.context,)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_no_langs(self):
        data = {
            'title': 'title',
            'picture': self.picture,
            'langs': [
                {
                    'title': 'lalala',
                }
            ]
        }
        serializer = PictureSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_langs_no_title(self):
        data = {
            'title': 'title',
            'picture': self.picture,
            'langs': [
                {
                    'language': self.lang
                }
            ]
        }
        serializer = PictureSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_langs_empty_title(self):
        data = {
            'title': 'title',
            'picture': self.picture,
            'langs': [
                {
                    'title': '',
                    'language': self.lang
                }
            ]
        }
        serializer = PictureSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
