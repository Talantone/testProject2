from rest_framework import routers

from .views import GroupViewSet, PersonViewSet

app_name = "personsAndGroups"
router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'people', PersonViewSet, basename='people')






