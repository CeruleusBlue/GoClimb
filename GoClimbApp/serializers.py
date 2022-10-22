from rest_framework import serializers

class CragRouteSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    grade = serializers.IntegerField()
    image = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=100)
    bolts = serializers.IntegerField()
    rating = serializers.IntegerField()
    length = serializers.IntegerField()
    ascents = serializers.IntegerField()
    firstAscent = serializers.CharField(max_length=100)