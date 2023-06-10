from rest_framework import serializers


class HeartRateSerializer(serializers.Serializer):
    heart_rate = serializers.IntegerField()
