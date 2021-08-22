import logging
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from boards.utils import get_or_create_room, get_room_and_set_game, update_all_screem


class BoardConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"room_{self.room_name}"
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        room_data = get_or_create_room(self.room_name)
        self.update_initial_board(room_data)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        data_json = json.loads(text_data)
        room_data = get_room_and_set_game(data_json)
        update_all_screem(room_data)

    def update_board(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

    def update_initial_board(self, room_data):
        self.send(text_data=json.dumps({"message": room_data}))
