from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Cart, CartItem, Order
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        cart_id = request.data.get('cart_id')
        user = request.user

        try:
            cart = Cart.objects.get(id=cart_id, user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist."}, status=status.HTTP_404_NOT_FOUND)

        order = Order.objects.create(
            user=user,
            cart=cart,
            total_price=cart.total_price(),
        )

        cart.clear_cart()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
