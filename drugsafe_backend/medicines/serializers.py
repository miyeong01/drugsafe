from rest_framework import serializers
from .models import Drug

class DrugListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = '__all__'