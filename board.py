import settings as s
from fleet import Fleet


def field_head_bottom_row(char=' ', ind=False):
    for col in range(s.GRID_SIZE + 1):
        print((str(col) if ind else char) if col > 0 else ' ' * 3, end=' ')


def field_left(row):
    print(' ' + str(row + 1), end=' |')


def field_right():
    print('', end='|')


def field_inner(fleet: Fleet, row: int):
    for col in range(s.GRID_SIZE):
        print_val = 0
        if (row, col) in fleet.shots:
            print_val = 1
        for ship in fleet.ships:
            if (row, col) in ship.body:
                if not (fleet.hidden and not ship.body[(row, col)]):
                    print_val = ship.body[(row, col)] + 2
                break
        end_char = ' ' if col < s.GRID_SIZE - 1 else ''
        print(s.SYMBOLS[print_val], end=end_char)


def board_divider():
    print('   ★  ', end='')


class Board:
    """Contains game board with two grids and displays it"""

    def __init__(self, pl_fleet: Fleet, ai_fleet: Fleet) -> None:
        self.pl_grid = pl_fleet
        self.ai_grid = ai_fleet

    def show(self):

        print()

        field_head_bottom_row(ind=True)
        board_divider()
        field_head_bottom_row(ind=True)
        print()

        field_head_bottom_row('─')
        board_divider()
        field_head_bottom_row('─')
        print()

        for row in range(s.GRID_SIZE):
            field_left(row)
            field_inner(self.pl_grid, row)
            field_right()
            board_divider()
            field_left(row)
            field_inner(self.ai_grid, row)
            field_right()
            print()

        field_head_bottom_row('─')
        board_divider()
        field_head_bottom_row('─')
        print()
