from rest_framework.serializers import Serializer, \
    CharField, IntegerField, DateField, URLField, SlugField


class SearchContentserializer(Serializer):
    id = IntegerField()
    name = CharField()
    baner = URLField()
    release_date = DateField()