from exceptions import GameOver, GameBreak
from games import Game


def main():
    game = Game()
    while True:
        try:
            game.turn()
        except GameOver as e:
            print(game.board)
            print(game.shot_message)
            print(f'Game over: {e.args[0]}')
            break
        except GameBreak:
            print('Game stopped.')
            break


if __name__ == '__main__':
    main()
