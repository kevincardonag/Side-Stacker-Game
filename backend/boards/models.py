import functools
import operator

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import COLUMN_SIZE, ROW_SIZE, NUMBER_TO_WIN, PLAYERS
from .decorators import check_limits


class Game(models.Model):
    room_name = models.CharField(
        verbose_name=_("Room name"), blank=False, null=False, max_length=255
    )
    turn = models.CharField(
        verbose_name=_("Game turn"),
        blank=False,
        null=False,
        max_length=255,
        choices=PLAYERS,
    )
    board = ArrayField(
        ArrayField(
            models.CharField(max_length=10, blank=True, null=True),
            size=ROW_SIZE,
        ),
        size=COLUMN_SIZE,
        blank=True,
    )
    winner = models.CharField(
        verbose_name=_("Winner"), blank=True, null=True, max_length=10
    )
    number_of_movements = models.IntegerField(
        verbose_name=_("Number of movements"), default=0
    )
    id_player_one = models.CharField(
        verbose_name=_("Id channel player 1"), blank=True, null=True, max_length=255
    )
    id_player_two = models.CharField(
        verbose_name=_("Id channel player 1"), blank=True, null=True, max_length=255
    )

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.board = [
                ["" for _column in range(0, COLUMN_SIZE + 1)]
                for _row in range(0, ROW_SIZE + 1)
            ]
            self.turn = "x"
        super().save(*args, **kwargs)

    def set_move(self, row, side, player):
        try:
            space_available = sum(_value != "" for _value in self.board[row])
            if space_available != 7:
                if side == "R":
                    copy_row = self.board[row]
                elif side == "L":
                    copy_row = self.board[row][::-1]

                for index in range(0, COLUMN_SIZE):
                    value = copy_row[index]
                    if value == "":
                        del copy_row[index]
                        copy_row.append(player)
                        break

                if side == "R":
                    self.board[row] = copy_row
                elif side == "L":
                    self.board[row] = copy_row[::-1]
                self.turn = "o" if player == "x" else "x"
                self.number_of_movements = self.number_of_movements + 1
                self.save()
                return True
            else:
                return False
        except IndexError:
            return False

    @check_limits
    def check_forward_positions(self, row, column, position):
        if position == "forward":
            operation = operator.add
        elif position == "back":
            operation = operator.sub
        if COLUMN_SIZE >= operation(column, (NUMBER_TO_WIN - 1)) >= 0:
            values = [self.board[row][column]]
            for new_column in range(1, NUMBER_TO_WIN):
                new_position = operation(column, new_column)
                position_value = self.board[row][new_position]
                values.append(position_value)
            won = self.check_win(values)
            return won
        else:
            return False

    @check_limits
    def check_up_and_down_positions(self, row, column, position):
        if position == "up":
            operation = operator.add
        elif position == "down":
            operation = operator.sub
        if ROW_SIZE >= operation(row, (NUMBER_TO_WIN - 1)) >= 0:
            values = [self.board[row][column]]
            for new_row in range(1, NUMBER_TO_WIN):
                new_position = operation(row, new_row)
                position_value = self.board[new_position][column]
                values.append(position_value)
            won = self.check_win(values)
            return won
        else:
            return False

    @check_limits
    def check_main_diagonal_forward(self, row, column, position):
        if position == "up":
            operation = operator.add
        elif position == "down":
            operation = operator.sub
        if (
            COLUMN_SIZE >= operation(column, (NUMBER_TO_WIN - 1)) >= 0
            and ROW_SIZE >= operation(row, (NUMBER_TO_WIN - 1)) >= 0
        ):
            values = [self.board[row][column]]
            for new_position in range(1, NUMBER_TO_WIN):
                new_row = operation(row, new_position)
                new_colunm = operation(column, new_position)
                position_value = self.board[new_row][new_colunm]
                values.append(position_value)
            won = self.check_win(values)
            return won
        else:
            return False

    @check_limits
    def check_main_diagonal_back_down(self, row, column):
        if (
            ROW_SIZE >= (row + (NUMBER_TO_WIN - 1)) >= 0
            and COLUMN_SIZE >= (column - (NUMBER_TO_WIN - 1)) >= 0
        ):
            values = [self.board[row][column]]
            for new_position in range(1, NUMBER_TO_WIN):
                new_row = row + new_position
                new_column = column - new_position
                position_value = self.board[new_row][new_column]
                values.append(position_value)
            won = self.check_win(values)
            return won
        else:
            return False

    @check_limits
    def check_main_diagonal_back_up(self, row, column):
        if (
            ROW_SIZE >= (row - (NUMBER_TO_WIN - 1)) >= 0
            and COLUMN_SIZE >= (column + (NUMBER_TO_WIN - 1)) >= 0
        ):
            values = [self.board[row][column]]
            for new_position in range(1, NUMBER_TO_WIN):
                new_row = row - new_position
                new_column = column + new_position
                position_value = self.board[new_row][new_column]
                values.append(position_value)
            won = self.check_win(values)
            return won
        else:
            return False

    def check_win_movement(self, row, col):
        self.check_win_from_position(row, col)
        self.check_win_from_position(row + 1, col)
        self.check_win_from_position(row, col + 1)
        self.check_win_from_position(row - 1, col)
        self.check_win_from_position(row, col - 1)
        self.check_win_from_position(row + 1, col + 1)
        self.check_win_from_position(row - 1, col - 1)
        self.check_win_from_position(row + 1, col - 1)
        self.check_win_from_position(row - 1, col + 1)

    def check_win_from_position(self, row, col):
        self.check_forward_positions(row, col, "forward")
        self.check_forward_positions(row, col, "back")
        self.check_up_and_down_positions(row, col, "up")
        self.check_up_and_down_positions(row, col, "down")
        self.check_main_diagonal_forward(row, col, "up")
        self.check_main_diagonal_forward(row, col, "down")
        self.check_main_diagonal_back_down(row, col)
        self.check_main_diagonal_back_up(row, col)

    def check_win(self, values):
        player_x = PLAYERS[0][0]
        player_o = PLAYERS[1][0]
        # If all are the same win the game
        player_x_won = values.count(player_x) == len(values)
        if player_x_won:
            self.winner = player_x
            self.save()
            return player_x_won
        player_o_won = values.count(player_o) == len(values)
        if player_o_won:
            self.winner = player_o
            self.save()
            return player_o_won
        return False
