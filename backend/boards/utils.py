import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from boards.constants import MAX_MOVEMENTS
from boards.models import Game


def get_or_create_room(room_name, channel_name):
    game, created = Game.objects.get_or_create(room_name=room_name)
    current_player = save_channel_name(game, channel_name)
    room_data = build_room_data(game)
    return room_data, current_player


def save_channel_name(game, channel_name):
    def save_o_channel(channel):
        player = "o"
        game.id_player_two = channel
        return player

    def save_x_turn(channel):
        player = "x"
        game.id_player_one = channel
        return player

    if game.id_player_one and not game.id_player_two:
        current_player = save_o_channel(channel_name)
    elif not game.id_player_one and not game.id_player_two:
        current_player = save_x_turn(channel_name)
    elif not game.id_player_one and not game.id_player_two:
        current_player = save_x_turn(channel_name)
    elif game.id_player_one and game.id_player_two:
        if game.turn == "x":
            current_player = save_x_turn(channel_name)
        elif game.turn == "o":
            current_player = save_o_channel(channel_name)
    game.save()
    return current_player


def get_room(room_name):
    try:
        game = Game.objects.get(room_name=room_name)
        return game
    except Game.DoesNotExist as error:
        logging.info(f"Game not found: {error}")


def get_room_and_set_game(data_json, channel_name):
    room_name = data_json.get("room_name", None)
    side = data_json.get("side", None)
    row = data_json.get("row", None)
    player = data_json.get("player", None)
    row_condition = row >= 0
    if all([room_name, row_condition, side, player]):
        game = get_room(room_name)
        is_x_turn = game.turn == "x" and game.id_player_one == channel_name
        is_o_turn = game.turn == "o" and game.id_player_two == channel_name
        if is_x_turn or is_o_turn:
            is_possible = game.set_move(row, side, player)
            if is_possible:
                for col, value in enumerate(game.board[row]):
                    if value != "":
                        game.check_win_movement(row, col)
                        if game.winner:
                            break
            room_data = build_room_data(game)
            return room_data, True
        else:
            return None, False
    else:
        logging.info("Missing args")


def update_all_screem(room_data):
    room_name = room_data["room_name"]
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        f"room_{room_name}_x",
        {"type": "update_board", "message": room_data},
    )
    async_to_sync(layer.group_send)(
        f"room_{room_name}_o",
        {"type": "update_board", "message": room_data},
    )


def update_message_turn(room_data):
    room_name = room_data["room_name"]
    layer = get_channel_layer()
    turn = room_data["player"]
    if turn == "x":
        async_to_sync(layer.group_send)(
            f"room_{room_name}_x",
            {"type": "update_turn", "message_turn": "Is your turn (x)"},
        )
        async_to_sync(layer.group_send)(
            f"room_{room_name}_o",
            {"type": "update_turn", "message_turn": "Wait your turn"},
        )
    elif turn == "o":
        async_to_sync(layer.group_send)(
            f"room_{room_name}_x",
            {"type": "update_turn", "message_turn": "Wait your turn"},
        )
        async_to_sync(layer.group_send)(
            f"room_{room_name}_o",
            {"type": "update_turn", "message_turn": "Is your turn (o)"},
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
