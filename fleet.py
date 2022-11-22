import random as rnd

import settings as s
from ship import Ship


class Fleet:
    """Contains field and ships for one player
    and manages ship addition and hit processing"""

    ships: list[Ship]  # list of ship objects
    cells: set[tuple[int, int]]  # set of all cells (row, column)
    free_cells: set[tuple[int, int]]
    # set of free cells (row, column) for ship positioning
    shots: list[tuple[int, int]]  # list of moves
    zones: list[tuple[int, int]]  # list of dead zones for AI
    hidden: bool  # to hide AI ships from player
    sunk: bool  # oh, no!

    def __init__(self, hidden: bool) -> None:
        self._size = s.GRID_SIZE
        self.cells = set((row, col) for col in range(self._size)
                         for row in range(self._size))
        self.ships = []
        self.shots = []
        self.zones = []
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
            pos = rnd.choice(list(self.free_cells.difference(tested_cells)))
            lay = rnd.randint(0, 1)
            if self.add_ship(Ship(size, pos, lay)) or \
               self.add_ship(Ship(size, pos, not lay)):
                break
            else:
                tested_cells.add(pos)

    def add_ship(self, ship: Ship) -> bool:
        # check field borders
        if not all(pos[0] <= self._size - 1 and pos[1] <= self._size - 1
                   for pos, _ in ship.body.items()):
            return False
        # check other ships
        for a_ship in self.ships:
            if any(pos in a_ship.zone for pos, _ in ship.body.items()):
                return False
        self.ships.append(ship)
        self.free_cells = self.free_cells.difference(set(ship.blocks()))
        return True

    def hit(self, pos: tuple[int, int]) -> Ship | None:
        self.shots.append(pos)
        for ship in self.ships:
            if ship.hit(pos):
                self.sunk = all(a.sunk for a in self.ships)
                return ship
        return None

    def add_zone(self, zone: list[tuple[int, int]]) -> None:
        self.zones.extend(zone)
