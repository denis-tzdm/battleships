GRID_SIZE = 6
SYMBOLS = {0: ' ', 1: '⨯', 2: '⊗', 3: '◻', 4: '◼'}
# 0: unhit cell, 1: hit cell, 2: ship's dead zone,
# 3: unhit ship block, 4: hit ship block
SHIP_TYPES = {3: 1, 2: 2, 1: 4}  # {size: count}
STOP_COMMAND = 'stop'
PLAYER_NAMES = {0: 'Player', 1: 'AI'}
