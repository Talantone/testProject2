from django.test import TestCase

from personsAndGroups.models import Person, Group
from personsAndGroups.serializers import PersonSerializer, GroupSerializer


class PersonSerializerTestCase(TestCase):
    def test_ok(self):
        person1 = Person.objects.create(name='John Doe', age=36)
        person2 = Person.objects.create(name='Dohn Joe', age=37)
        data = PersonSerializer([person1, person2], many=True).data
        expected_data = [
            {
                'id': person1.id,
                'name': 'John Doe',
                'age': 36
            },
            {
                'id': person2.id,
                'name': 'Dohn Joe',
                'age': 37
            }
        ]
        self.assertEqual(expected_data, data)

class GroupSerializerTestCase(TestCase):
    def test_ok(self):
        person1 = Person.objects.create(name='Dohn Doe', age=36)
        person2 = Person.objects.create(name='John Joe', age=37)
        group1 = Group.objects.create(name='Group1')
        group2 = Group.objects.create(name='Group2')
        group1.persons.add(person1)
        group2.persons.add(person2)
        data = GroupSerializer([group1, group2], many=True).data
        expected_data = [
            {
                'id': group1.id,
                'name': 'Group1',
                'persons': [
                    person1.id
                ]
            },
            {
                'id': group2.id,
                'name': 'Group2',
                'persons': [
                    person2.id
                ]
            }
        ]
        self.assertEqual(expected_data, data)
