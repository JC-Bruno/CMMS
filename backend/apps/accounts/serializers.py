from rest_framework import serializers


class CurrentUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField(allow_blank=True)
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    is_superuser = serializers.BooleanField()
    tenant = serializers.DictField(allow_null=True)
    permissions = serializers.ListField(child=serializers.CharField())


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()