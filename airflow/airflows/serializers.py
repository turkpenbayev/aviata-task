from rest_framework import serializers


class ResultSerializer(serializers.Serializer):
    search_id = serializers.UUIDField(read_only=True, source='pk')
    status = serializers.CharField(read_only=True)
    items = serializers.JSONField(read_only=True ,source='items_dict')