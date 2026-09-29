from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import User

from app_run import models
from app_run import serializers


@api_view(['GET'])
def company_contacts(request):
    company_data = {
        'company_name': settings.COMPANY_NAME,
        'slogan': settings.SLOGAN,
        'contacts': settings.CONTACTS,
    }

    return Response(company_data)


class RunViewSet(viewsets.ModelViewSet):
    queryset = models.Run.objects.all()
    serializer_class = serializers.RunSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        qs = self.queryset.exclude(is_superuser=True)

        coach = self.request.query_params.get('coach', None)
        athlete = self.request.query_params.get('athlete', None)

        if coach and not athlete:
            qs = qs.filter(is_staff=True)

        if athlete and not coach:
            qs = qs.filter(is_staff=False)

        return qs
