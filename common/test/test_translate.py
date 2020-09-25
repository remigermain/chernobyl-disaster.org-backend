from django.test import tag
from lib.test import BaseTest
from common.serializers.translate import TranslateLangSerializer
from common.models import Translate
from django.urls import reverse
import json


@tag('translate')
class TranslateTest(BaseTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.__translate = Translate.objects.create(key="test.key")

    @tag('auth')
    def test_auth(self):
        instance = self.test_create_serializer()
        response = self.client.get(reverse("translatelang-list"))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse("translatelang-list"))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse("translatelang-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse("translate-list"))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse("translate-list"))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse("translate-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 403)

        response = self.factory.get(reverse("translatelang-list"))
        self.assertEqual(response.status_code, 200)
        response = self.factory.get(reverse("translate-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        instance = self.test_create_serializer()
        response = self.client.put(reverse("translate-detail", args=[instance.id]), data={})
        self.assertEqual(response.status_code, 403)
        response = self.factory.put(reverse("translate-detail", args=[instance.id]), data={})
        self.assertEqual(response.status_code, 403)

    @tag('serializer', 'create')
    def test_create_serializer(self):
        data = {
            'parent_key': self.__translate.id,
            'value': "value value",
            'language': self.lang
        }
        serializer = TranslateLangSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_created(instance)
        self.assertEqual(self.__translate.langs.count(), 1)
        return instance

    @tag('serializer', 'create')
    def test_create_serializer_2(self):
        self.test_create_serializer()
        data = {
            'parent_key': self.__translate.id,
            'value': "value value",
            'language': self.lang2
        }
        serializer = TranslateLangSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_created(instance)
        self.assertEqual(self.__translate.langs.count(), 2)
        return instance

    @tag('serializer', 'create')
    def test_update_serializer(self):
        instance = self.test_create_serializer()
        data = {
            'parent_key': self.__translate.id,
            'value': "value value 2",
            'language': self.lang2
        }
        serializer = TranslateLangSerializer(instance=instance, data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_commit_update(instance, ['value', 'language'])

    @tag('client', 'create')
    def test_create_client(self):
        data = {
            'parent_key': self.__translate.id,
            'value': "value value",
            'language': self.lang
        }
        response = self.factory.post(reverse("translatelang-list"), data=data)
        self.assertEqual(response.status_code, 201)
        return json.loads(response.content)

    @tag('client', 'create')
    def test_update_client(self):
        create = self.test_create_client()
        data = {
            'parent_key': self.__translate.id,
            'value': "value value2",
            'language': self.lang2
        }
        response = self.factory.patch(reverse("translatelang-detail", args=[create['id']]), data=data)
        self.assertEqual(response.status_code, 200)

    ###############################
    #      error
    ###############################

    @tag('serializer', 'create')
    def test_create_serializer_no_parent(self):
        data = {
            'value': "value value",
            'language': self.lang
        }
        serializer = TranslateLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer', 'create')
    def test_create_serializer_unk_parent(self):
        data = {
            'parent_key': 666,
            'value': "value value",
            'language': self.lang
        }
        serializer = TranslateLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer', 'create')
    def test_create_serializer_no_value(self):
        data = {
            'parent_key': self.__translate.id,
            'language': self.lang
        }
        serializer = TranslateLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer', 'create')
    def test_create_serializer_no_language(self):
        data = {
            'parent_key': self.__translate.id,
        }
        serializer = TranslateLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer', 'create')
    def test_create_serializer_nuk_language(self):
        data = {
            'parent_key': self.__translate.id,
            'language': "worng lang"
        }
        serializer = TranslateLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer', 'create')
    def test_create_serializer_empty(self):
        data = {}
        serializer = TranslateLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer', 'create')
    def test_create_serializer_same_language(self):
        self.test_create_serializer()
        data = {
            'parent_key': self.__translate.id,
            'value': 'value value',
            'language': self.lang
        }
        serializer = TranslateLangSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer', 'update')
    def test_update_serializer_wrong_parent(self):
        instance = self.test_create_serializer()
        data = {
            'parent_key': 6666,
            'value': 'value value',
            'language': self.lang2
        }
        serializer = TranslateLangSerializer(instance=instance, data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer', 'update')
    def test_update_serializer_empty_value(self):
        instance = self.test_create_serializer()
        data = {
            'parent_key': 6666,
            'value': "",
            'language': self.lang2
        }
        serializer = TranslateLangSerializer(instance=instance, data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('client', 'update')
    def test_update_client_wrong_lang(self):
        instance = self.test_create_client()
        data = {
            'parent_key': self.__translate.id,
            'value': "value value",
            'language': "wrong lang"
        }
        response = self.factory.patch(reverse("translatelang-detail", args=[instance['id']]), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'update')
    def test_update_client_empty_value(self):
        instance = self.test_create_client()
        data = {
            'value': "",
        }
        response = self.factory.patch(reverse("translatelang-detail", args=[instance['id']]), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'update')
    def test_update_client_wrong_parent(self):
        instance = self.test_create_client()
        data = {
            'parent_key': 666,
            'value': "value value",
            'language': self.lang
        }
        response = self.factory.patch(reverse("translatelang-detail", args=[instance['id']]), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'create')
    def test_create_client_wrong_lang(self):
        data = {
            'parent_key': self.__translate.id,
            'value': "value value",
            'language': "wrong lang"
        }
        response = self.factory.post(reverse("translatelang-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'create')
    def test_create_client_missing_lang(self):
        data = {
            'parent_key': self.__translate.id,
            'value': "value value",
        }
        response = self.factory.post(reverse("translatelang-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'create')
    def test_create_client_missing_value(self):
        data = {
            'parent_key': self.__translate.id,
            'language': self.lang
        }
        response = self.factory.post(reverse("translatelang-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'create')
    def test_create_client_empty_value(self):
        data = {
            'parent_key': self.__translate.id,
            'value': "",
            'language': self.lang
        }
        response = self.factory.post(reverse("translatelang-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'create')
    def test_create_client_missing_parent(self):
        data = {
            'value': "",
            'language': self.lang
        }
        response = self.factory.post(reverse("translatelang-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'create')
    def test_create_client_wrong_parent(self):
        data = {
            'parent_key': 666,
            'value': "",
            'language': self.lang
        }
        response = self.factory.post(reverse("translatelang-list"), data=data)
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        instance = self.test_create_serializer()
        response = self.factory.delete(reverse("translatelang-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 403)
        response = self.factory_admin.delete(reverse("translatelang-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 204)

        response = self.factory.delete(reverse("translate-detail", args=[self.__translate.id]))
        self.assertEqual(response.status_code, 403)
        response = self.factory_admin.delete(reverse("translate-detail", args=[self.__translate.id]))
        self.assertEqual(response.status_code, 204)

    def test_delete_commit(self):
        from utils.function import contenttypes_uuid
        from utils.models import Commit

        instance = self.test_create_serializer()
        uuid = contenttypes_uuid(instance)
        self.assertNotEqual(Commit.objects.filter(uuid=uuid).count(), 0)
        response = self.factory_admin.delete(reverse("translatelang-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Commit.objects.filter(uuid=uuid).count(), 0)

    def test_delete_commit_parent(self):
        from utils.function import contenttypes_uuid
        from utils.models import Commit

        self.test_create_serializer_2()
        langs = self.__translate.langs.all()

        # delete child
        uuid = contenttypes_uuid(langs[0])
        self.assertNotEqual(Commit.objects.filter(uuid=uuid).count(), 0)
        langs[0].delete()
        self.assertEqual(Commit.objects.filter(uuid=uuid).count(), 0)

        uuid = contenttypes_uuid(langs[0])
        self.assertNotEqual(Commit.objects.filter(uuid=uuid).count(), 0)
        langs.delete()
        self.assertEqual(Commit.objects.filter(uuid=uuid).count(), 0)
