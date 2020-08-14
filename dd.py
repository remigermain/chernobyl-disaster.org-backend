from timeline.serializers.picture import PictureSerializerPost
from django.core.files.uploadedfile import SimpleUploadedFile
data = {'title': 'wrgwegwegwegwe', 'event': '', 'date': '2020-08-13T13:22:00.000Z', 'photographer': '', 'langs': [{'id': '5', 'title': 'fwefrwe', 'language': 'fr'}]}

image = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b'
file = SimpleUploadedFile('small.gif', image, content_type='image/gif')
data['picture'] = file
instance = Picture.objects.get(id=2)
s = PictureSerializerPost(instance, data=data)
s.is_valid()
s.errors

from timeline.serializers.picture import PictureLangSerializer
p = PictureLangSerializer(many=True, required=True)
d = {'title': 'wrgwegwegwegwe', 'tags': '1', 'event': '', 'date': '2020-08-14T17:52:00.000Z', 'photographer': '', 'langs': [{'title': 'fefwe', 'language': 'fr'}]}
data = [{'title': 'fwefwe', 'language': 'fr'}]
p.get_value(d)