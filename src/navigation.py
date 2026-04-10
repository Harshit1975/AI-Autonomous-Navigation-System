# navigation.py — Controls the agent's movement along the planned path

class NavigationController:
    """
    Moves the agent cell-by-cell along the computed path.
    Tracks position, step count, and status.
    """

    def __init__(self, path):
        self.path = path
        self.step_index = 0
        self.finished = False
        self.collided = False

    @property
    def current_position(self):
        """Current (row, col) of the agent."""
        if self.step_index < len(self.path):
            return self.path[self.step_index]
        return self.path[-1]

    def advance(self, grid):
        """
        Move one step forward on the path.
        Checks for collision before moving.
        Returns True if the step was taken, False if blocked or done.
        """
        if self.finished or self.collided:
            return False

        next_index = self.step_index + 1
        if next_index >= len(self.path):
            self.finished = True
            return False

        next_pos = self.path[next_index]
        r, c = next_pos

        # Collision check (dynamic obstacle could have appeared)
        if grid[r][c] == 1:
            self.collided = True
            return False

        self.step_index = next_index
        return True

    def status(self):
        if self.collided:
            return "COLLISION DETECTED — replanning needed"
        if self.finished:
            return "GOAL REACHED"
        return f"Navigating — step {self.step_index}/{len(self.path) - 1}"