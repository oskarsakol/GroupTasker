from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group,User
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, filters
from .models import Task
from .serializers import TaskSerializer, UserSerializer, GroupSerializer
from django_filters.rest_framework import DjangoFilterBackend



class TaskViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    model = Task
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)
    filter_fields = ('completed',)
    ordering = ('-created',)
    search_fields = ('name',)

    def get_queryset(self):

        queryset = self.model.objects.all().filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):

        return serializer.save(creator=self.request.user)


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

