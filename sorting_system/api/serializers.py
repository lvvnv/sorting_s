from rest_framework import serializers

class ClassificationSerializer(serializers.Serializer):
    class_name = serializers.CharField(source='class')
    confidence = serializers.FloatField()

    class Meta:
        fields = ['class_name', 'confidence']