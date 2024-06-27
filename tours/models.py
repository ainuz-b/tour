from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify

User = get_user_model()

class Tour(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50, blank=True)
    title = models.CharField(max_length=200, verbose_name='Название тура')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='product_img/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена') 
    available_slots = models.IntegerField(default=0, verbose_name='Доступные места')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()
