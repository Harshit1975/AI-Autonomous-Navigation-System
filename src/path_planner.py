import heapq

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])

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
            path.reverse()

            # ✅ CLEAN RETURN (ONLY y,x)
            return [(node[0], node[1]) for node in path]

        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            neighbor = (current[0]+dr, current[1]+dc)

            r, c = neighbor

            if not (0 <= r < rows and 0 <= c < cols):
                continue

            if grid[r][c] == 1:
                continue

            temp_g = g_score[current] + 1

            if neighbor not in g_score or temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f = temp_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, neighbor))

    # ❌ NO PATH FOUND
    return None