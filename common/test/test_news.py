from django.test import tag
from lib.test import BaseTest
from common.models import News
from django.urls import reverse


@tag('news')
class newsTest(BaseTest):

    @tag('auth')
    def test_auth(self):
        instance = News.objects.create(title="title", text="text", is_active=True)
        response = self.client.get(reverse("news-list"))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse("news-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse("news-list"))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse("news-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 403)
        response = self.client.delete(reverse("news-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 403)

        response = self.factory.get(reverse("news-list"))
        self.assertEqual(response.status_code, 200)
        response = self.factory.get(reverse("news-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        instance = News.objects.create(title="title", text="text", is_active=True)
        data = {
            'title': 'newtitle'
        }
        response = self.factory.post(reverse("news-list"), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.post(reverse("news-detail", args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 403)

    def test_patch(self):
        instance = News.objects.create(title="title", text="text",  is_active=True)
        data = {
            'title': 'newtitle'
        }
        response = self.factory.post(reverse("news-list"), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.post(reverse("news-detail", args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        instance = News.objects.create(title="title", text="text",  is_active=True)
        data = {
            'title': 'newtitle'
        }
        response = self.factory.put(reverse("news-list"), data=data)
        self.assertEqual(response.status_code, 403)
        response = self.factory.put(reverse("news-detail", args=[instance.id]), data=data)
        self.assertEqual(response.status_code, 403)

    def test_delete(self):
        instance = News.objects.create(title="title", text="text",  is_active=True)
        response = self.factory.delete(reverse("news-list"))
        self.assertEqual(response.status_code, 403)
        response = self.factory.delete(reverse("news-detail", args=[instance.id]))
        self.assertEqual(response.status_code, 403)
