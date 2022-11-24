from elements import *


class Game:
    """Game controller"""

    admiral: Admiral  # current Admiral

    def __init__(self) -> None:
        self.admirals = [HumanAdmiral(s.PLAYER_NAMES[0]),
                         AIAdmiral(s.PLAYER_NAMES[1])]
        self.board = Interface(self.admirals[1].sea,
                               self.admirals[0].sea)
        self.current_admiral = rnd.randint(0, 1)  # 0 - player, 1 - AI
        self.shot_message = ''
        self.turn_counter = 0
        print(f"\n{'Welcome onboard, Admiral!':^40}")

    def turn(self):
        self.turn_counter += 1
        print(f'\n{f" ★  Turn {self.turn_counter}  ★ ":─^40}')
        self.admiral = self.admirals[self.current_admiral]
        if self.admiral.ai:  # AI turn: first fire, then show result
            shot = self.admiral.fire()
            self.process_shot(shot)
            print(self.board)
            print(self.shot_message)
        else:  # player's turn: first show board, then fire
            print(self.board)
            shot = self.admiral.fire()
            self.process_shot(shot)
            print(self.shot_message)

    def process_shot(self, shot: Cell) -> None:
        self.shot_message = (f'\n{self.admiral.name} fires'
                             f' {shot.col + 1}, {shot.row + 1}.')
        hit: Ship | None = self.admiral.hit(shot)
        if hit:
            self.shot_message += '\nHit!'
            if hit.sunk:
                self.shot_message += ' The ship sinks!'
                if self.admiral.sea.sunk:
                    raise GameOver(f'{self.admiral.name} wins!')
        else:
            self.shot_message += '\nMiss.'
            self.current_admiral = not self.current_admiral


class Interface:
    """Contains game board with two grids and displays it"""

    _board: str  # current board state to show

    def __init__(self, pl_sea: Sea, ai_sea: Sea) -> None:
        self.pl_grid = pl_sea
        self.ai_grid = ai_sea

    def __str__(self) -> str:

        self._board = '\n'

        self.field_head_bottom(ind=True)
        self.board_divider()
        self.field_head_bottom(ind=True)
        self._board += '\n'

        self.field_head_bottom('─')
        self.board_divider()
        self.field_head_bottom('─')
        self._board += '\n'

        for row in range(s.GRID_SIZE):
            self.field_left(row)
            self.field_inner(self.pl_grid, row)
            self.field_right()
            self.board_divider()
            self.field_left(row)
            self.field_inner(self.ai_grid, row)
            self.field_right()
            self._board += '\n'

        self.field_head_bottom('─')
        self.board_divider()
        self.field_head_bottom('─')
        self._board += '\n'

        return self._board

    def field_head_bottom(self, char: str = ' ', ind: bool = False) -> None:
        for col in range(s.GRID_SIZE + 1):
            self._board += (str(col) if ind else char) if col > 0 else ' ' * 3
            self._board += ' '

    def field_left(self, row: int) -> None:
        self._board += ' ' + str(row + 1) + ' |'

    def field_right(self) -> None:
        self._board += '|'

    def field_inner(self, sea: Sea, row: int) -> None:
        for col in range(s.GRID_SIZE):
            print_val = 0
            cell = Cell(col, row)
            if sea.hidden and (cell in sea.dead_zones):
                print_val = 2
            if cell in sea.shots:
                print_val = 1
            for ship in sea.ships:
                if cell in ship.body:
                    if not (sea.hidden and not ship.body[cell]):
                        print_val = ship.body[cell] + 3
                    break
            end_char = ' ' if col < s.GRID_SIZE - 1 else ''
            self._board += s.SYMBOLS[print_val] + end_char

    def board_divider(self) -> None:
        self._board += '   ★  '
