import json
from urllib import parse


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from personsAndGroups.models import Person, Group
from personsAndGroups.serializers import PersonSerializer, GroupSerializer
from personsAndGroups.views import PersonViewSet, GroupViewSet


class PersonsApiTestCase(APITestCase):
    def test_get_person_list(self):
        person1 = Person.objects.create(name='John Doe', age=36)
        person2 = Person.objects.create(name='Dohn Joe', age=37)
        url = reverse('people-list')
        response = self.client.get(url)
        serializer_data = PersonSerializer([person1, person2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_nonexistent_person(self):
        url = reverse('people-detail', args=[213456])
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_detail_person(self):
        person1 = Person.objects.create(name='John Doe', age=36)
        url = reverse('people-detail', args=[person1.pk])
        response = self.client.get(url)
        serializer_data = PersonSerializer(person1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_update_person(self):
        person1 = Person.objects.create(name='John Doe', age=36)
        factory = APIRequestFactory()
        request = factory.patch(reverse('people-detail', args=[person1.pk]), {'name': 'Dohn Joe'})
        view = PersonViewSet.as_view({'patch': 'partial_update'})
        response = view(request, pk=person1.pk)
        expected_data = {'id': 1, 'age': 36, 'name': 'Dohn Joe'}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_delete_person(self):
        person1 = Person.objects.create(name='John Doe', age=36)
        factory = APIRequestFactory()
        request = factory.delete(reverse('people-detail', args=[person1.pk]))
        view = PersonViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=person1.pk)
        expected_data = None
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(expected_data, response.data)


class GroupsApiTestCase(APITestCase):
    def test_get_group_list(self):
        person1 = Person.objects.create(name='John Doe', age=36)
        person2 = Person.objects.create(name='Dohn Joe', age=37)
        group1 = Group.objects.create(name='Group1')
        group2 = Group.objects.create(name='Group2')
        group1.persons.add(person1)
        group2.persons.add(person1, person2)
        url = reverse('groups-list')
        response = self.client.get(url)
        serializer_data = GroupSerializer([group1, group2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_nonexistent_group(self):
        url = reverse('groups-detail', args=[213456])
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_detail_group(self):
        person1 = Person.objects.create(name='John Doe', age=36)
        group1 = Group.objects.create(name='Group1')
        group1.persons.add(person1)
        url = reverse('groups-detail', args=[group1.pk])
        response = self.client.get(url)
        serializer_data = GroupSerializer(group1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_update_group(self):
        person1 = Person.objects.create(name='John Doe', age=36)
        person2 = Person.objects.create(name='Dohn Joe', age=63)
        group1 = Group.objects.create(name='Group1')
        group1.persons.add(person1, person2)
        factory = APIRequestFactory()
        request = factory.patch(reverse('groups-detail', args=[person1.pk]), {'name': 'GroupOfDohnsAndJohns'})
        view = GroupViewSet.as_view({'patch': 'partial_update'})
        response = view(request, pk=group1.pk)
        expected_data = {'id': 1, 'name': 'GroupOfDohnsAndJohns', 'persons': [1, 2]}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_delete_group(self):
        person1 = Person.objects.create(name='John Doe', age=36)
        group1 = Group.objects.create(name='Group1')
        group1.persons.add(person1)
        factory = APIRequestFactory()
        request = factory.delete(reverse('groups-detail', args=[group1.pk]))
        view = PersonViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=group1.pk)
        expected_data = None
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_delete_persons_from_group(self):
        person1 = Person.objects.create(name='John Doe', age=36)
        person2 = Person.objects.create(name='Dohn Joe', age=63)
        person3 = Person.objects.create(name='Joehn Dohnoe', age=69)
        group1 = Group.objects.create(name='Group1')
        group1.persons.add(person1, person2, person3)
        factory = APIRequestFactory()
        request = factory.delete(reverse('groups-detail', args=[group1.pk]), {'persons': [person1.pk]})
        view = GroupViewSet.as_view({'delete': 'remove_persons'})
        response = view(request, pk=group1.pk)
        expected_data = {'update': {'id': 1, 'name': 'Group1', 'persons': [person2.id, person3.id]}}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_add_persons_to_group(self):
        person1 = Person.objects.create(name='John Doe', age=36)
        person2 = Person.objects.create(name='Dohn Joe', age=63)
        person3 = Person.objects.create(name='Joehn Dohnoe', age=69)
        group1 = Group.objects.create(name='Group1')
        group1.persons.add(person2, person3)
        factory = APIRequestFactory()
        request = factory.patch(reverse('groups-detail', args=[group1.pk]), {'persons': [person1.pk]})
        view = GroupViewSet.as_view({'patch': 'add_persons'})
        response = view(request, pk=group1.pk)
        expected_data = {'update': {'id': 1, 'name': 'Group1', 'persons': [person1.id, person2.id, person3.id]}}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)
