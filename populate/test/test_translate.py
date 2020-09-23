from django.test import tag
from lib.test import BaseTest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from common.models import Translate, TranslateLang
import json


@tag('populate')
class PopulateTranslateTest(BaseTest):

    @tag('auth')
    def test_auth(self):
        response = self.client.get(reverse('translate_overview'))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('translate_upload'))
        self.assertEqual(response.status_code, 403)
        response = self.client.delete(reverse('translate_delete', args=[self.lang]))
        self.assertEqual(response.status_code, 403)

    def test_overview(self):
        response = self.factory.get(reverse('translate_overview'))
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        response = self.factory.delete(reverse('translate_delete', args=[self.lang]))
        self.assertEqual(response.status_code, 403)
        response = self.factory_admin.delete(reverse('translate_delete', args=["wrong"]))
        self.assertEqual(response.status_code, 400)

        self.test_upload_lang()
        count = Translate.objects.count()
        self.assertNotEqual(count, 0)
        self.assertNotEqual(TranslateLang.objects.count(), 0)
        response = self.factory_admin.delete(reverse('translate_delete', args=[self.lang]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Translate.objects.count(), count)
        self.assertEqual(TranslateLang.objects.count(), 0)

    def test_upload(self):
        response = self.factory.post(reverse('translate_upload'))
        self.assertEqual(response.status_code, 403)
        response = self.factory_admin.post(reverse('translate_upload'))
        self.assertEqual(response.status_code, 400)

        content = json.dumps({
            'auth': {
                'key': "value"
            },
            'test': {
                'recursive': {
                    'long': 'test',
                    'long2': 'test'
                },
                'pop': 'icic',
            }
        }).encode('utf-8')
        _file = SimpleUploadedFile("fr.json", content, content_type="application/json")
        data = {'file': _file}
        response = self.factory_admin.post(reverse('translate_upload'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Translate.objects.count(), 4)
        results = [
            ["auth.key", "value"],
            ["test.recursive.long", "test"],
            ["test.recursive.long2", "test"],
            ["test.pop", "icic"],
        ]
        for t in Translate.objects.all():
            _lst = [trans[0] for trans in results if trans[0] == t.key]
            self.assertEqual(len(_lst), 1)

        self.assertEqual(TranslateLang.objects.count(), 0)

    def test_upload_lang(self):
        content = json.dumps({
            'auth': {
                'key': "value"
            },
            'test': {
                'recursive': {
                    'long': 'test',
                    'long2': 'test'
                },
                'pop': 'icic',
            }
        }).encode('utf-8')
        _file = SimpleUploadedFile("fr.json", content, content_type="application/json")
        data = {'file': _file, 'language': self.lang}
        response = self.factory_admin.post(reverse('translate_upload'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Translate.objects.count(), 4)
        results = [
            ["auth.key", "value"],
            ["test.recursive.long", "test"],
            ["test.recursive.long2", "test"],
            ["test.pop", "icic"],
        ]
        for t in Translate.objects.all():
            _lst = [trans[0] for trans in results if trans[0] == t.key]
            self.assertEqual(len(_lst), 1)

        self.assertEqual(TranslateLang.objects.count(), 4)
        for t in TranslateLang.objects.all().select_related('parent_key'):
            _lst = [trans for trans in results if trans[0] == t.parent_key.key]
            self.assertEqual(len(_lst), 1)
            self.assertEqual(_lst[0][1], t.value)
            self.assertEqual(t.language, self.lang)

    def test_upload_wrong_lang(self):
        content = json.dumps({
            'auth': {
                'key': "value"
            },
            'test': {
                'recursive': {
                    'long': 'test',
                    'long2': 'test'
                },
                'pop': 'icic',
            }
        }).encode('utf-8')
        _file = SimpleUploadedFile("fr.json", content, content_type="application/json")
        data = {'file': _file, 'language': "wrong-lang"}
        response = self.factory_admin.post(reverse('translate_upload'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_upload_wrong_file(self):
        data = {'file': "icici", 'language': self.lang}
        response = self.factory_admin.post(reverse('translate_upload'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_upload_no_file(self):
        data = {'language': self.lang}
        response = self.factory_admin.post(reverse('translate_upload'), data=data)
        self.assertEqual(response.status_code, 400)