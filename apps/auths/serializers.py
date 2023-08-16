from rest_framework import serializers


class CustomUserSerializer(serializers.Serializer):
    bot_code = serializers.CharField()
    chat_id = serializers.CharField()