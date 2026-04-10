# utils.py — Shared constants and color definitions

# Grid settings
GRID_ROWS = 20
GRID_COLS = 20
CELL_SIZE = 30          # pixels per cell
WINDOW_W = GRID_COLS * CELL_SIZE + 200   # extra panel for dashboard
WINDOW_H = GRID_ROWS * CELL_SIZE

FPS = 30

# Colors (RGB)
WHITE      = (255, 255, 255)
BLACK      = (20,  20,  20)
GRAY       = (180, 180, 180)
DARK_GRAY  = (60,  60,  60)
GREEN      = (39,  174, 96)
RED        = (231, 76,  60)
BLUE       = (52,  152, 219)
YELLOW     = (241, 196, 15)
ORANGE     = (230, 126, 34)
PURPLE     = (155, 89,  182)
BG_COLOR   = (245, 245, 245)
PANEL_BG   = (30,  30,  30)

# Cell types
EMPTY    = 0
OBSTACLE = 1
START    = 2
GOAL     = 3
PATH     = 4
VISITED  = 5
AGENT    = 6