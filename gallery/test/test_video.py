from django.test import tag
from lib.test import BaseTest
from gallery.serializers.video import VideoSerializerPost
from gallery.models import VideoLang, Video
from django.urls import reverse
from django.utils import timezone
from timeline.models import Event


@tag('video')
class VideoTest(BaseTest):

    def setUp(self):
        super().setUp()
        self.event = Event.objects.create(title="title", date=timezone.now())

    def test_auth(self):
        instance = self.test_create_serializer()

        response = self.client.get(reverse("video-list"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("video-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        instance = self.test_create_serializer()
        response = self.client.delete(reverse("video-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 403)
        response = self.factory.delete(reverse("video-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 403)
        response = self.factory_admin.delete(reverse("video-detail", args=["wrong"]))
        self.assertEqual(response.status_code, 404)
        response = self.factory_admin.delete(reverse("video-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 204)

    def test_create_serializer(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe'
        }
        serializer = VideoSerializerPost(data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_created(instance)
        return instance

    def test_create_serializer_event(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
            'event': self.event.id
        }
        serializer = VideoSerializerPost(data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_created(instance)
        return instance

    def test_create_serializer_langs(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
            'langs': [{
                'title': 'lala',
                'language': self.lang,
            }]
        }
        serializer = VideoSerializerPost(data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_created(instance)
        self.assertEqual(instance.langs.count(), 1)
        return instance

    def test_create_serializer_langs2(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
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
        serializer = VideoSerializerPost(data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_created(instance)
        self.assertEqual(instance.langs.count(), 2)
        return instance

    def test_create_client(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe'
        }
        response = self.client.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 201)

    def test_create_client_event(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
            'event': self.event.id
        }
        response = self.client.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 201)

    def test_create_client_langs(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
            'langs[0][title]': 'lala',
            'langs[0][language]': self.lang,
        }
        response = self.client.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(VideoLang.objects.count(), 1)

    def test_create_client_langs2(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
            'langs[0][title]': 'lala',
            'langs[0][language]': self.lang,
            'langs[1][title]': 'lala',
            'langs[1][language]': self.lang2,
        }
        response = self.client.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(VideoLang.objects.count(), 2)
    
    def test_update_serializer(self):
        instance = self.test_create_serializer()
        data = {
            'title': 'title title',
        }
        serializer = VideoSerializerPost(instance=instance, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_update(instance, diff=['title'])

    def test_update_client(self):
        instance = self.test_create_serializer()
        data = {
            'title': 'title title',
        }
        response = self.client.patch(reverse('video-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.patch(reverse('video-detail', args=[instance.id]), data=data)
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
        response = self.client.patch(reverse('video-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.patch(reverse('video-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Video.objects.count(), 1)
        self.assertEqual(VideoLang.objects.count(), 2)

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
        response = self.client.patch(reverse('video-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.patch(reverse('video-detail', args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Video.objects.count(), 1)
        self.assertEqual(VideoLang.objects.count(), 2)

    def test_create_client_no_title(self):
        data = {
            'video': 'https://peertube.com/emmferpfe'
        }
        response = self.factory.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_empty_title(self):
        data = {
            'title': '',
            'video': 'https://peertube.com/emmferpfe'
        }
        response = self.factory.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_no_video(self):
        data = {
            'title': 'title',
        }
        response = self.factory.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_empty_video(self):
        data = {
            'title': 'title',
            'video': ''
        }
        response = self.factory.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_wrong_video(self):
        data = {
            'title': 'title',
            'video': 'worng_url'
        }
        response = self.factory.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_same_langs(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
            'langs[0][title]': 'lala',
            'langs[0][language]': self.lang,
            'langs[1][title]': 'lala',
            'langs[1][language]': self.lang,
        }
        response = self.factory.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_wrong_lang(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
            'langs[0][title]': 'lala',
            'langs[0][language]': "self.lang",
        }
        response = self.factory.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_no_langs(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
            'langs[0][title]': 'lala',
        }
        response = self.factory.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_langs_no_title(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
            'langs[0][language]': self.lang,
        }
        response = self.factory.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_client_langs_empty_title(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
            'langs[0][title]': '',
            'langs[0][language]': self.lang,
        }
        response = self.factory.post(reverse('video-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_serializer_wrong_event(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
            'event': self.event.id + 2
        }
        serializer = VideoSerializerPost(data=data, context=self.context, partial=True)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_empty_event(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
            'event': ""
        }
        serializer = VideoSerializerPost(data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertIsNone(instance.event)

    def test_update_serializer(self):
        instance = self.test_create_serializer()
        data = {
            'title': 'title title',
        }
        serializer = VideoSerializerPost(instance=instance, data=data, context=self.context, partial=True)
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
        serializer = VideoSerializerPost(instance=instance, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.check_commit_update(obj, diff=['title', 'langs'])
        self.assertEqual(obj.langs.count(), 2)

    def test_create_serializer_no_title(self):
        data = {
            'video': 'https://peertube.com/emmferpfe'
        }
        serializer = VideoSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_empty_title(self):
        data = {
            'title': '',
            'video': 'https://peertube.com/emmferpfe'
        }
        serializer = VideoSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_no_video(self):
        data = {
            'title': 'title',
        }
        serializer = VideoSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_empty_video(self):
        data = {
            'title': 'title',
            'video': ''
        }
        serializer = VideoSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_wrong_video(self):
        data = {
            'title': 'title',
            'video': 'worng_url'
        }
        serializer = VideoSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_same_langs(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
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
        serializer = VideoSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_wrong_lang(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
            'langs': [
                {
                    'title': 'lalala',
                    'language': "wrong"
                }
            ]
        }
        serializer = VideoSerializerPost(data=data, context=self.context,)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_no_langs(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
            'langs': [
                {
                    'title': 'lalala',
                }
            ]
        }
        serializer = VideoSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_langs_no_title(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
            'langs': [
                {
                    'language': self.lang
                }
            ]
        }
        serializer = VideoSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_langs_empty_title(self):
        data = {
            'title': 'title',
            'video': 'https://peertube.com/emmferpfe',
            'langs': [
                {
                    'title': '',
                    'language': self.lang
                }
            ]
        }
        serializer = VideoSerializerPost(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_delete_commit(self):
        from utils.function import contenttypes_uuid
        from utils.models import Commit

        instance = self.test_create_serializer()

        uuid = contenttypes_uuid(instance)
        self.assertNotEqual(Commit.objects.filter(uuid=uuid).count(), 0)
        response = self.factory_admin.delete(reverse("video-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Commit.objects.filter(uuid=uuid).count(), 0)

    def test_delete_commit_parent(self):
        from utils.function import contenttypes_uuid
        from utils.models import Commit

        instance = self.test_create_serializer_langs2()
        langs = instance.langs.all()

        # delete child
        uuid = contenttypes_uuid(langs[0])
        self.assertNotEqual(Commit.objects.filter(uuid=uuid).count(), 0)
        langs[0].delete()
        self.assertEqual(Commit.objects.filter(uuid=uuid).count(), 0)

        uuid = contenttypes_uuid(langs[0])
        self.assertNotEqual(Commit.objects.filter(uuid=uuid).count(), 0)
        langs.delete()
        self.assertEqual(Commit.objects.filter(uuid=uuid).count(), 0)