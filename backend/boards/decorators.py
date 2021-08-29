from boards.constants import COLUMN_SIZE, ROW_SIZE


def check_limits(func):
    def inner(*args, **kwargs):
        column = args[2]
        row = args[1]
        if COLUMN_SIZE >= column >= 0 and ROW_SIZE >= row >= 0:
            return func(*args, **kwargs)
        else:
            pass

    return inner
