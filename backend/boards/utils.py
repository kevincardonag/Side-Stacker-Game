from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from boards.models import Game


def get_or_create_room(room_name):
    game, created = Game.objects.get_or_create(room_name=room_name)
    room_data = {
        "board": game.board,
        "player": game.winner if game.winner else game.turn,
        "room_name": room_name,
        "win": True if game.winner else False,
    }
    return room_data


def get_room_and_set_game(data_json):
    room_name = data_json.get("room_name", None)
    col = data_json.get("col", None)
    row = data_json.get("row", None)
    player = data_json.get("player", None)
    col_condition = col >= 0
    row_condition = row >= 0
    if all([room_name, col_condition, row_condition, player]):
        try:
            game = Game.objects.get(room_name=room_name)
            is_possible = game.set_move(row, col, player)
            if is_possible:
                win_conditios = []
                win_conditios.extend(check_win_from_position(game, row, col, player))
                win_conditios.extend(
                    check_win_from_position(game, row + 1, col, player)
                )
                win_conditios.extend(
                    check_win_from_position(game, row, col + 1, player)
                )
                win_conditios.extend(
                    check_win_from_position(game, row - 1, col, player)
                )
                win_conditios.extend(
                    check_win_from_position(game, row, col - 1, player)
                )
                win_conditios.extend(
                    check_win_from_position(game, row + 1, col + 1, player)
                )
                win_conditios.extend(
                    check_win_from_position(game, row - 1, col - 1, player)
                )
                win_conditios.extend(
                    check_win_from_position(game, row + 1, col - 1, player)
                )
                win_conditios.extend(
                    check_win_from_position(game, row - 1, col + 1, player)
                )
                there_is_winner = any(win_conditios)
                if there_is_winner:
                    game.winner = player
                    game.save()
                room_data = {
                    "board": game.board,
                    "room_name": room_name,
                    "win": there_is_winner,
                    "player": game.winner if game.winner else game.turn,
                }
                return room_data
            else:
                pass
        except Game.DoesNotExist:
            pass
    else:
        pass


def update_all_screem(room_data):
    room_name = room_data["room_name"]
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        f"room_{room_name}",
        {"type": "update_board", "message": room_data},
    )


def check_win_from_position(game, row, col, player):
    win_forward = game.check_forward_positions(row, col, player, "forward")
    win_back = game.check_forward_positions(row, col, player, "back")
    win_up = game.check_up_and_down_positions(row, col, player, "up")
    win_down = game.check_up_and_down_positions(row, col, player, "down")
    win_diagonal_forward_up = game.check_main_diagonal_forward(row, col, player, "up")
    win_diagonal_forward_dowm = game.check_main_diagonal_forward(
        row, col, player, "down"
    )
    win_main_diagonal_back_down = game.check_main_diagonal_back_down(row, col, player)
    win_main_diagonal_back_up = game.check_main_diagonal_back_up(row, col, player)
    win_conditions = [
        win_forward,
        win_back,
        win_up,
        win_down,
        win_diagonal_forward_up,
        win_diagonal_forward_dowm,
        win_main_diagonal_back_down,
        win_main_diagonal_back_up,
    ]
    return win_conditions
