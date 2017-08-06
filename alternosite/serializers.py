from rest_framework import serializers
from alternosite.models import Product


class RecentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
