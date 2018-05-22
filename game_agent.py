"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random as r

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def terminal_test(game):
    """
    Checks to see if the current player is out of moves.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    Returns
    -------
    boolean
        True if the current player is out of moves.
        False if the player has legal moves to chose from.
    """
    return not bool(game.get_legal_moves())


def timeout_check(self):
    """
    Checks to see if the TIMER_THRESHOLD has been reached.
    """
    if self.time_left() < self.TIMER_THRESHOLD:
        raise SearchTimeout()


def check_winner(game, player):
    """
    Return best score if move wins game.
    Return worst score if move loses game.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")


def heuristic_1(game, player):

    # useful attributes
    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    total = my_moves + opp_moves

    # to insure no division by 0
    if total == 0:
        total += 1

    # appreciating weight
    weight = 1/total

    # become more aggressive as the game goes on
    return float(my_moves - (weight * opp_moves))


def heuristic_2(game, player):

    # useful attributes
    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    mobility = my_moves
    relative_mobility = my_moves - opp_moves

    # linear combination score
    return float(mobility + relative_mobility)


def heuristic_3(game, player):

    # moves left for each player
    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    # consistently decrease opponents moves
    return float(my_moves - (1.5 * opp_moves))

"""
When I called the heuristics in order, now changed so that the most effective
heuristic_2 is called in custom_score.
AB_Custom(custom_score): heuristic_1
AB_Custom_2(custom_score_2): heuristic_2
AB_Custom_3(custom_score_3): heuristic_3

Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3
                        Won | Lost   Won | Lost   Won | Lost   Won | Lost
    1       Random      10  |   0    10  |   0     9  |   1    10  |   0
    2       MM_Open      6  |   4     7  |   3     8  |   2     6  |   4
    3      MM_Center     8  |   2    10  |   0    10  |   0    10  |   0
    4     MM_Improved    6  |   4     7  |   3     7  |   3     8  |   2
    5       AB_Open      4  |   6     6  |   4     5  |   5     4  |   6
    6      AB_Center     6  |   4     3  |   7     6  |   4     8  |   2
    7     AB_Improved    5  |   5     3  |   7     6  |   4     6  |   4
--------------------------------------------------------------------------
           Win Rate:      64.3%        65.7%        72.9%        74.3%

Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3
                        Won | Lost   Won | Lost   Won | Lost   Won | Lost
    1       Random       9  |   1    10  |   0    10  |   0    10  |   0
    2       MM_Open      9  |   1     6  |   4     9  |   1     5  |   5
    3      MM_Center     8  |   2     9  |   1     9  |   1     9  |   1
    4     MM_Improved    5  |   5     6  |   4     9  |   1     8  |   2
    5       AB_Open      6  |   4     6  |   4     3  |   7     4  |   6
    6      AB_Center     5  |   5     4  |   6     7  |   3     4  |   6
    7     AB_Improved    5  |   5     5  |   5     6  |   4     4  |   6
--------------------------------------------------------------------------
           Win Rate:      67.1%        65.7%        75.7%        62.9%

Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3
                        Won | Lost   Won | Lost   Won | Lost   Won | Lost
    1       Random      10  |   0     9  |   1    10  |   0    10  |   0
    2       MM_Open      7  |   3     6  |   4     7  |   3     7  |   3
    3      MM_Center     8  |   2     7  |   3    10  |   0     9  |   1
    4     MM_Improved    6  |   4     5  |   5     9  |   1     8  |   2
    5       AB_Open      4  |   6     3  |   7     5  |   5     6  |   4
    6      AB_Center     7  |   3     6  |   4     8  |   2     5  |   5
    7     AB_Improved    7  |   3     6  |   4     6  |   4     4  |   6
--------------------------------------------------------------------------
           Win Rate:      70.0%        60.0%        78.6%        70.0%

Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3
                        Won | Lost   Won | Lost   Won | Lost   Won | Lost
    1       Random      10  |   0     9  |   1    10  |   0    10  |   0
    2       MM_Open      8  |   2     8  |   2    10  |   0     9  |   1
    3      MM_Center     7  |   3     9  |   1    10  |   0    10  |   0
    4     MM_Improved    8  |   2     9  |   1     6  |   4     6  |   4
    5       AB_Open      4  |   6     4  |   6     7  |   3     4  |   6
    6      AB_Center     4  |   6     3  |   7     8  |   2     6  |   4
    7     AB_Improved    6  |   4     5  |   5     4  |   6     5  |   5
--------------------------------------------------------------------------
           Win Rate:      67.1%        67.1%        78.6%        71.4%



Linear combinations of heuristics:
AB_Custom: custom_score: heuristic_1(game, player) + heuristic_3(game, player)
AB_Custom_2: custom_score_2: 0.5*heuristic_2(game, player) + 0.15*heuristic_1(game, player) + 0.35*heuristic_3(game, player)
AB_Custom_3: custom_score_3: heuristic_1(game, player) + heuristic_2(game, player) + heuristic_3(game, player)

Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3
                        Won | Lost   Won | Lost   Won | Lost   Won | Lost
    1       Random       9  |   1     9  |   1    10  |   0    10  |   0
    2       MM_Open      9  |   1     8  |   2     8  |   2     8  |   2
    3      MM_Center    10  |   0    10  |   0     8  |   2     8  |   2
    4     MM_Improved    6  |   4     9  |   1     7  |   3     7  |   3
    5       AB_Open      5  |   5     5  |   5     5  |   5     6  |   4
    6      AB_Center     6  |   4     6  |   4     6  |   4     6  |   4
    7     AB_Improved    6  |   4     4  |   6     6  |   4     6  |   4
