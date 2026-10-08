from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from app_run.models import Run
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
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = serializers.RunSerializer


class RunStartAPIView(APIView):
    def post(self, request, *args, **kwargs):
        run_id = kwargs.get('run_id')
        run = get_object_or_404(Run, id=run_id)
        if run.status != run.StatusChoices.INIT:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        run.status = run.StatusChoices.IN_PROGRESS
        run.save()

        return Response(status=status.HTTP_200_OK)


class RunStopAPIView(APIView):
    def post(self, request, *args, **kwargs):
        run_id = kwargs.get('run_id')
        run = get_object_or_404(Run, id=run_id)
        if run.status != run.StatusChoices.IN_PROGRESS:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        run.status = run.StatusChoices.FINISHED
        run.save()

        return Response(status=status.HTTP_200_OK)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        qs = self.queryset.exclude(is_superuser=True)

        type_of_user = self.request.query_params.get('type', None)

        if type_of_user == 'coach':
            qs = qs.filter(is_staff=True)
        if type_of_user == 'athlete':
            qs = qs.filter(is_staff=False)

        return qs