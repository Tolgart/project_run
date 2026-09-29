from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from django.shortcuts import render

from app_run.models import Run
from app_run.serializers import RunSerializer


@api_view(['GET'])
def company_contacts(request):
    company_data = {
        'company_name': settings.COMPANY_NAME,
        'slogan': settings.SLOGAN,
        'contacts': settings.CONTACTS,
    }

    return Response(company_data)


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer