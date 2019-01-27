from django.contrib.auth.models import Group, User
from rest_framework import serializers, request
from .models import Task
from django.contrib.auth import get_user_model


class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='creator.username', read_only=True)
    # user = serializers.CharField(max_length=20, choices='user.username')
    # groups = serializers.CharField(read_only=True)

    # def create(self, validated_data):
    #     user_group = request.user.groups.get()
    #     User.objects.filter(groups__name=user_group).set(validated_data.get('user', User.objects))



    class Meta:
        model = Task
        fields = ('creator', 'user', 'name', 'description', 'completed', 'created')
        # fields = ('user', 'groups', 'name', 'description', 'completed', 'created')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        # user_groups = Group.objects.get(name='groups')
        user.groups.set(validated_data.get('groups', user.groups))
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'groups')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
