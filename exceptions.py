class GameBreak(Exception):
    pass


class GameOver(Exception):
    pass


class BadInput(Exception):
    pass


class OutOfBoard(BadInput):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        print('Fire position out of board range!')


class SamePos(BadInput):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        print('Already fired there!')


class NotTwoArguments(BadInput):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        print('Enter two space-separated coordinates!')


class NonIntegers(BadInput):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        print('Enter two space separated coordinates (integers)!')
