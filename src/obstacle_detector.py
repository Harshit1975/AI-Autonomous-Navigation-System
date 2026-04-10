# obstacle_detector.py — Uses OpenCV to process a frame and detect obstacles

import cv2
import numpy as np

def generate_obstacle_frame(grid, cell_size):
    """
    Renders the grid as an OpenCV image.
    Returns a BGR frame showing free cells (white) vs obstacles (red).
    """
    rows = len(grid)
    cols = len(grid[0])
    frame = np.ones((rows * cell_size, cols * cell_size, 3), dtype=np.uint8) * 240

    for r in range(rows):
        for c in range(cols):
            x = c * cell_size
            y = r * cell_size
            if grid[r][c] == 1:   # obstacle
                cv2.rectangle(frame, (x, y), (x + cell_size, y + cell_size),
                              (0, 0, 200), -1)  # filled red (BGR)

    # Draw grid lines
    for r in range(rows + 1):
        cv2.line(frame, (0, r * cell_size),
                 (cols * cell_size, r * cell_size), (180, 180, 180), 1)
    for c in range(cols + 1):
        cv2.line(frame, (c * cell_size, 0),
                 (c * cell_size, rows * cell_size), (180, 180, 180), 1)

    return frame

def detect_obstacle_at(grid, row, col):
    """Returns True if the given cell is an obstacle."""
    rows = len(grid)
    cols = len(grid[0])
    if 0 <= row < rows and 0 <= col < cols:
        return grid[row][col] == 1
    return True   # treat out-of-bounds as obstacle