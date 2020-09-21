from lib.serializers import ModelSerializerBase
from rest_framework.serializers import SerializerMethodField
from gallery.models import People, PeopleLang
from common.models import Tag


class PeopleLangSerializer(ModelSerializerBase):
    class Meta:
        model = PeopleLang
        fields = ['biography', 'language']


class PeopleSerializer(ModelSerializerBase):
    langs = PeopleLangSerializer(many=True, required=False)

    class Meta:
        model = People
        fields = ['name', 'born', 'death', 'profil', 'wikipedia', 'langs', 'tags']


class PeopleSerializerPost(PeopleSerializer):
    class Meta(PeopleSerializer.Meta):
        pass

    def create(self, validated_data):
        # alway create tag same name has people name
        try:
            tag = Tag.objects.get(name=validated_data['name'])
        except Tag.DoesNotExist:
            tag = Tag.objects.create(name=validated_data['name'], creator=self.context['request'].user)
        instance = super().create(validated_data)
        instance.tags.add(tag)
        return instance

    def update(self, instance, validated_data):
        # alway update tag same name has people name
        try:
            tag = Tag.objects.get(name=instance.name)
        except Tag.DoesNotExist:
            tag = Tag.objects.create(name=validated_data['name'], creator=self.context['request'].user)
        obj = super().update(instance, validated_data)
        if tag.name != validated_data['name']:
            tag.name = validated_data['name']
            tag.save()
        obj.tags.add(tag)
        return obj


class PeopleSerializerGet(PeopleSerializerPost):
    profil = SerializerMethodField()

    class Meta(PeopleSerializerPost.Meta):
        pass

    def get_profil(self, obj):
        return {
            'original_jpeg': obj.to_url('profil'),
            'original_webp': obj.to_url('profil_webp'),
            'thumbnail_webp': obj.to_url('profil_thumbnail_webp'),
            'thumbnail_jpeg': obj.to_url('profil_thumbnail_jpeg'),
        }
