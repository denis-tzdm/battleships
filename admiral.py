import random as rnd

import settings as s
from exceptions import *
from fleet import Fleet


class Admiral:
    """Representation of a player and it's actions"""

    fleet: Fleet  # enemy fleet, against which the shots will be processed
    name: str
    ai: bool

    def __init__(self, name: str) -> None:
        self.name = name
        self.setup_fleet()

    def setup_fleet(self):
        while True:
            try:
                self.fleet = Fleet(not self.ai)  # hide ai fleet from player
                self.fleet.add_random_ships()
                break
            except IndexError:
                pass  # there are non-possible field configurations, repeat

    def fire(self) -> tuple[int, int] | None:
        return None


class AIAdmiral(Admiral):
    """AI player"""

    ai: bool = True

    def fire(self) -> tuple[int, int]:
        # to-do: sequential AI shot logic
        shots_left = self.fleet.cells.difference(set(self.fleet.shots))
        return rnd.choice(list(shots_left))


class HumanAdmiral(Admiral):
    """Human player"""

    ai: bool = False

    def fire(self) -> tuple[int, int]:
        while True:
            try:
                input_str = input(f'\nEnter position as "x y" to fire your guns or '
                                  f'"{s.STOP_COMMAND}" to stop the game: ')
                return self.validate_input(input_str)
            except BadInput:
                pass

    def validate_input(self, input_str: str) -> tuple[int, int]:
        # stop command
        if input_str == s.STOP_COMMAND:
            raise GameBreak
        pos_list = input_str.split()
        # other than 2 values
        if len(pos_list) != 2:
            raise NotTwoArguments
        # other than 2 integers
        if not all(map(str.isdigit, pos_list)):
            raise NonIntegers
        col, row = map(lambda x: int(x) - 1, pos_list)
        # out of field
        if not all(map(lambda x: 0 <= x <= s.GRID_SIZE - 1, [col, row])):
            raise OutOfBoard
        # already fired there
        if (row, col) in self.fleet.shots:
            raise SamePos

        return row, col
