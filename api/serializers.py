from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'mobile', 'password']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            mobile=validated_data.get('mobile', ''),
            password=validated_data['password']
        )
        return user

class TaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), many=True, required=False, write_only=True
    )
    assigned_users_detail = UserSerializer(source='assigned_users', many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

