import heapq
import copy

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
    print(total_distance)
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

def print_solution(solution_node):
  # Print the solution path
  path = []
  while solution_node:
    path.append(solution_node.move)
    solution_node = solution_node.parent
  path.reverse()
  print("Solution Path:")
  print(" -> ".join(path))

def solve_15_puzzle(initial_state):
  # A* algorithm to solve the 15 Puzzle problem
  start_node = PuzzleNode(initial_state)
  goal_state = PuzzleNode([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])

  visited = set()
  priority_queue = [start_node]

  while priority_queue:
    current_node = heapq.heappop(priority_queue)

    if current_node.puzzle == goal_state.puzzle:
      print("Puzzle Solved!")
      print_solution(current_node)
      break

    visited.add(tuple(map(tuple, current_node.puzzle)))

    neighbors = get_neighbors(current_node)
    for neighbor in neighbors:
      if tuple(map(tuple, neighbor.puzzle)) not in visited:
        heapq.heappush(priority_queue, neighbor)

if __name__ == "__main__":
  # Example usage:
  initial_state = [
      [1, 2, 3, 4],
      [5, 6, 0, 8],
      [9, 10, 7, 12],
      [13, 14, 11, 15]
  ]
  print(initial_state)
  solve_15_puzzle(initial_state)