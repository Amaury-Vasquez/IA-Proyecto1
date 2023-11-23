from models.fifteen_puzzle_model import Coordinate
from scipy.spatial.distance import cityblock
import math
import random
import heapq
import copy

def get_empty_square(board: list[list[int or None]]) -> Coordinate:
  for idx, row in enumerate(board):
      for jdx, value in enumerate(row):
        if value == 0:
          return Coordinate(x=jdx, y=idx)

def get_is_solvable(puzzle):
  # Aplanar la lista
  flattened = [num for row in puzzle for num in row]
    
  # Encontrar la posición del espacio en blanco (representado por 0)
  blank_row = next(i for i, x in enumerate(puzzle) if 0 in x)

  # Contar inversiones
  inversions = 0
  for i in range(len(flattened)):
    for j in range(i + 1, len(flattened)):
      if flattened[i] > flattened[j] and flattened[i] != 0 and flattened[j] != 0:
        inversions += 1

  # Verificar si la paridad de la permutación y la posición del espacio en blanco son ambas pares o ambas impares
  return (inversions % 2 == 0) == (blank_row % 2 != 0)

class PuzzleNode:
  def __init__(self, puzzle, parent=None, move=""):
    self.puzzle = puzzle
    self.parent = parent
    self.move = move
    self.cost = 0  # g(n)
    self.heuristic = 0  # h(n)
    self.calculate_cost()
  
  def calculate_cost(self):
    # Calculate the cost (g(n)) and heuristic (h(n))
    if self.parent:
      self.cost = self.parent.cost + 1
    self.heuristic = self.calculate_heuristic()

  def calculate_heuristic(self):
    # A* heuristic function (Manhattan distance)
    total_distance = 0
    for i in range(4):
      for j in range(4):
        if self.puzzle[i][j] != 0:
          row, col = divmod(self.puzzle[i][j] - 1, 4)
          total_distance += abs(i - row) + abs(j - col)
    return total_distance

  def __lt__(self, other):
    # Comparison method for priority queue
    return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def get_movement_direction(empty_row, empty_col, new_row, new_col):
    # Get the movement direction based on the change in coordinates
    if new_col > empty_col:
        return "R"
    elif new_col < empty_col:
        return "L"
    elif new_row > empty_row:
        return "D"
    elif new_row < empty_row:
        return "U"
    else:
        return ""

def get_neighbors(node):
  # Generate neighboring nodes by moving the empty space
  neighbors = []
  empty_row, empty_col = next((i, j) for i, row in enumerate(node.puzzle) for j, val in enumerate(row) if val == 0)

  moves = [(0, 1, "R"), (1, 0, "D"), (0, -1, "L"), (-1, 0, "U")]

  for dr, dc, move in moves:
    new_row, new_col = empty_row + dr, empty_col + dc
    if 0 <= new_row < 4 and 0 <= new_col < 4:
      new_puzzle = copy.deepcopy(node.puzzle)
      new_puzzle[empty_row][empty_col], new_puzzle[new_row][new_col] = new_puzzle[new_row][new_col], new_puzzle[empty_row][empty_col]
      direction = get_movement_direction(empty_row, empty_col, new_row, new_col)
      neighbors.append(PuzzleNode(new_puzzle, node, direction))

  return neighbors

def get_solution_path(solution_node):
  path = []
  while solution_node:
    path.append(solution_node.puzzle)
    solution_node = solution_node.parent
  path.reverse()
  return path

def solve_15_puzzle(initial_state: list[list[int]]):
  # A* algorithm to solve the 15 Puzzle problem
  start_node = PuzzleNode(initial_state)
  goal_state = PuzzleNode([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])

  visited = set()
  priority_queue = [start_node]
  solution_path = []
  while priority_queue:
    current_node = heapq.heappop(priority_queue)

    if current_node.puzzle == goal_state.puzzle:
      solution_path = get_solution_path(current_node)
      break

    visited.add(tuple(map(tuple, current_node.puzzle)))

    neighbors = get_neighbors(current_node)
    for neighbor in neighbors:
      if tuple(map(tuple, neighbor.puzzle)) not in visited:
        heapq.heappush(priority_queue, neighbor)
  return solution_path

def get_random_board() -> list[list[int or None]]:
  board = list(range(0, 16))
  random.shuffle(board)
  return [board[0:4], board[4:8], board[8:12], board[12:16]]

def evaluate_puzzle(board: list[list[int or None]]) -> int:
  accumulated = 0

  for idx, row in enumerate(board):
    for jdx, value in enumerate(row):
      if value != 0:
        ideal_linear_value = (value - 1)
        ideal_row, ideal_column = divmod(ideal_linear_value, 4)
        accumulated += cityblock([idx, jdx], [ideal_row, ideal_column])
  return abs((accumulated * 2) - 100)

def solve_puzzle(board):
  is_solvable = get_is_solvable(board)
  solution_moves: list[list[int]] = []
  if is_solvable:
    solution_moves = solve_15_puzzle(board)
  return dict(solution_found=is_solvable, moves=solution_moves)