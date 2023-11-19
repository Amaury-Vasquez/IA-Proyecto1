from models.fifteen_puzzle_model import Coordinate, SolutionItem
from scipy.spatial.distance import cityblock
from numpy import copy
import math

# In order to solve the puzzle, we need to define a heuristic function
# that will evaluate the board and return a number that represents
# how close the board is to the solution.
# The grades for each coordinate are given according to the manhattan distance
# If you can't move the coordinate that is being evaluated, you add 1 point to the coord evaluation
# The best evaluation is 0, which means that the board is solved.

def move_square(board: list[list[int or None]], emptySquare: Coordinate, move: Coordinate) -> list[list[int or None]]:
  newBoard = copy(board)
  print(newBoard)
  newBoard[emptySquare.y][emptySquare.x] = newBoard[move.y][move.x]
  newBoard[move.y][move.x] = None
  return newBoard

def get_moves(board: list[list[int or None]], emptySquare: Coordinate) -> list[Coordinate]:
  y = emptySquare.y
  x = emptySquare.x
  moves = []
  if (x > 0):
    a_move = Coordinate(x = x - 1, y = y)
    moves.append({"move": a_move, "rate": evaluate_puzzle(move_square(board, emptySquare, a_move))})
  if (x < 3):
    b_move = Coordinate(x = x + 1, y = y)
    moves.append({"move": b_move, "rate": evaluate_puzzle(move_square(board, emptySquare, b_move))})
  if (y > 0):
    c_move = Coordinate(x = x, y = y - 1)
    moves.append({"move": c_move, "rate": evaluate_puzzle(move_square(board, emptySquare, c_move))})
  if (y < 3):
    d_move = Coordinate(x = x, y = y + 1)
    moves.append({"move": d_move, "rate": evaluate_puzzle(move_square(board, emptySquare, d_move))})
    
  moves.sort(key = lambda move: move["rate"], reverse = True)
  return moves

def evaluate_puzzle(board: list[list[int or None]]) -> int:
  accumulated = 0
  for idx, row in enumerate(board):
    for jdx, value in enumerate(row):
      if value is not None:
        ideal_row = (value - 1)
        accumulated += cityblock([idx, jdx], [math.trunc(ideal_row / 4), ideal_row % 4])
  return abs((accumulated * 2) - 100)

def solve_puzzle(board: list[list[int or None]], emptySquare: Coordinate) -> list[SolutionItem]:
  solution_found = False
  solution_moves: list[SolutionItem] = []
  iterations = 0
  rate = 0
  while not solution_found and iterations < 50:
    if (rate == 100):
      solution_found = True
    else:
      possible_moves = get_moves(board, emptySquare)
      board = move_square(board, possible_moves[0]["move"], emptySquare)
      rate = evaluate_puzzle(board)
      solution_moves.append(SolutionItem(start = possible_moves[0]["move"], end = emptySquare, evaluation = rate))
      emptySquare = possible_moves[0]["move"]
    iterations += 1
  return {"solution_found": solution_found, "moves": solution_moves, "iterations": iterations}