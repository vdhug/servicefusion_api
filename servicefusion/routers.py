from rest_framework import routers
from persons.viewsets import PersonViewSet


router = routers.DefaultRouter()
router.register(r'person', PersonViewSet)