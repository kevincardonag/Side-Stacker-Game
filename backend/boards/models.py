import operator

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import COLUMN_SIZE, ROW_SIZE, NUMBER_TO_WIN


class Game(models.Model):
    room_name = models.CharField(verbose_name=_("Room name"), blank=False, null=False, max_length=255)
    board = ArrayField(
        ArrayField(
            models.CharField(max_length=10, blank=True, null=True),
            size=ROW_SIZE - 1,
        ),
        size=COLUMN_SIZE - 1,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.board:
            self.board = [[None for _column in range(0, COLUMN_SIZE)] for _row in range(0, ROW_SIZE)]
        super().save(*args, **kwargs)

    def set_move(self, column, row, player):
        position = self.board[row][column]
        if position is None:
            self.board[row][column] = player
            self.save()
        else:
            pass

    def check_forward_positions(self, column, row, player, position):
        if position == "forward":
            operation = operator.add()
        elif position == "back":
            operation = operator.sub()

        if operation(row, (NUMBER_TO_WIN - 1)) <= ROW_SIZE:
            values = []
            values.append(self.board[row][column])
            for new_column in range(1, NUMBER_TO_WIN):
                position_value = self.board[row][operation(column, new_column)]
                values.append(position_value)
            # If all are the same win the game
            return values.count(player) == len(values)
        else:
            return False

    # def check_back_positions(self, column, row, player):
    #     if row - (NUMBER_TO_WIN - 1) >= COLUMN_SIZE:
    #         values = []
    #         values.append(self.board[row][column])
    #         for new_column in range(1, NUMBER_TO_WIN):
    #             position_value = self.board[row][column - new_column]
    #             values.append(position_value)
    #         # If all are the same win the game
    #         return values.count(player) == len(values)
    #     else:
    #         return False
