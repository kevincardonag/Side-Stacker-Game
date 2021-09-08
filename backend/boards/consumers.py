import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from boards.models import Game
from boards.utils import (
    get_or_create_room,
    get_room_and_set_game,
    update_all_screem,
    update_message_turn,
)


class BoardConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        room_data, current_player = get_or_create_room(
            self.room_name, self.channel_name
        )
        self.room_group_name = f"room_{self.room_name}_{current_player}"
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        self.update_initial_board(room_data)
        update_message_turn(room_data)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        data_json = json.loads(text_data)
        room_data, is_valid_turn = get_room_and_set_game(data_json, self.channel_name)
        if is_valid_turn:
            update_all_screem(room_data)
            update_message_turn(room_data)

    def update_board(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

    def update_turn(self, event):
        message = event["message_turn"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message_turn": message}))

    def update_initial_board(self, room_data):
        self.send(text_data=json.dumps({"message": room_data}))
