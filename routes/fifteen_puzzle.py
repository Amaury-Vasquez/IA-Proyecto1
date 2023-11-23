from fastapi import APIRouter
from models.fifteen_puzzle_model import *
from solutions.fifteen_puzzle_solution import evaluate_puzzle, solve_puzzle, get_random_board, get_is_solvable

puzzle_router = APIRouter(tags=["fifteen-puzzle"], prefix="/fifteen-puzzle")

@puzzle_router.get("/board", response_model=FifteenPuzzleBoard)
def get_board():
  is_solvable = False
  board = []
  while not is_solvable:
    board = get_random_board()
    is_solvable = get_is_solvable(board)
    
  return {"board": board}

@puzzle_router.post("/evaluate", response_model=int)
def evaluate(data: FifteenPuzzleBoard):
  try:
    return evaluate_puzzle(data.board)
  except Exception as e:
    print(e)

@puzzle_router.post("/solve", response_model=FifteenPuzzleSolution)
def solve(data: FifteenPuzzleBoard):
  try:
    solution = solve_puzzle(data.board)
    return {"solution_found": solution["solution_found"], "moves": solution["moves"]}
  except Exception as e:
    print(e)