from rest_framework import serializers

from boards.models import Game


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["room_name", "board"]
