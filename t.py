self.time_left = time_left

# Initialize the best move so that this function returns something
# in case the search fails due to timeout
legal_moves = game.get_legal_moves(self)
if len(legal_moves) > 0:
    best_move = legal_moves[randint(0, len(legal_moves)-1)]
else:
    best_move = (-1, -1)
try:
    # The try/except block will automatically catch the exception
    # raised when the timer is about to expire.
    depth = 1
    while True:
        current_move = self.alphabeta(game, depth)
        if current_move == (-1, -1):
            return best_move
        else:
            best_move = current_move
        depth += 1
except SearchTimeout:
    return best_move
return best_move
