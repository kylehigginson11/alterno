from rest_framework import serializers
from alternosite.models import Product


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'id')


class PopularItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name')
