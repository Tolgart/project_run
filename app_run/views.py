from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from django.contrib.auth.models import User

from app_run.models import Run
from app_run.serializers import RunSerializer, UserSerializer


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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = self.queryset.exclude(is_superuser=True)

        type_of_user = self.request.query_params.get('type', None)

        if type_of_user == 'coach':
            qs = qs.filter(is_staff=True)
        if type_of_user == 'athlete':
            qs = qs.filter(is_staff=False)

        return qs