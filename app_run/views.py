from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from app_run.models import Run
from app_run import serializers


@api_view(['GET'])
def company_contacts(request):
    """
    Передаёт реквизиты компании для использования на элементах сайта
    через API 'api/company_details/'
    """
    company_data = {
        'company_name': settings.COMPANY_NAME,
        'slogan': settings.SLOGAN,
        'contacts': settings.CONTACTS,
    }

    return Response(company_data)

class ProjectPagination(PageNumberPagination):
    page_size_query_param = 'size'

class RunViewSet(viewsets.ModelViewSet):
    """
    Возвращает все объекты забегов.
    """
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = serializers.RunSerializer
    pagination_class = ProjectPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'athlete']
    ordering_fields = ['created_at']


class RunStartAPIView(APIView):
    """
    Переводит забег с id = run_id в статус 'in_progress'.
    """
    def post(self, request, *args, **kwargs):
        run_id = kwargs.get('run_id')
        run = get_object_or_404(Run, id=run_id)
        if run.status != run.StatusChoices.INIT:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        run.status = run.StatusChoices.IN_PROGRESS
        run.save()

        return Response(status=status.HTTP_200_OK)


class RunStopAPIView(APIView):
    """
    Переводит забег с id = run_id в статус 'finished'.
    """
    def post(self, request, *args, **kwargs):
        run_id = kwargs.get('run_id')
        run = get_object_or_404(Run, id=run_id)
        if run.status != run.StatusChoices.IN_PROGRESS:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        run.status = run.StatusChoices.FINISHED
        run.save()

        return Response(status=status.HTTP_200_OK)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Выводит список всех пользователей, за исключением администраторов,
    на страницах сайта
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = ProjectPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['date_joined']

    def get_queryset(self):
        qs = self.queryset.exclude(is_superuser=True)

        type_of_user = self.request.query_params.get('type', None)

        if type_of_user == 'coach':
            qs = qs.filter(is_staff=True)
        if type_of_user == 'athlete':
            qs = qs.filter(is_staff=False)

        return qs