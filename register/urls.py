from django.urls import path, include
from rest_framework.routers import DefaultRouter
from register.views import CommentModelViewSet, CommenList, send_email

app_name = 'register'

router = DefaultRouter()
router.register('comments', CommentModelViewSet, basename='comment')

urlpatterns = [
    path('comments/<int:site_id>/list/', CommenList.as_view(), name='comments-list'),
    path('send/mail/', send_email, name='send_email'),
    path('', include(router.urls)),
]
