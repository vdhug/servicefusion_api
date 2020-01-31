from rest_framework import routers
from persons.viewsets import AddressViewSet


router = routers.DefaultRouter()
router.register(r'address', AddressViewSet)