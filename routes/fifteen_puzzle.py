from fastapi import APIRouter
from models.fifteen_puzzle_model import *
from solutions.fifteen_puzzle_solution import evaluate_puzzle, solve_puzzle

# mockBoard = [
#   [15, 14, 13, 12],
#   [11, 10, 9, 8],
#   [None, 6, 5, 7],
#   [4, 3, 2, 1]
# ]
solvedBoard = [
  [1, 2, 3, 4],
  [5, 6, 7, 8],
  [9, 10, 11, 12],
  [13, 14, 15, None]
]

puzzle_router = APIRouter(tags=["fifteen-puzzle"], prefix="/fifteen-puzzle")

@puzzle_router.post("/evaluate", response_model=FifteenPuzzleEvaluation)
def evaluate(data: FifteenPuzzleBoard):
  return {
    "evaluation": evaluate_puzzle(data.board)
  }

@puzzle_router.post("/solve", response_model=FifteenPuzzleSolution)
def solve(data: FifteenPuzzleSolutionRequest):
  emptySquare = Coordinate(x = 3, y = 3)
  solution_moves = solve_puzzle(solvedBoard, emptySquare)
  return solution_moves