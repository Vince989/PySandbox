import sys
import time


class Move:
    def __init__(self, piece, old_row, old_col, new_row, new_col):
        self.piece = piece
        self.old_row = old_row
        self.new_row = new_row
        self.old_col = old_col
        self.new_col = new_col


class Piece:
    id = 1

    def __init__(self, length, width, row, col):
        self.id = Piece.id; Piece.id += 1
        self.row = row
        self.col = col
        self.length = length
        self.width = width
        self.block_type = length * width

    def __repr__(self):
        if self.width > self.length:
            shape = "wide"
        elif self.length > self.width:
            shape = "high"
        else:
            shape = "sq"

        return (f"({self.id}: {self.length}l {self.width}w "
                f"{self.row}r {self.col}y  {self.block_type}{shape})")


class Board_state:
    def __init__(self, rows, cols, pieces):
        self.board = [[0] * cols for row in range(rows)]
        self.rows = rows
        self.cols = cols
        self.pieces = pieces
        self.place_all_pieces()
        # print('board state')
        # print('num pieces', len(pieces))
        # self.print_board()
        """
        EXAMPLE BOARD
                    columns(x):

                   0  1  2  3  4
    board =    0 [[1, 1, 0, 0, 1],
               1  [1, 1, 0, 1, 0],
    rows(y):   2  [0, 0, 0, 0, 1],
               3  [1, 0, 0, 0, 1],
               4  [1, 0, 1, 1, 0]
                ]

        blocks = [(2, 2, 0, 0),
                  (1, 1, 0, 4),
                  (1, 1, 1, 3),
                  (2, 1, 2, 4),
                  (2, 1, 3, 0),
                  (1, 2, 4, 2)
                 ]
                 each block in the blocks list is a tuple: (length, width, row, column)
        """

    def place_all_pieces(self):
        for piece in self.pieces:
            self.place_piece(piece)

    def print_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                print(self.board[row][col], end="")
            print()

    def place_piece(self, piece):
        for row in range(piece.row, piece.row + piece.length):
            for col in range(piece.col, piece.col + piece.width):
                self.board[row][col] = piece.id

    def check_valid_moves(self):
        moves = []
        for piece in self.pieces:
            # check move left
            # print('original piece position', piece.row, piece.col)
            shift = 1
            while piece.col - shift >= 0:
                # print('adding left moves')
                if all(row[piece.col - shift] == 0 for row in
                       self.board[piece.row:piece.row + piece.length]):
                    # print('new col', piece.col-shift)
                    moves.append(Move(piece, piece.row, piece.col, piece.row, piece.col - shift))
                else:
                    break
                shift += 1

            shift = 1
            while piece.col + piece.width + shift - 1 < self.cols:
                # print('_new col right', piece.col+piece.width+shift)
                # print('adding right moves')
                if all(row[piece.col + piece.width + shift - 1] == 0 for row in
                       self.board[piece.row:piece.row + piece.length]):
                    # print('new col right', piece.col+piece.width+shift)
                    moves.append(Move(piece, piece.row, piece.col, piece.row, piece.col + shift))
                else:
                    break
                shift += 1

            shift = 1
            while piece.row - shift >= 0:
                # print('adding up moves')
                if all(element == 0 for element in
                       self.board[piece.row - shift][piece.col:piece.col + piece.width]):
                    # print('new row', piece.row-shift)
                    moves.append(Move(piece, piece.row, piece.col, piece.row - shift, piece.col))
                else:
                    break
                shift += 1

            shift = 1
            while piece.row + piece.length + shift - 1 < self.rows:
                # print('adding down moves')
                if all(element == 0 for element in self.board[piece.row + piece.length + shift - 1][
                                                   piece.col:piece.col + piece.width]):
                    # print('new row', piece.row+piece.length+shift)
                    moves.append(Move(piece, piece.row, piece.col, piece.row + shift, piece.col))
                else:
                    break
                shift += 1
        return moves

    def check_column(self, new_col, start_row, end_row):
        return new_col >= 0 and new_col < self.cols and all(
            row[new_col] == 0 for row in self.board[start_row:end_row])

    def check_row(self, new_row, start_col, end_col):
        return new_row >= 0 and new_row < self.rows and all(
            element == 0 for element in self.board[new_row][start_col:end_col])


