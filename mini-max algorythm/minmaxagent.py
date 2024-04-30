import copy
from copy import deepcopy


def change_player(connect4, next_connect):
    if connect4.who_moves == 'o':
        next_connect.who_moves = 'x'
    else:
        next_connect.who_moves = 'o'


class MinMaxAgent:
    def __init__(self, my_token=str):
        self.my_token = my_token

    def decide(self, connect4):
        best_value = float('-inf')
        best_column = None
        row = None
        for line in connect4.possible_drops():
            next_connect = copy.deepcopy(connect4)
            next_connect.drop_token(line)
            value = self.minimax(next_connect, 3, True)
            if value > best_value:
                best_value = value
                best_column = line
        return best_column

    def minimax(self, connect4, depth, is_maximizing):
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
            max_value = -float('inf')
            for line in connect4.possible_drops():
                next_connect = copy.deepcopy(connect4)
                next_connect.drop_token(line)
                value = self.minimax(next_connect, depth - 1, False)
                max_value = max(max_value, value)
            return max_value
        else:
            min_value = float('inf')
            for line in connect4.possible_drops():
                next_connect = copy.deepcopy(connect4)
                change_player(connect4, next_connect)
                next_connect.drop_token(line)
                value = self.minimax(next_connect, depth - 1, True)
                min_value = min(min_value, value)
            return min_value

    def evaluation(self, connect4):
        if self.my_token == 'o':
            opponent_token = 'x'
        else:
            opponent_token = 'o'
        score = 0
        opponent_score = 0
        final_score = 0
        for four in connect4.iter_fours():
            if four.count(self.my_token) == 3 and four.count('_') == 1:
                score += 0.2
            if four.count(self.my_token) == 2 and four.count('_') == 1:
                score += 0.1
            if four.count(self.my_token) == 3 and four.count(opponent_token) == 1:
                opponent_score += 0.2
            if four.count(self.my_token) == 2 and four.count(opponent_token) == 1:
                opponent_score += 0.1
            if four.count(opponent_token) == 2 and four.count(self.my_token) == 1:
                score += 0.1
            if four.count(opponent_token) == 3 and four.count(self.my_token) == 1:
                score += 0.2
            if four.count(opponent_token) == 3 and four.count('_') == 1:
                opponent_score += 0.2
            if four.count(opponent_token) == 2 and four.count('_') == 1:
                opponent_score += 0.1
        final_score = score - opponent_score
        if final_score >= 1:
            final_score = 0.9
        return final_score
