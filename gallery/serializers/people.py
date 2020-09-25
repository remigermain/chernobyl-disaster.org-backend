from lib.serializers import ModelSerializerBase
from rest_framework.serializers import SerializerMethodField
from gallery.models import People, PeopleLang
from common.models import Tag


class PeopleLangSerializer(ModelSerializerBase):
    class Meta:
        model = PeopleLang
        fields = ['id', 'biography', 'language']


class PeopleSerializer(ModelSerializerBase):
    langs = PeopleLangSerializer(many=True, required=False)
    profil = SerializerMethodField()

    class Meta:
        model = People
        fields = ['id', 'name', 'born', 'death', 'profil', 'wikipedia', 'langs', 'tags']

    def create(self, validated_data):
        # alway create tag same name has people name
        try:
            tag = Tag.objects.get(name=validated_data['name'])
        except Tag.DoesNotExist:
            tag = Tag.objects.create(name=validated_data['name'])
        instance = super().create(validated_data)
        instance.tags.add(tag)
        return instance

    def update(self, instance, validated_data):
        # alway update tag same name has people name
        try:
            tag = Tag.objects.get(name=instance.name)
        except Tag.DoesNotExist:
            tag = Tag.objects.create(name=validated_data['name'])

        obj = super().update(instance, validated_data)

        if 'name' in validated_data and tag.name != validated_data['name']:
            tag.name = validated_data['name']
            tag.save()
        obj.tags.add(tag)
        return obj

    def get_profil(self, obj):
        return {
            'original_jpeg': obj.to_url('profil'),
            'original_webp': obj.to_url('profil_webp'),
            'thumbnail_webp': obj.to_url('profil_thumbnail_webp'),
            'thumbnail_jpeg': obj.to_url('profil_thumbnail_jpeg'),
        }


class PeopleSerializerPost(PeopleSerializer):
    profil = None

    class Meta(PeopleSerializer.Meta):
        pass
