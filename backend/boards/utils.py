import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from boards.constants import MAX_MOVEMENTS
from boards.models import Game


def get_or_create_room(room_name):
    game, created = Game.objects.get_or_create(room_name=room_name)
    room_data = build_room_data(game)
    return room_data


def get_room(room_name):
    try:
        game = Game.objects.get(room_name=room_name)
        return game
    except Game.DoesNotExist as error:
        logging.info(f"Game not found: {error}")


def get_room_and_set_game(data_json):
    room_name = data_json.get("room_name", None)
    side = data_json.get("side", None)
    row = data_json.get("row", None)
    player = data_json.get("player", None)
    row_condition = row >= 0
    if all([room_name, row_condition, side, player]):
        game = get_room(room_name)
        is_possible = game.set_move(row, side, player)
        if is_possible:
            for col, value in enumerate(game.board[row]):
                if value != "":
                    game.check_win_movement(row, col)
                    if game.winner:
                        break
        room_data = build_room_data(game)
        return room_data
    else:
        logging.info("Missing args")


def update_all_screem(room_data):
    room_name = room_data["room_name"]
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        f"room_{room_name}",
        {"type": "update_board", "message": room_data},
    )


def build_room_data(game):
    room_data = {
        "board": game.board,
        "room_name": game.room_name,
        "player": game.turn,
        "max_movements": game.number_of_movements >= MAX_MOVEMENTS,
        "winner": game.winner,
    }
    return room_data
