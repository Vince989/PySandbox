import sys
from sliding import Main, Piece

board_data = sys.argv[1]
goal_data = sys.argv[2]

with open(board_data, 'r') as board_file:
    rows, cols = map(int, board_file.readline().strip().split())
    pieces = [Piece(*[int(num) for num in line.strip().split()])
              for line in board_file]

with open(goal_data, 'r') as goal_file:
    goal_pieces = [Piece(*[int(num) for num in line.strip().split()])
                   for line in goal_file]
    # if not 'many.blocks' in goal_data:

main = Main(goal_pieces, pieces, rows, cols)
main.solve_puzzle()
