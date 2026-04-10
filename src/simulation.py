# simulation.py — Full Pygame simulation window

import pygame
import sys
import time
import cv2
import numpy as np
from src.utils import *
from src.path_planner import astar
from src.obstacle_detector import generate_obstacle_frame, detect_obstacle_at
from src.navigation import NavigationController


def create_default_grid():
    """Build a 20x20 grid with some preset obstacles."""
    grid = [[0] * GRID_COLS for _ in range(GRID_ROWS)]
    # Add wall-like obstacles
    obstacles = [
        (3,5),(3,6),(3,7),(3,8),(3,9),
        (7,2),(8,2),(9,2),(10,2),(11,2),
        (5,12),(6,12),(7,12),(8,12),
        (13,6),(13,7),(13,8),(13,9),(13,10),(13,11),
        (16,3),(16,4),(16,5),
        (1,15),(2,15),(3,15),(4,15),(5,15),
        (10,14),(11,14),(12,14),(12,15),(12,16),
    ]
    for r, c in obstacles:
        grid[r][c] = 1
    return grid

def draw_cell(surface, row, col, color):
    x = col * CELL_SIZE
    y = row * CELL_SIZE
    rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2)
    pygame.draw.rect(surface, color, rect, border_radius=3)

def draw_grid(surface, grid, path, visited, agent_pos, start, goal):
    surface.fill(BG_COLOR)

    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            pos = (r, c)
            if grid[r][c] == 1:
                draw_cell(surface, r, c, DARK_GRAY)
            elif pos == agent_pos:
                draw_cell(surface, r, c, BLUE)
            elif pos == goal:
                draw_cell(surface, r, c, GREEN)
            elif pos == start:
                draw_cell(surface, r, c, ORANGE)
            elif pos in set(path):
                draw_cell(surface, r, c, YELLOW)
            elif pos in visited:
                draw_cell(surface, r, c, (220, 235, 250))
            else:
                draw_cell(surface, r, c, WHITE)

    # Grid lines
    for r in range(GRID_ROWS + 1):
        pygame.draw.line(surface, GRAY, (0, r * CELL_SIZE),
                         (GRID_COLS * CELL_SIZE, r * CELL_SIZE), 1)
    for c in range(GRID_COLS + 1):
        pygame.draw.line(surface, GRAY, (c * CELL_SIZE, 0),
                         (c * CELL_SIZE, GRID_ROWS * CELL_SIZE), 1)

def draw_dashboard(surface, font, small_font, nav, steps, path_len):
    """Side panel with stats."""
    px = GRID_COLS * CELL_SIZE + 10
    pw = 190
    pygame.draw.rect(surface, PANEL_BG, (GRID_COLS * CELL_SIZE, 0, 200, WINDOW_H))

    title = font.render("NAV SYSTEM", True, WHITE)
    surface.blit(title, (px, 15))

    lines = [
        ("Status", nav.status()[:22] if nav else "Planning..."),
        ("Steps taken", str(steps)),
        ("Path length", str(path_len)),
        ("Agent pos", str(nav.current_position) if nav else "—"),
    ]
    y = 60
    for label, value in lines:
        lbl = small_font.render(label + ":", True, GRAY)
        val = small_font.render(value, True, YELLOW)
        surface.blit(lbl, (px, y))
        surface.blit(val, (px, y + 18))
        y += 52

    # Legend
    legend = [
        (BLUE,     "Agent"),
        (GREEN,    "Goal"),
        (ORANGE,   "Start"),
        (YELLOW,   "Path"),
        (DARK_GRAY,"Obstacle"),
        ((220,235,250), "Explored"),
    ]
    y = WINDOW_H - 160
    small2 = small_font
    for color, label in legend:
        pygame.draw.rect(surface, color, (px, y, 12, 12), border_radius=2)
        lbl = small2.render(label, True, GRAY)
        surface.blit(lbl, (px + 18, y))
        y += 22

def run_simulation():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("AI Autonomous Navigation System")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("monospace", 14, bold=True)
    small_font = pygame.font.SysFont("monospace", 11)

    grid = create_default_grid()
    start = (0, 0)
    goal  = (19, 19)

    # Run A* path planning
    path = astar(grid, start, goal)
    if not path:
        print("No path found! Check your grid.")
        pygame.quit()
        sys.exit()

    print(f"Path found: {len(path)} steps")

    nav = NavigationController(path)
    visited = set()
    steps = 0
    move_delay = 0.08   # seconds between agent steps
    last_move = time.time()

    # Save OpenCV frame as proof asset
    cv_frame = generate_obstacle_frame(grid, CELL_SIZE)
    cv2.imwrite("outputs/screenshots/obstacle_map_opencv.png", cv_frame)
    print("Saved obstacle map to outputs/screenshots/")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:   # R = restart
                    nav = NavigationController(path)
                    steps = 0
                    visited.clear()
                if event.key == pygame.K_s:   # S = screenshot
                    pygame.image.save(screen, "outputs/screenshots/nav_screenshot.png")
                    print("Screenshot saved.")

        # Advance agent
        now = time.time()
        if now - last_move > move_delay and not nav.finished and not nav.collided:
            visited.add(nav.current_position)
            nav.advance(grid)
            steps += 1
            last_move = now

        # Draw
        draw_grid(screen, grid, path, visited,
                  nav.current_position, start, goal)
        draw_dashboard(screen, font, small_font, nav, steps, len(path))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

    