from django.test import tag
from lib.test import BaseTest
from timeline.serializers.event import EventSerializer


@tag('model', 'event')
class EventTest(BaseTest):

    @tag('serializer')
    def test_create_serializer(self):
        data = {
            'title': 'test-title',
            'date': str(self.time)
        }
        serializer = EventSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.title, data['title'])
        self.assertEqual(obj.date, self.str_to_time(data['date']))
        self.check_creator(obj)
        return obj

    @tag('serializer')
    def test_create_serializer_update(self):
        obj = self.test_create_serializer()
        obj_id = obj.id
        obj_title = obj.title
        obj_date = obj.date
        data = {
            'title': 'test-update',
            'date': str(self.delta_time(days=2))
        }
        serializer = EventSerializer(instance=obj, data=data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid())
        update_obj = serializer.save()
        self.assertEqual(update_obj.id, obj_id)
        self.assertNotEqual(update_obj.title, obj_title)
        self.assertEqual(update_obj.title, data['title'])
        self.assertNotEqual(obj_date, self.str_to_time(data['date']))
        self.assertEqual(update_obj.date, self.str_to_time(data['date']))
        self.check_commit(update_obj)

    @tag('serializer')
    def test_create_serializer_same_date(self):
        obj = self.test_create_serializer()
        data = {
            'title': 'test-title',
            'date': str(obj.date)
        }
        serializer = EventSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_empty(self):
        data = {}

        serializer = EventSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
