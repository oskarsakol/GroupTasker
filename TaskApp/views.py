from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, filters
from rest_framework.response import Response

from .models import Task, Comment
from .serializers import TaskSerializer, UserSerializer, GroupSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins


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

    @action(methods=['get', ], detail=True)
    def comments(self, request, pk=None):
        instance = self.get_object()

        comments = instance.assigned_comment.all()

        serializer_class = CommentSerializer

        serializer = serializer_class(comments, many=True)

        return Response(serializer.data)


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

    @action(methods=['get', ], detail=True)
    def users(self, request, pk=None):
        instance = self.get_object()

        users = instance.user_set.all()

        serializer_class = UserSerializer

        serializer = serializer_class(users, many=True)

        return Response(serializer.data)


class UserViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get', ], detail=True)
    def groups(self, request, pk=None):
        instance = self.get_object()

        groups = instance.groups.all()

        serializer_class = GroupSerializer

        serializer = serializer_class(groups, many=True)

        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    model = Comment
    serializer_class = CommentSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = ('-created',)

    def get_queryset(self):
        queryset = self.model.objects.all().filter(creator=self.request.user)
        return queryset

    def perform_create(self, serializer):
        return serializer.save(creator=self.request.user)
