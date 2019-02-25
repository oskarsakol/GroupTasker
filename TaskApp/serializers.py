from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Task, Comment
from django.contrib.auth import get_user_model
User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'creator', 'user', 'completed', 'created', 'edited', 'group')
        read_only_fields = ('id', 'creator', 'created', 'edited')

    def validate(self, attrs):
        creator = self.context['request'].user
        user = attrs.get('user')
        group = attrs.get('group')
        group_users = group.user_set.all()

        if creator not in group_users:
            raise ValidationError(f'You cannot add user to group {group.name}.')

        if user not in group_users:
            raise ValidationError(f'You cannot assign task for user {user.username} to group {group.name}.')

        return attrs


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.groups.set(validated_data.get('groups', user.groups))
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'groups')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'creator', 'description', 'task', 'created')
        read_only_fields = ('id', 'creator', 'created')

    def validate(self, attrs):
        user_group = self.context['request'].user.groups.all()

        task = attrs.get('task')
        task_group = attrs.get('task').group
        creator = self.context['request'].user

        last_id = Comment.objects.values_list('pk', flat=True).filter(task=task).order_by('id').last()
        if last_id:
            creator_of_previous_post = Comment.objects.get(id=last_id).creator
            validate_creator(creator, creator_of_previous_post)

        if task_group not in user_group:
            raise ValidationError(f'You can not comment on this task because '
                                  f'your not the member of the group {task_group.name}.')

        return attrs

    def validate_description(self, description):

        content = [description]

        if content[0].islower():
            raise ValidationError('Your comment has to start with upper letter')

        return description


def validate_creator(current_creator, previous_creator):

    if current_creator == previous_creator:
        raise ValidationError('You can not comment on this post twice in a row')

    return current_creator, previous_creator
