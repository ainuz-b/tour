from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, toggle_like, toggle_rating

router = DefaultRouter()
router.register('comment', CommentViewSet)

urlpatterns = [
    path('like/<int:id>/', toggle_like, name='toggle-like'),
    path('rating/<int:id>/', toggle_rating, name='toggle-rating'),
    path('', include(router.urls)),
]