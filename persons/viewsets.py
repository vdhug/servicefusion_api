from rest_framework import viewsets
from .models import Person, Email, Address, Phone
from .serializers import PersonSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date
import datetime
from dateutil.relativedelta import relativedelta


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class AnalyticsViewSet(viewsets.ViewSet):
    
    @action(methods=['get'], detail=False)
    def stats(self, request):
        today = date.today()

        oldest = self.get_queryset().order_by("birth").first()
        oldest_age = today.year - oldest.birth.year - ((today.month, today.day) < (oldest.birth.month, oldest.birth.day))

        younger = self.get_queryset().order_by("birth").last()
        younger_age = today.year - younger.birth.year - ((today.month, today.day) < (younger.birth.month, younger.birth.day))

        total= self.get_queryset().count()
        return Response(
            {
                'total': total,
                'younger': {
                    'age': younger_age,
                    'birth': younger.birth
                },
                'oldest': {
                    'age': oldest_age,
                    'birth': oldest.birth
                }
            }
        )

    @action(methods=['get'], detail=False)
    def ages(self, request):
        today = date.today()
        adult = (today - relativedelta(years=20)).year
        elderly = (today - relativedelta(years=60)).year

        young_count = Person.objects.all().filter(birth__year__gte=adult).count()
        elderly_count = Person.objects.all().filter(birth__year__lte=elderly).count()
        
        adult_count = Person.objects.all().filter(birth__year__range=(elderly, adult)).count()

        r = {
            "data": [young_count, adult_count, elderly_count],
            "labels": ["Young", "Adult", "Elderly"]
        }
        return Response(r)
    
    @action(methods=['get'], detail=False)
    def secondary(self, request):        
        phones_count = Phone.objects.all().count()
        emails_count = Email.objects.all().count()
        addresses_count = Address.objects.all().count()

        r = {
            "data": [phones_count, emails_count, addresses_count],
            "labels": ["Phones", "Emails", "Addresses"]
        }
        return Response(r)