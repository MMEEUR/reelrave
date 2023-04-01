from rest_framework.serializers import ModelSerializer
from .models import Person, Role


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ('role',)


class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = ('name', 'picture')


class PersonListSerializer(ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = ('name', 'picture', 'roles')


class PersonDetailSerializer(ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = ('name', 'birthday', 'height_centimeter', 'picture', 'roles')