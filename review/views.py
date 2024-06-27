from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from tours.models import Tour

from .permissions import IsOwnerOrReadOnly
from .models import Comment, Like, Rating
from .serializers import CommentSerializer

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in self.permission_classes] 
        
@api_view(['POST'])
def toggle_like(request, id):
    user = request.user
    if not user.is_authenticated:
        return Response(status=401)
    tour = get_object_or_404(Tour, id=id)
    if Like.objects.filter(user=user, tour=tour).exists():
        Like.objects.filter(user=user, tour=tour).delete()
        return Response(status=204)
    else:
        Like.objects.create(user=user, tour=tour)
        return Response(status=201)

@api_view(['POST'])
def toggle_rating(request, id):
    user = request.user
    if not user.is_authenticated:
        return Response(status=401)
    tour = get_object_or_404(Tour, id=id)
    rating_value = request.data.get('rating')
    if not rating_value:
        return Response({"error": "Rating value is required."}, status=400)
    
    try:
        rating_value = int(rating_value)
        if rating_value < 1 or rating_value > 5:
            return Response({"error": "Rating value must be between 1 and 5."}, status=400)
    except ValueError:
        return Response({"error": "Invalid rating value."}, status=400)

    existing_rating = Rating.objects.filter(user=user, tour=tour).first()
    if existing_rating:
        existing_rating.rating = rating_value
        existing_rating.save()
    else:
        Rating.objects.create(user=user, tour=tour, rating=rating_value)
    
    return Response(status=201)
