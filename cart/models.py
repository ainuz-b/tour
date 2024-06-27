from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from tours.models import Tour

User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        cart_items = self.cart_items.all()
        return sum(item.total_price() for item in cart_items)

    def clear_cart(self):
        self.cart_items.all().delete()

    def __str__(self):
        return f"Cart #{self.id} - User: {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.tour.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.tour.title} in Cart #{self.cart.id}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('open', 'Открыт'),
        ('in_process', 'В обработке'),
        ('canceled', 'Отмененный'),
        ('finished', 'Завершенный')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='order', null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    verification_code = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} with total price {self.total_price} - User: {self.user.username}"

    def create_verification_code(self):
        code = get_random_string(10)
        self.verification_code = code 
        self.save()
