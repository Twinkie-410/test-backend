from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from api.v1.serializers.course_serializer import CourseSerializer
from users.models import Subscription

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""
    balance = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_balance(self, obj):
        return obj.balance.balance


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""
    user = CustomUserSerializer()
    course = CourseSerializer()

    class Meta:
        model = Subscription
        fields = '__all__'
