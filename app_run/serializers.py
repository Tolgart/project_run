from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404

from .models import Run, AthleteInfo, Challenge, Position
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
        fields = ['user_id', 'goals', 'weight']


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'latitude', 'longitude']

    def validate_id(self, value):
        run = get_object_or_404(Run, id=value)

        if run.status != Run.StatusChoices.IN_PROGRESS:
            raise serializers.ValidationError("Забег должен быть в статусе 'in_progress'")

        return value

    def validate_latitude(self, value):
        if not (-90.0 <= value <= 90.0):
            raise serializers.ValidationError()

        return value

    def validate_longitude(self, value):
        if not (-180.0 <= value <= 180.0):
            raise serializers.ValidationError()

        return value