from rest_framework import serializers
from .models import Tour

class TourSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Tour
        fields = '__all__'

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Цена не может быть отрицательной')
        return price

    def validate_available_slots(self, available_slots):
        if available_slots < 0:
            raise serializers.ValidationError('Количество доступных мест не может быть отрицательным')
        return available_slots

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs

class TourListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ['title', 'price', 'image', 'available_slots']
