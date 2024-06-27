from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import *
from tours.models import Tour

User = get_user_model()

class Like(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models .CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.user} liked {self.tour}'

class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=RATING_CHOICES, null=True)

    def __str__(self):
        return f'Rating {self.user} {self.rating} for {self.tour}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment from {self.user} to {self.tour}'