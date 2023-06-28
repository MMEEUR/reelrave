from rest_framework.serializers import Serializer, \
    CharField, IntegerField, DateField, URLField, ImageField


class SearchContentserializer(Serializer):
    object_id = IntegerField()
    object_type = CharField()
    name = CharField()
    baner = ImageField()
    release_date = DateField()
    get_absolute_url = URLField()