--------------------------------------------------------------------------
           Win Rate:      72.9%        72.9%        71.4%        72.9%

Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3
                        Won | Lost   Won | Lost   Won | Lost   Won | Lost
    1       Random       9  |   1    10  |   0    10  |   0    10  |   0
    2       MM_Open      7  |   3     7  |   3     7  |   3     8  |   2
    3      MM_Center     8  |   2     9  |   1    10  |   0     9  |   1
    4     MM_Improved    7  |   3     9  |   1     8  |   2    10  |   0
    5       AB_Open      6  |   4     4  |   6     5  |   5     4  |   6
    6      AB_Center     6  |   4     6  |   4     5  |   5     5  |   5
    7     AB_Improved    4  |   6     6  |   4     3  |   7     3  |   7
--------------------------------------------------------------------------
           Win Rate:      67.1%        72.9%        68.6%        70.0%
"""


def custom_score(game, player):
    """
    Appreciating weight on the number of moves the opponent has.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.

    Best Score
    ----------
    """
    check_winner(game, player)

    return heuristic_1(game, player)


def custom_score_2(game, player):
    """
    Linear combination.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    check_winner(game, player)

    return heuristic_2(game, player)


def custom_score_3(game, player):
    """
    Fixed weight to reward decreasing opponents moves.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    check_winner(game, player)

    return heuristic_3(game, player)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass

        # Return the best move from the last completed search iteration
        return best_move


    def max_value(self, game, depth):

        timeout_check(self)

        # recursive stack unwinds at depth of 0 or terminal_test
        if depth <= 0 or terminal_test(game):
            return self.score(game, self)

        value = float('-inf')

        # max in node, update depth
        for move in game.get_legal_moves():
            value = max(value, self.min_value(game.forecast_move(move), depth - 1))
        return value


    def min_value(self, game, depth):

        timeout_check(self)

        # recursive stack unwinds at depth of 0 or terminal_test
        if depth <= 0 or terminal_test(game):
            return self.score(game, self)

        value = float('inf')

        # min in node, update depth
        for move in game.get_legal_moves():
            value = min(value, self.max_value(game.forecast_move(move), depth - 1))
        return value


    def minimax(self, game, depth):
        """
        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        timeout_check(self)

        best_score = float('-inf')
        legal_moves = game.get_legal_moves()

        # no legal moves left
        if not legal_moves:
            return (-1, -1)
        # best move default (random legal move)
        best_move = legal_moves[r.randint(0, len(legal_moves) - 1)]

        # all possible actions contrained by depth
        for move in legal_moves:
            score = self.min_value(game.forecast_move(move), depth - 1)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left # update time left

        best_move = (-1, -1)

        # The try/except block will automatically catch the exception
        # raised when the timer is about to expire.
        try:
            search_depth = 0 # iterative deepening, start at 0
            while True:
                move = self.alphabeta(game, search_depth)
                if move == (-1, -1):
                    return best_move
                else:
                    best_move = move
                search_depth += 1 # increment until timeout

        except SearchTimeout:
            return best_move # return current best move on timeout

        # return the best move from the last completed search iteration
        return best_move

    def max_value(self, game, alpha, beta, depth):

        timeout_check(self)

        # recursive stack unwinds at depth of 0 or terminal_test
        if depth <= 0 or terminal_test(game):
            return self.score(game, self)

        value = float('-inf') # init max value

        # max in node, update depth/alpha
        for move in game.get_legal_moves():
            value = max(value, self.min_value(game.forecast_move(move), alpha, beta, depth - 1))
            if value >= beta: # check upper bound
                return value
            alpha = max(alpha, value) # update alpha
        return value


    def min_value(self, game, alpha, beta, depth):

        timeout_check(self)

        # recursive stack unwinds at depth of 0 or terminal_test
        if depth <= 0 or terminal_test(game):
            return self.score(game, self)

        value = float('inf') # init min value

        # min in node, update depth/beta
        for move in game.get_legal_moves():
            value = min(value, self.max_value(game.forecast_move(move), alpha, beta, depth - 1))
            if value <= alpha: # check lower bound
                return value
            beta = min(beta, value) # update beta
        return value


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """
        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md


        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        timeout_check(self) # raises exception when time limit is reached

        best_score = float('-inf')

        legal_moves = game.get_legal_moves()

        # no legal moves left
        if terminal_test(game):
            return (-1, -1)
        # best move default (random legal move)
        best_move = legal_moves[r.randint(0, len(legal_moves) - 1)]

        # all possible actions constrained by depth/alpha/beta
        for move in legal_moves:
            value = self.min_value(game.forecast_move(move), alpha, beta, depth - 1)
            if value > best_score:
                best_score = value
                best_move = move
            alpha = max(alpha, best_score) # initial update on alpha
        return best_move
