from rest_framework import serializers
from .models import *


class RollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roll
        fields = "__all__"


class RoundCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = ["pk", "user"]


class RoundUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = ["pk", "user", "is_finished"]


class RoundDetailSerializer(serializers.ModelSerializer):
    spins = RollSerializer(many=True)

    class Meta:
        model = Round
        fields = "__all__"