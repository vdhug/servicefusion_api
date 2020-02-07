from rest_framework import routers
from persons.viewsets import PersonViewSet, AnalyticsViewSet


router = routers.DefaultRouter()
router.register(r'persons', PersonViewSet, basename='persons')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')