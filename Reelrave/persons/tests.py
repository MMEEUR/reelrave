from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Person, Role


class PersonTest(APITestCase):
    def setUp(self):
        self.role = Role.objects.create(role="Test")
        self.role_2 = Role.objects.create(role="Test2")

        self.person = Person.objects.create(
            name="TestPerson",
            birthday="2018-04-20",
            height_centimeter=200,
        )

        self.person.roles.add(self.role)

        self.person_2 = Person.objects.create(
            name="TestPerson2",
            birthday="2018-04-22",
            height_centimeter=202,
        )

        self.person_2.roles.add(self.role_2)

        return super().setUp()

    def test_person_list(self):
        url = reverse("persons:person_list")

        test_data = {
            "Roles": [
                {"role": "Test", "slug": "test"},
                {"role": "Test2", "slug": "test2"},
            ],
            "Persons": [
                {
                    "name": "TestPerson",
                    "picture": None,
                    "roles": [{"role": "Test", "slug": "test"}],
                },
                {
                    "name": "TestPerson2",
                    "picture": None,
                    "roles": [{"role": "Test2", "slug": "test2"}],
                },
            ],
        }

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Roles"], test_data["Roles"])
        self.assertEqual(response.data["Persons"], test_data["Persons"])

    def test_person_detail(self):
        url = reverse("persons:person_detail", kwargs={"id": self.person.id})

        test_data = {
            "name": "TestPerson",
            "birthday": "2018-04-20",
            "height_centimeter": "200",
            "picture": None,
            "roles": [{"role": "Test", "slug": "test"}],
        }

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, test_data)

    def test_person_list_by_role(self):
        url = reverse("persons:person_list_by_role", kwargs={"role": self.role_2.slug})

        test_data = {
            "Roles": {"role": "Test2", "slug": "test2"},
            "Persons": [
                {
                    "name": "TestPerson2",
                    "picture": None,
                    "roles": [{"role": "Test2", "slug": "test2"}],
                }
            ],
        }

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Roles"], test_data["Roles"])
        self.assertEqual(response.data["Persons"], test_data["Persons"])

    def test_person_search(self):
        query = str(self.person.name)

        url = reverse("persons:person_search") + f"?q={query}"

        test_data = {
            "query": query,
            "results": [
                {
                    "name": "TestPerson",
                    "picture": None,
                    "roles": [{"role": "Test", "slug": "test"}],
                }
            ],
        }

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, test_data)