import heapq
from collections import deque

# ===============================
# COMMON FUNCTION
# ===============================
def get_neighbors(node, grid):
    rows, cols = len(grid), len(grid[0])
    y, x = node

    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    neighbors = []

    for dy, dx in directions:
        ny, nx = y + dy, x + dx

        if 0 <= ny < rows and 0 <= nx < cols:
            if grid[ny][nx] == 0:
                neighbors.append((ny, nx))

    return neighbors


# ===============================
# A* ALGORITHM
# ===============================
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]

            path.append(start)
            return path[::-1]

        for neighbor in get_neighbors(current, grid):
            temp_g = g_score[current] + 1

            if neighbor not in g_score or temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f = temp_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, neighbor))

    return None


# ===============================
# BFS (Breadth First Search)
# ===============================
def bfs(grid, start, goal):
    queue = deque([start])
    visited = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = visited[current]

            return path[::-1]

        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                visited[neighbor] = current
                queue.append(neighbor)

    return None


# ===============================
# DIJKSTRA
# ===============================
def dijkstra(grid, start, goal):
    pq = [(0, start)]
    came_from = {}
    cost = {start: 0}

    while pq:
        curr_cost, current = heapq.heappop(pq)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]

            path.append(start)
            return path[::-1]

        for neighbor in get_neighbors(current, grid):
            new_cost = curr_cost + 1

            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))

    return None