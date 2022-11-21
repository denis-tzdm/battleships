class Ship:
    """Describes a ship and manages its state"""
    
    sunk: bool  # the ship is sunk
    body: dict[tuple[int, int], int]
    # ship's body, a dict of block positions and states {(row, column): state}
    # where state = 1 when the block is hit or 0 otherwise
    zone: list[tuple[int, int]]
    # ship's dead zone: it's blocks and one block around

    def __init__(self, size: int, pos: tuple[int, int], lay: int) -> None:
        # size - int - ship size in blocks
        # pos - tuple - ship's first block coordinates (row, column)
        # lay - int - ship layout: 0 - horizontal, 1 - vertical
        self.size = size
        self.pos = pos
        self.lay = lay
        self.sunk = False
        self.body = {_: 0 for _ in self.blocks()}
        self.zone = self.define_zone()

    def blocks(self) -> list[tuple[int, int]]:
        """All blocks of a ship"""

        if self.lay:
            pos_list = [(self.pos[0] + ind, self.pos[1])
                        for ind in range(self.size)]
        else:
            pos_list = [(self.pos[0], self.pos[1] + ind)
                        for ind in range(self.size)]
        return pos_list

    def define_zone(self) -> list[tuple[int, int]]:
        """All blocks of a ship itself and it's dead zone"""

        if self.lay:
            pos_list = [(self.pos[0] + ind, self.pos[1])
                        for ind in range(-1, self.size + 1)]
            pos_list.extend((self.pos[0] + ind, self.pos[1] - 1)
                            for ind in range(-1, self.size + 1))
            pos_list.extend((self.pos[0] + ind, self.pos[1] + 1)
                            for ind in range(-1, self.size + 1))
        else:
            pos_list = [(self.pos[0], self.pos[1] + ind)
                        for ind in range(-1, self.size + 1)]
            pos_list.extend((self.pos[0] - 1, self.pos[1] + ind)
                            for ind in range(-1, self.size + 1))
            pos_list.extend((self.pos[0] + 1, self.pos[1] + ind)
                            for ind in range(-1, self.size + 1))
        return pos_list

    def hit(self, hit_pos: tuple[int, int]) -> bool:
        """If a shot was a hit"""

        if hit_pos in self.body:
            self.body[hit_pos] = 1
            self.sunk = all(v for _, v in self.body.items())
            return True
        return False
