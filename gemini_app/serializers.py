from rest_framework import serializers
from gemini_app.models import *

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
