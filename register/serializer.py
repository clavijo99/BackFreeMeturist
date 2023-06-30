from rest_framework import serializers
from core.models import Comment
from user.serializer import UserSerializer
from django.contrib.auth import get_user_model


class CommentSerializer(serializers.ModelSerializer):
    """ Model serializer from city model """

    # def validate_phone(self, value):
    #     if len(str(value)) > 10:
    #         raise serializers.ValidationError("Ensure this field has no more than 10 characters")
    #     return value

    # def validate_no_identification(self, value):
    #     if len(str(value)) > 10:
    #         raise serializers.ValidationError("Ensure this field has no more than 10 characters")
    #     return value

    class Meta:
        model = Comment
        fields = ('id', 'name', 'site', 'quality', 'created_at')
        read_only_fields = ('id',)


class CommentListSerializer(CommentSerializer):

    user = UserSerializer()

    class Meta(CommentSerializer.Meta):
        depth = 1
        fields = ('id', 'name', 'site', 'quality', 'user', 'created_at')
        read_only_fields = ('id', 'user')
