from pydantic import BaseModel
from typing import Optional

class Coordinate(BaseModel):
  x: int
  y: int
  
class SolutionItem(BaseModel):
  start: Coordinate
  end: Coordinate
  evaluation: int
  
class FifteenPuzzleBoard(BaseModel):
  board: list[list[Optional[int]]]

class FifteenPuzzleEvaluation(BaseModel):
  evaluation: int
  
class FifteenPuzzleSolution(BaseModel):
  moves: list[SolutionItem]
  solution_found: bool
  iterations: int

class FifteenPuzzleSolutionRequest(FifteenPuzzleBoard):
  emptySquare: Coordinate
  