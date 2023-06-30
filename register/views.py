from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from register.serializer import CommentSerializer, CommentListSerializer
from core.models import Comment
from register.permissions import CommentsOwnerUser
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.http import JsonResponse
import os


class CommentModelViewSet(ModelViewSet):
    """ model view set comment model """
    permission_classes = [IsAuthenticated, CommentsOwnerUser]
    authentication_classes = [TokenAuthentication]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        """ save user auth """
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CommentListSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.action == 'list':
            return Comment.objects.filter(user=self.request.user)
        return Comment.objects.all()

class CommenList(generics.ListAPIView):
    serializer_class = CommentListSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        site_id = self.kwargs.get('site_id')
        if site_id:
            queryset = queryset.filter(site__id=site_id)
        return queryset

@api_view(['POST'])
def send_email(request, format=None):
    if request.method == 'POST':
        message = request.data.get('message', '')
        full_name = request.data.get('full_name', '')
        email = request.data.get('email', '')
        subject = 'Contact tourism page from ' + full_name

        EMAIL_TO = os.environ.get('EMAIL_TO')

        send_mail(
            subject,
            message,
            email,
            [EMAIL_TO],
            fail_silently=False,
        )

        return JsonResponse({'success': True, 'message': "Email send successfull!"})
    return JsonResponse({'success': False, 'message': 'Error send email!'})
