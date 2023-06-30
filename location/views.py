from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, mixins, GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from core.models import Category, Site, Recommended
from location.serializer import CategorySerializer, SiteSerializer, SiteListSerializer, RecommendedSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics


class CategoryListViewSet(ModelViewSet):
    """
    view set from list and retrieve countries
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        """"""
        if self.action == 'update' or self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_authenticators(self):
        if self.request.method == "PUT" or self.request.method == 'POST' or self.request.method == 'DELETE':
            self.authentication_classes = [TokenAuthentication]
        return [auth() for auth in self.authentication_classes]


class SiteViewSet(ModelViewSet):
    """
    view set from list and retrieve sites
    """
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.GET.get('name', None)
        category = self.request.GET.get('category_id', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        if category:
            queryset = queryset.filter(category_id=category)
        return queryset.order_by('-quality')

    def get_permissions(self):
        """"""
        if self.action == 'update' or self.action == 'create' or self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [AllowAny]

        return [permission() for permission in self.permission_classes]

    def get_authenticators(self):
        if self.request.method == "PUT" or self.request.method == 'POST' or self.request.method == 'DELETE':
            self.authentication_classes = [TokenAuthentication]
        return [auth() for auth in self.authentication_classes]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return SiteListSerializer
        return self.serializer_class

class SitesList(generics.ListAPIView):
    serializer_class = SiteSerializer

    def get_queryset(self):
        queryset = Site.objects.all()
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset

class RecommendedList(generics.ListAPIView):
    serializer_class = RecommendedSerializer
    queryset = Recommended.objects.all()
