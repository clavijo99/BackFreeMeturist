from django.urls import path, include
from rest_framework.routers import DefaultRouter
from location.views import CategoryListViewSet, SiteViewSet, SitesList, RecommendedList

router = DefaultRouter()
router.register('categories', CategoryListViewSet, basename='category')
router.register('sites', SiteViewSet, basename='site')

app_name = 'location'

urlpatterns = [
    path('sites/<int:category_id>/list/', SitesList.as_view(), name='sites-list'),
    path('recommended/', RecommendedList.as_view(), name='recommended-list'),
    path('', include(router.urls))
]
