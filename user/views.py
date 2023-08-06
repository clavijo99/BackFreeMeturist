from django.contrib.auth import get_user_model
from rest_framework import permissions, authentication, mixins, generics
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from core.models import User, Comment
from register.serializer import CommentListSerializer
from user.serializer import UserSerializer, TokenSerializer


class LoginUser(ObtainAuthToken):
    """ get token authenticated """
    serializer_class = TokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ListUser(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet, mixins.UpdateModelMixin):
    """ list users """
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def get_authenticators(self):
        if self.request.method == "PUT":
            self.authentication_classes = [authentication.TokenAuthentication]
        return [auth() for auth in self.authentication_classes]


class UserMe(generics.RetrieveUpdateDestroyAPIView):
    """ get user authenticated """
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(['GET'])
def count_user(request, format=None):
    """ obtiene  """
    count = get_user_model().objects.all().count()
class UserMeId(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

class CommentById(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    lookup_field = 'pk'


class CommentsByUserId(generics.ListAPIView):
    serializer_class = CommentListSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return Comment.objects.filter(user_id=user_id)
