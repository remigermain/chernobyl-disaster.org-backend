from django.test import tag
from common.serializer import PeopleSerializer
from lib.test import BaseTest


@tag('model', 'people')
class PeopleTest(BaseTest):

    @tag('serializer')
    def test_create_serializer(self):
        data = {
            'name': 'test'
        }
        serializer = PeopleSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.name, data['name'])
        self.check_creator(obj)
        return obj

    @tag('serializer')
    def test_create_serializer_update(self):
        obj = self.test_create_serializer()
        old_name = obj.name
        data = {
            'name': 'test-updated'
        }
        serializer = PeopleSerializer(instance=obj, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        update_obj = serializer.save()
        self.assertEqual(update_obj.id, obj.id)
        self.assertNotEqual(obj.name, old_name)
        self.assertEqual(update_obj.name, data['name'])
        self.check_commit(obj)

    @tag('serializer')
    def test_create_serializer_empty(self):
        data = {}

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