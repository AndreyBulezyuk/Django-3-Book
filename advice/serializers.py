from rest_framework import serializers
from .models import Advice

class AdviceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advice
        fields = ['content']