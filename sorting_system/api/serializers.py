from rest_framework import serializers

class ClassificationSerializer(serializers.Serializer):
    class_name = serializers.CharField()
    confidence = serializers.FloatField()