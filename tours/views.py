from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters 
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Tour
from .serializers import TourSerializer, TourListSerializer

class TourViewSet(ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['title', 'price']
    search_fields = ['title', 'description', 'price']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TourListSerializer
        return self.serializer_class

    def get_serializer_context(self):
        return {'request': self.request}