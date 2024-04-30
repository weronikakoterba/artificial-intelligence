import copy


def change_player(connect4, next_connect):
    if connect4.who_moves == 'o':
        next_connect.who_moves = 'x'
    else:
        next_connect.who_moves = 'o'


class AlphaBetaAgentWithoutEvaluation:
    def __init__(self, my_token=str):
        self.my_token = my_token

    def decide(self, connect4):
        tab=[]
        alpha = -float('inf')
        beta = float('inf')
        best_value = float('-inf')
        best_column = None
        row = None
        for line in connect4.possible_drops():
            next_connect = copy.deepcopy(connect4)
            next_connect.drop_token(line)
            value = self.alphabeta(next_connect, 6, alpha, beta, True)
            if value > best_value:
                best_value = value
                best_column = line
        return best_column

    def alphabeta(self, connect4, depth, alpha, beta, is_maximizing):
        if connect4.game_over:
            if connect4.wins == self.my_token:
                return 1
            if connect4.wins is None:
                return 0
            else:
                return -1
        elif depth == 0:
            return self.evaluation(connect4)
        elif is_maximizing:
            max_value = float('-inf')
            for line in connect4.possible_drops():
                next_connect = copy.deepcopy(connect4)
                next_connect.drop_token(line)
                value = self.alphabeta(next_connect, depth - 1, alpha, beta, False)
                alpha = max(alpha, value)
                max_value = max(max_value, value)
                if max_value >= beta:
                    break
            return max_value
        else:
            min_value = float('inf')
            for line in connect4.possible_drops():
                next_connect = copy.deepcopy(connect4)
                change_player(connect4, next_connect)
                next_connect.drop_token(line)
                value = self.alphabeta(next_connect, depth - 1, alpha, beta, True)
                beta = min(beta, value)
                min_value = min(min_value, value)
                if min_value <= alpha:
                    break
            return min_value

    def evaluation(self, connect4):
        return 0
