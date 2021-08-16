from rest_framework import serializers


class AuthorizationAgentSerializer(serializers.Serializer):

    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