# 1. have a board, check valid moves ->
# 2. if board's distance to goal is 0, return True ->
# 3. generate and hash pieces list for each valid move ->
# 4. throw away pieces lists that have already been seen ->
# 5. for the ones that remain, calculate their distances to the goal ->
# 6. if one of the distances is 0, print out sequence and return True ->
# 7. create a board state for each pieces list ->
# 8. add each board state to the list of boards to be evaluated ->
# 9. if no more board states in list, print -1 and return false ->
# 10. pop the first board from the list and evaluate. ->
class Main:
    def __init__(self, goal_pieces, pieces, rows, cols):
        self.goal_pieces = goal_pieces
        self.goal_state = Board_state(rows, cols, goal_pieces)
        self.initial_pieces = pieces
        self.rows = rows
        self.cols = cols
        self.inspected_states = {}

    # returns the unique hash for this board state
    # add this value into the set to save the state
    def hash_pieces(self, pieces):
        return hash(
            tuple(sorted((piece.length, piece.width, piece.row, piece.col) for piece in pieces)))

    # def print_move(move):
    #   length, width, from_row, from_col, to_row, to_col = move
    #   print(f"{from_row} {from_col} {to_row} {to_col}")

    def already_inspected_state(self, state):
        return self.inspected_states.get(state, False)

    def set_inspected_state(self, state):
        self.inspected_states[state] = True

    def check_distance_to_goal(self, new_pieces):
        overall_distance = 0
        for goal in self.goal_pieces:
            shortest_distance = float('inf')
            for piece in new_pieces:
                if goal.length == piece.length and goal.width == piece.width:
                    if goal.row == piece.row and goal.col == piece.col:
                        shortest_distance = 0
                        # match of position and size has been found, so go to next goal
                        continue
                    y_distance = abs(goal.row - piece.row)
                    x_distance = abs(goal.col - piece.col)
                    distance = x_distance + y_distance
                    shortest_distance = min(shortest_distance, distance)
            overall_distance += shortest_distance
        # print('distance to goal', overall_distance)
        return overall_distance

    def filter_uninspected_moves(self, valid_moves, pieces, parent_state):
        uninspected_moves = []
        for move in valid_moves:
            updated_piece = Piece(move.piece.length, move.piece.width, move.new_row, move.new_col, )

            new_pieces = [piece for piece in pieces if piece != move.piece]
            new_pieces.append(updated_piece)

            state = self.hash_pieces(new_pieces)
            if not self.already_inspected_state(state):
                # print('old piece', move.piece.row, move.piece.col, 'new piece', move.new_row, move.new_col)
                self.set_inspected_state(state)
                distance_to_goal = self.check_distance_to_goal(new_pieces)
                uninspected_moves.append([new_pieces, move, distance_to_goal, state, parent_state])
        # print('valid moves', len(uninspected_moves))
        uninspected_moves.sort(key=lambda x: x[2])
        return uninspected_moves

    def solve_puzzle(self):
        initial_distance_to_goal = self.check_distance_to_goal(self.initial_pieces)
        if initial_distance_to_goal == 0:
            print(0, 0, 0, 0)
            return True
        initial_state = Board_state(self.rows, self.cols, self.initial_pieces)
        # print('start board')
        # initial_state.print_board()
        # print('goal board')
        # self.goal_state.print_board()
        state = self.hash_pieces(self.initial_pieces)
        self.set_inspected_state(state)
        moves_to_evaluate = []
        valid_moves = initial_state.check_valid_moves()
        if not valid_moves:
            print(-1)
            return False

        new_moves = self.filter_uninspected_moves(valid_moves, self.initial_pieces, None)
        moves_to_evaluate.extend(new_moves)

        tree = {}
        # print('beginning the loop')
        # end the loop if all possible states have been inspected
        start_time = time.time()
        while len(moves_to_evaluate) > 0:
            # extract data from next move and remove from moves_to_evaluate
            pieces, move, distance_to_goal, current_state, parent_state = moves_to_evaluate.pop(0)
            # print('printing new pieces')
            # for piece in pieces:
            #    print(piece.row, piece.col)
            # print(f'moving {move.piece.row}, {move.piece.col} to {move.new_row}, {move.new_col}')
            # add to tree
            tree[current_state] = (move, parent_state)
            if time.time() - start_time > 60:
                print('timeout')
                return False
            # return true if goal state is in current pieces
            if distance_to_goal == 0:

                sequence = []

                # move backwards to get sequence of moves from beginning
                sequence.append(move)
                while parent_state != None:
                    sequence.append(tree[parent_state][0])
                    parent_state = tree[parent_state][1]
                # print out sequence in order
                for move in sequence[::-1]:
                    print(move.old_row, move.old_col, move.new_row, move.new_col)
                print(time.time() - start_time)
                return True

            # create new board for the current state
            new_state = Board_state(self.rows, self.cols, pieces)

            # generate new moves from current state
            valid_moves = new_state.check_valid_moves()
            # if no valid moves, that means this state is a dead end
            if valid_moves:
                new_moves = self.filter_uninspected_moves(valid_moves, pieces, current_state)
                # add new moves to list of moves_to_evaluate
                moves_to_evaluate.extend(new_moves)
                # for move in new_moves:
                #    print(move[1].piece.row, move[1].piece.col, move[1].new_row, move[1].new_col)
        print(-1)
        return False
