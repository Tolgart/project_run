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
from django.db.models import Count, Sum

from app_run.models import Run, AthleteInfo, Challenge, Position
from app_run import serializers

from .services import calculate_distance

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
        user = run.athlete

        if run.status != run.StatusChoices.IN_PROGRESS:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        run.status = run.StatusChoices.FINISHED
        run.distance = calculate_distance(run_id)
        run.save()


        total_stats = user.runs.filter(status=run.StatusChoices.FINISHED).aggregate(
            finished_runs = Count('distance'),
            total_distance = Sum('distance')
        )

        if total_stats['finished_runs'] == 10:
            Challenge.objects.get_or_create(full_name="Сделай 10 Забегов!", athlete=user)
        if total_stats['total_distance'] >= 50:
            try:
                Challenge.objects.get_or_create(full_name='Пробеги 50 километров!', athlete=user)

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


class AthleteInfoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)

        athlete_info, created = AthleteInfo.objects.get_or_create(user_id=user)

        serializer = serializers.AthleteInfoSerializer(athlete_info)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)

        goals = request.data.get('goals')
        weight = request.data.get('weight')

        if not (weight.isdigit() and 0 < int(weight) < 900):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        athlete_info, created = AthleteInfo.objects.update_or_create(user_id=user,
                                                                     defaults={'goals': goals, 'weight': weight}
                                                                     )

        serializer = serializers.AthleteInfoSerializer(athlete_info)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = serializers.ChallengeSerializer

    def get_queryset(self):
        qs = self.queryset

        athlete = self.request.query_params.get('athlete', None)
        if athlete:
            qs = qs.filter(athlete=athlete)

        return qs


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = serializers.PositionSerializer

    def get_queryset(self):
        qs = self.queryset

        run = self.request.query_params.get('run', None)
        if run:
            qs = qs.filter(run=run)

        return qs

