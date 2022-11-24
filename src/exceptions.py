class GameBreak(Exception):
    pass


class GameOver(Exception):
    pass


class BadInput(Exception):
    pass


class OutOfBoardShot(BadInput):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        print('Fire position out of board range!')


class SamePosShot(BadInput):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        print('Already fired there!')


class DeadZoneShot(BadInput):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        print('It\'s a sunk ship zone, nothing there!')


class NotTwoArguments(BadInput):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        print('Enter two space-separated coordinates ("x y")!')


class NonIntegers(BadInput):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        print('Enter two space-separated coordinates (integers) '
              'without quotes!')
