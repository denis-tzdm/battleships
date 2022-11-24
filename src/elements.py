import random as rnd

import settings as s
from exceptions import *


class Cell:
    """A cell of a field"""

    _col: int  # block's x
    _row: int  # block's y

    def __init__(self, col: int, row: int) -> None:
        self._col = col
        self._row = row

    def __eq__(self, other) -> bool:
        return isinstance(other, Cell) \
               and self._col == other._col \
               and self._row == other._row

    def __hash__(self):  # we will use Cell in set and dict
        return hash(str(self._col) + str(self._row))

    # col and row should not change so Cell should remain immutable
    @property
    def col(self):
        return self._col

    @property
    def row(self):
        return self._row


class Ship:
    """Describes a ship and manages its state"""

    sunk: bool  # the ship is sunk
    body: dict[Cell, int]
    # ship's body, a dict of block positions and states {(row, column): state}
    # where state = 1 when the block is hit or 0 otherwise
    zone: list[Cell]

    # ship's dead zone: it's blocks and one block around

    def __init__(self, size: int, pos: Cell, lay: int) -> None:
        # size - int - ship size in blocks
        # pos - tuple - ship's first block coordinates (row, column)
        # lay - int - ship layout: 0 - horizontal, 1 - vertical
        self.size = size
        self.pos = pos
        self.lay = lay
        self.sunk = False
        self.body = {_: 0 for _ in self.blocks()}
        self.zone = self.define_zone()

    def blocks(self) -> list[Cell]:
        """All blocks of a ship"""

        if self.lay:
            cell_list = [Cell(self.pos.col + ind, self.pos.row)
                         for ind in range(self.size)]
        else:
            cell_list = [Cell(self.pos.col, self.pos.row + ind)
                         for ind in range(self.size)]
        return cell_list

    def define_zone(self) -> list[Cell]:
        """All blocks of a ship itself and it's dead zone"""

        if self.lay:
            pos_list = [Cell(self.pos.col + ind, self.pos.row)
                        for ind in range(-1, self.size + 1)]
            pos_list.extend(Cell(self.pos.col + ind, self.pos.row - 1)
                            for ind in range(-1, self.size + 1))
            pos_list.extend(Cell(self.pos.col + ind, self.pos.row + 1)
                            for ind in range(-1, self.size + 1))
        else:
            pos_list = [Cell(self.pos.col, self.pos.row + ind)
                        for ind in range(-1, self.size + 1)]
            pos_list.extend(Cell(self.pos.col - 1, self.pos.row + ind)
                            for ind in range(-1, self.size + 1))
            pos_list.extend(Cell(self.pos.col + 1, self.pos.row + ind)
                            for ind in range(-1, self.size + 1))
        return pos_list

    def hit(self, cell: Cell) -> bool:
        """If a shot was a hit"""

        if cell in self.body:
            self.body[cell] = 1
            self.sunk = all(state for _, state in self.body.items())
            return True
        return False


class Sea:
    """Contains field and ships for one player
    and manages ship addition and hit processing"""

    ships: list[Ship]  # list of ship objects
    cells: set[Cell]  # set of all cells (row, column)
    free_cells: set[Cell]
    # set of free cells (row, column) for ship positioning
    shots: list[Cell]  # list of moves
    dead_zones: list[Cell]  # list of dead zones
    hidden: bool  # to hide AI ships from player
    sunk: bool  # oh, no!

    def __init__(self, hidden: bool) -> None:
        self._size = s.GRID_SIZE
        self.cells = set(Cell(col, row) for col in range(self._size)
                         for row in range(self._size))
        self.ships = []
        self.shots = []
        self.dead_zones = []
        self.free_cells = self.cells
        self.hidden = hidden

    def add_random_ships(self) -> None:
        for ship_type, ship_count in s.SHIP_TYPES.items():
            for _ in range(ship_count):
                self.add_random_ship(ship_type)

    def add_random_ship(self, size: int) -> None:
        tested_cells = set()
        while True:
            # choose only those cells we haven't tried yet
            cell = rnd.choice(list(self.free_cells.difference(tested_cells)))
            lay = rnd.randint(0, 1)
            if self.add_ship(Ship(size, cell, lay)) or \
                    self.add_ship(Ship(size, cell, not lay)):
                break
            else:
                tested_cells.add(cell)

    def add_ship(self, ship: Ship) -> bool:
        # check field borders
        if not all(cell.col <= self._size - 1 and cell.row <= self._size - 1
                   for cell, _ in ship.body.items()):
            return False
        # check other ships
        for a_ship in self.ships:
            if any(cell in a_ship.zone for cell, _ in ship.body.items()):
                return False
        self.ships.append(ship)
        self.free_cells = self.free_cells.difference(set(ship.blocks()))
        return True

    def hit(self, cell: Cell) -> Ship | None:
        self.shots.append(cell)
        for ship in self.ships:
            if ship.hit(cell):
                self.sunk = all(a.sunk for a in self.ships)
                return ship
        return None

    def add_zone(self, zone: list[Cell]) -> None:
        self.dead_zones.extend(zone)


class Admiral:
    """Representation of a player and it's actions"""

    sea: Sea  # enemy sea, against which the shots will be processed
    name: str
    ai: bool

    def __init__(self, name: str) -> None:
        self.name = name
        self.setup_fleet()

    def setup_fleet(self):
        while True:
            try:
                self.sea = Sea(not self.ai)  # hide ai fleet from player
                self.sea.add_random_ships()
                break
            except IndexError:
                pass  # there are non-possible field configurations, repeat

    def fire(self) -> Cell:
        pass

    def hit(self, pos: Cell) -> Ship | None:
        hit: Ship = self.sea.hit(pos)
        # no point in firing sunk ship's dead zone
        # so add it to dead zones list
        if hit and hit.sunk:
            self.sea.add_zone(hit.zone)
        return hit


class AIAdmiral(Admiral):
    """AI player"""

    ai: bool = True

    def fire(self) -> Cell:
        # to-do: sequential AI shot logic
        useless_shots = set(self.sea.shots + self.sea.dead_zones)
        shots_left = self.sea.cells.difference(useless_shots)

        return rnd.choice(list(shots_left))


class HumanAdmiral(Admiral):
    """Human player"""

    ai: bool = False

    def fire(self) -> Cell:
        while True:
            try:
                input_str = input(f'\nEnter position as "x y" to fire your guns or '
                                  f'"{s.STOP_COMMAND}" to stop the game: ')
                return self.validate_input(input_str)
            except BadInput:
                pass

    def validate_input(self, input_str: str) -> Cell:
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
        shot = Cell(col, row)
        # out of field
        if shot not in self.sea.cells:
            raise OutOfBoardShot
        # already fired there
        if shot in self.sea.shots:
            raise SamePosShot
        # dead zone of a sunk ship
        if shot in self.sea.dead_zones:
            raise DeadZoneShot

        return shot
