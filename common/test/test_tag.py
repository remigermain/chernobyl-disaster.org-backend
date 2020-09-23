from django.test import tag
from lib.test import BaseTest
from common.serializers.tag import TagSerializer
from common.models import TagLang
from django.urls import reverse


@tag('tag')
class TagTest(BaseTest):

    @tag('auth')
    def test_auth(self):
        instance = self.test_create_serializer()
        response = self.client.get(reverse("tag-list"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("tag-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("tag-list"))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse("tag-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 403)

    @tag('serializer', 'create')
    def test_create_serializer(self):
        data = {
            'name': "name name",
        }
        serializer = TagSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_created(instance)
        return instance

    @tag('serializer', 'create')
    def test_create_serializer_lang(self):
        data = {
            'name': "name name",
            'langs': [
                {
                    'name': 'lala',
                    'language': self.lang
                }
            ]
        }
        serializer = TagSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_created(instance)
        self.check_commit_created(TagLang.objects.first())
        return instance

    @tag('serializer', 'create')
    def test_create_serializer_lang2(self):
        data = {
            'name': "name name",
            'langs': [
                {
                    'name': 'lala',
                    'language': self.lang
                },
                {
                    'name': 'lala',
                    'language': self.lang2
                }
            ]
        }
        serializer = TagSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_created(instance)
        self.assertEqual(TagLang.objects.count(), 2)
        return instance

    @tag('serializer', 'update')
    def test_update_serializer_lang2(self):
        instance = self.test_create_serializer_lang2()
        data = {
            'name': "name name name",
        }
        serializer = TagSerializer(instance=instance, data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_update(instance, ["name"])
        return instance

    @tag('serializer', 'update')
    def test_update_serializer_change_lang(self):
        instance = self.test_create_serializer_lang2()
        obj1 = instance.langs.first()
        obj2 = instance.langs.last()
        data = {
            'name': instance.name,
            'langs': [
                {
                    'id': obj2.id,
                    'name': 'lalal',
                    'language': obj1.language,
                },
                {
                    'id': obj1.id,
                    'name': 'lalal',
                    'language': obj2.language,
                },
            ],
        }
        serializer = TagSerializer(instance=instance, data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_update(instance, ["langs"])
        return instance

    ###############################
    #      error
    ###############################

    @tag('serializer', 'update')
    def test_update_serializer_empty_name(self):
        instance = self.test_create_serializer_lang2()
        data = {
            'name': "",
        }
        serializer = TagSerializer(instance=instance, data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer', 'update')
    def test_update_serializer_wrong_lang2(self):
        instance = self.test_create_serializer_lang2()
        data = {
            'name': "",
            'langs': [
                {
                    'name': 'lala',
                    'language': self.lang
                },
                {
                    'name': 'lala',
                    'language': self.lang2
                }
            ]
        }
        serializer = TagSerializer(instance=instance, data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer', 'create')
    def test_create_serializer_wrong_lang(self):
        data = {
            'name': "name name",
            'langs': [
                {
                    'name': 'lala',
                    'language': "wrong"
                },
            ]
        }
        serializer = TagSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer', 'create')
    def test_create_serializer_wrong_name(self):
        data = {
            'name': "",
            'langs': [
                {
                    'name': 'lala',
                    'language': self.lang
                },
            ]
        }
        serializer = TagSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer', 'create')
    def test_create_serializer_wrong_lang_name(self):
        data = {
            'name': "name",
            'langs': [
                {
                    'name': '',
                    'language': self.lang
                },
            ]
        }
        serializer = TagSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer', 'create')
    def test_client_serializer_wrong_lang_name(self):
        data = {
            'name': "name",
            'langs': [
                {
                    'name': '',
                    'language': self.lang
                },
            ]
        }
        response = self.factory.post(reverse("tag-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('serializer', 'create')
    def test_client_serializer_wrong_name(self):
        data = {
            'name': "",
            'langs': [
                {
                    'name': 'name',
                    'language': self.lang
                },
            ]
        }
        response = self.factory.post(reverse("tag-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('serializer', 'create')
    def test_client_serializer_wrong_lang(self):
        data = {
            'name': "",
            'langs': [
                {
                    'name': 'name',
                    'language': "wrong"
                },
            ]
        }
        response = self.factory.post(reverse("tag-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('serializer', 'create')
    def test_client_serializer_wrong_same_lang(self):
        data = {
            'name': "name",
            'langs': [
                {
                    'name': 'name',
                    'language': self.lang
                },
                {
                    'name': 'name',
                    'language': self.lang
                },
            ]
        }
        response = self.factory.post(reverse("tag-list"), data=data)
        self.assertEqual(response.status_code, 400)
