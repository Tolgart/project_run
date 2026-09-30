from rest_framework import serializers
from .models import Run
from django.contrib.auth.models import User

class UserSerializerForRunViewSet(serializers.ModelSerializer):
    """
    Используется как вложенный сериализатор для RunSerializer,
    который отдаёт только нужные поля модели User при запросе
    через api/runs.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']


class RunSerializer(serializers.ModelSerializer):
    athlete_data = UserSerializerForRunViewSet(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type']

    def get_type(self, obj):
        return 'coach' if obj.is_staff else 'athlete'