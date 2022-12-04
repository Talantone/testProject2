from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Group, Person
from .serializers import GroupSerializer, PersonSerializer


class GroupViewSet(ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    @action(methods=['delete'], detail=True)
    def remove_persons(self, request, pk):
        group = self.get_object()
        persons_to_remove = Person.objects.get(id__in=request.data['persons'])
        group.persons.remove(persons_to_remove)
        return Response({'update': GroupSerializer(group).data})

    @action(methods=['patch'], detail=True)
    def add_persons(self, request, pk):
        group = self.get_object()
        persons_to_remove = Person.objects.get(id__in=request.data['persons'])
        group.persons.add(persons_to_remove)
        return Response({'update': GroupSerializer(group).data})


class PersonViewSet(ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
