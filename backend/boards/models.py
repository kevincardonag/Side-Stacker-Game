import functools
import operator

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import COLUMN_SIZE, ROW_SIZE, NUMBER_TO_WIN, PLAYERS


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

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.board = [
                ["" for _column in range(0, COLUMN_SIZE + 1)]
                for _row in range(0, ROW_SIZE + 1)
            ]
            self.turn = "x"
        super().save(*args, **kwargs)

    def set_move(self, row, column, player):
        position = self.board[row][column]
        if position == "":
            self.board[row][column] = player
            self.turn = "o" if player == "x" else "x"
            self.save()
            return True
        else:
            return False

    def check_matriz_limits(
        self,
        row,
        column,
    ):
        return COLUMN_SIZE >= column >= 0 and ROW_SIZE >= row >= 0

    def check_forward_positions(self, row, column, player, position):
        if position == "forward":
            operation = operator.add
        elif position == "back":
            operation = operator.sub
        limit_conditions = self.check_matriz_limits(row, column)
        if limit_conditions and ROW_SIZE >= operation(column, (NUMBER_TO_WIN - 1)) <= 0:
            values = [self.board[row][column]]
            for new_column in range(1, NUMBER_TO_WIN):
                new_position = operation(column, new_column)
                position_value = self.board[row][new_position]
                values.append(position_value)
            # If all are the same win the game
            return values.count(player) == len(values)
        else:
            return False

    def check_up_and_down_positions(self, row, column, player, position):
        if position == "up":
            operation = operator.add
        elif position == "down":
            operation = operator.sub
        limit_conditions = self.check_matriz_limits(row, column)
        if limit_conditions and ROW_SIZE >= operation(row, (NUMBER_TO_WIN - 1)) <= 0:
            values = [self.board[row][column]]
            for new_row in range(1, NUMBER_TO_WIN):
                new_position = operation(row, new_row)
                position_value = self.board[new_position][column]
                values.append(position_value)
            # If all are the same win the game
            return values.count(player) == len(values)
        else:
            return False

    def check_main_diagonal_forward(self, row, column, player, position):
        if position == "up":
            operation = operator.add
        elif position == "down":
            operation = operator.sub
        limit_conditions = self.check_matriz_limits(row, column)
        if (
            limit_conditions
            and operation(column, (NUMBER_TO_WIN - 1)) <= ROW_SIZE
            and operation(row, (NUMBER_TO_WIN - 1)) <= ROW_SIZE
        ):
            values = [self.board[row][column]]
            for new_position in range(1, NUMBER_TO_WIN):
                new_row = operation(row, new_position)
                new_colunm = operation(column, new_position)
                position_value = self.board[new_row][new_colunm]
                values.append(position_value)
            # If all are the same win the game
            return values.count(player) == len(values)
        else:
            return False

    def check_main_diagonal_back_down(self, row, column, player):
        limit_conditions = self.check_matriz_limits(row, column)
        if (
            limit_conditions
            and (row + (NUMBER_TO_WIN - 1)) <= ROW_SIZE
            and (column - (NUMBER_TO_WIN - 1)) <= ROW_SIZE
        ):
            values = [self.board[row][column]]
            for new_position in range(1, NUMBER_TO_WIN):
                new_row = row + new_position
                new_column = column - new_position
                position_value = self.board[new_row][new_column]
                values.append(position_value)
            # If all are the same win the game
            return values.count(player) == len(values)
        else:
            return False

    def check_main_diagonal_back_up(self, row, column, player):
        limit_conditions = self.check_matriz_limits(row, column)
        if (
            limit_conditions
            and (row - (NUMBER_TO_WIN - 1)) <= ROW_SIZE
            and (column + (NUMBER_TO_WIN - 1)) <= ROW_SIZE
        ):
            values = [self.board[row][column]]
            for new_position in range(1, NUMBER_TO_WIN):
                new_row = row - new_position
                new_column = column + new_position
                position_value = self.board[new_row][new_column]
                values.append(position_value)
            # If all are the same win the game
            return values.count(player) == len(values)
        else:
            return False
