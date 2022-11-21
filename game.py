from admiral import *
from board import Board
from ship import Ship


class Game:
    """Game controller"""

    admiral: Admiral  # current Admiral
    shot: tuple[int, int]  # current shot
    hit: Ship | None  # if current shot is a hit

    def __init__(self) -> None:
        self.admirals = [HumanAdmiral(s.PLAYER_NAMES[0]),
                         AIAdmiral(s.PLAYER_NAMES[1])]
        self.board = Board(self.admirals[1].fleet,
                           self.admirals[0].fleet)
        self.current_admiral = rnd.randint(0, 1)  # 0 - player, 1 - AI
        self.hit = None
        self.shot_message = ''
        self.turn_counter = 0
        print(f"\n{'Welcome onboard, Admiral!':^40}")

    def turn(self):
        self.turn_counter += 1
        print(f'\n{f"  Turn {self.turn_counter}  ":─^40}')
        self.admiral = self.admirals[self.current_admiral]
        if self.admiral.ai:  # AI turn: first fire, then show result
            self.shot = self.admiral.fire()
            self.process_shot()
            self.board.show()
            print(self.shot_message)
        else:  # player's turn: first show board, then fire
            self.board.show()
            self.shot = self.admiral.fire()
            self.process_shot()
            print(self.shot_message)

    def process_shot(self):
        pos = self.shot
        self.shot_message = (f'\n{self.admiral.name} fires'
                             f' {pos[1] + 1}, {pos[0] + 1}.')
        self.hit = self.admiral.fleet.hit(pos)
        if self.hit:
            self.shot_message += '\nHit!'
            if self.hit.sunk:
                self.shot_message += ' The ship sinks!'
                if self.admiral.fleet.sunk:
                    raise GameOver(f'{self.admiral.name} wins!')
        else:
            self.shot_message += '\nMiss.'
            self.current_admiral = not self.current_admiral
