from rest_framework import generics

from .serializers import BoardSerializer
from boards.models import Game


class BoardCreateApiView(generics.CreateAPIView):
    serializer_class = BoardSerializer


class BoardRetrieveApiView(generics.RetrieveAPIView):
    serializer_class = BoardSerializer
    queryset = Game.objects.all()
