from pydantic import BaseModel
from typing import Optional, List

class Coordinate(BaseModel):
  x: int
  y: int
  
  __eq__ = lambda self, other: self.x == other.x and self.y == other.y
  
class SolutionItem(BaseModel):
  start: Coordinate
  end: Coordinate
  value: int
  evaluation: int
  
  __eq__ = lambda self, other: self.start == other.start and self.end == other.end and self.value == other.value and self.evaluation == other.evaluation
  
class FifteenPuzzleBoard(BaseModel):
  board: List[List[int]] = [
    [1, 2, 3, 4], 
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 0, 15]
  ]

class FifteenPuzzleSolution(BaseModel):
  moves: List[List[List[int]]]
  solution_found: bool

class FifteenPuzzleSolutionRequest(FifteenPuzzleBoard):
  emptySquare: Coordinate = Coordinate(x=2, y=3)
  