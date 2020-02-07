from rest_framework import routers
from persons.viewsets import PersonViewSet, AnalyticsViewSet


router = routers.DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'analytics', AnalyticsViewSet)