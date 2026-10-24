from rest_framework import serializers
from .models import Run, AthleteInfo
from django.contrib.auth.models import User

class UserSerializerForRunSerializer(serializers.ModelSerializer):
    """
    Используется как вложенный сериализатор для RunSerializer,
    который отдаёт только нужные поля модели User при запросе
    через api/runs.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']


class RunSerializer(serializers.ModelSerializer):
    athlete_data = UserSerializerForRunSerializer(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type', 'runs_finished']

    def get_type(self, obj):
        return 'coach' if obj.is_staff else 'athlete'

    def get_runs_finished(self, obj):
        return obj.runs.filter(status=Run.StatusChoices.FINISHED).count()


class AthleteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AthleteInfo
        fields = ['goals', 'weight']