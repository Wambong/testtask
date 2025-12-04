# from rest_framework import serializers, viewsets
# from django.shortcuts import get_object_or_404
# from .models import Item, Order
#
#
# # Serializers
# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = '__all__'
#
#
# class OrderSerializer(serializers.ModelSerializer):
#     items = ItemSerializer(many=True, read_only=True)
#     item_ids = serializers.PrimaryKeyRelatedField(
#         queryset=Item.objects.all(), many=True, write_only=True, source='items'
#     )
#
#     class Meta:
#         model = Order
#         fields = ['id', 'table_number', 'items', 'item_ids', 'total_price', 'status', 'created_at']
#         read_only_fields = ['total_price', 'created_at']
#
#     def create(self, validated_data):
#         items = validated_data.pop('items', [])
#         order = Order.objects.create(**validated_data)
#         order.items.set(items)
#         order.total_price = sum(item.price for item in items)
#         order.save()
#         return order
#
#     def update(self, instance, validated_data):
#         items = validated_data.pop('items', None)
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         if items is not None:
#             instance.items.set(items)
#             instance.total_price = sum(item.price for item in items)
#         instance.save()
#         return instance
#
#
#
