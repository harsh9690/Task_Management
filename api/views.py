# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Task
from .serializers import TaskSerializer, UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'User registered successfully', 'user': UserSerializer(user).data}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    user_ids = request.data.get('user_ids', [])
    users = get_user_model().objects.filter(id__in=user_ids)
    task.assigned_users.add(*users)
    return Response({'message': 'Task assigned successfully'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks_for_user(request, user_id):
    tasks = Task.objects.filter(assigned_users__id=user_id)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)
