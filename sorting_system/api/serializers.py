from rest_framework import serializers

class ClassificationSerializer(serializers.Serializer):
    class_name = serializers.CharField(source='class')
    confidence = serializers.FloatField()

    class Meta:
        fields = ['class_name', 'confidence']


class DetectionSerializer(serializers.Serializer):
    class_name = serializers.CharField(source='class')
    confidence = serializers.FloatField()
    box = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        fields = ['class_name', 'confidence', 'box']


class DetectionResponseSerializer(serializers.Serializer):
    detections = DetectionSerializer(many=True)
    processed_image_base64 = serializers.CharField()

    class Meta:
        fields = ['detections', 'processed_image_base64']