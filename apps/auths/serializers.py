from rest_framework import serializers
from auths.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['bot_code', 'chat_id']
