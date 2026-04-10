import sys
import json
import numpy as np

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.path_planner import astar, bfs, dijkstra 


# ===============================
# 🎯 CANVAS (GRID UI)
# ===============================
class Canvas(QWidget):
    def __init__(self, rows=20, cols=20):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.cell_size = 25

        self.grid = np.zeros((rows, cols))
        self.start = (0, 0)
        self.goal = (rows - 1, cols - 1)

        self.path = []
        self.explored = []

        self.mode = "obstacle"

        self.setFixedSize(cols * self.cell_size, rows * self.cell_size)
        self.setCursor(Qt.CrossCursor)

    # 🎯 DRAW GRID
    def paintEvent(self, event):
        painter = QPainter(self)

        for y in range(self.rows):
            for x in range(self.cols):
                rect_x = x * self.cell_size
                rect_y = y * self.cell_size

                if (y, x) == self.start:
                    painter.fillRect(rect_x, rect_y, self.cell_size, self.cell_size, QColor("green"))

                elif (y, x) == self.goal:
                    painter.fillRect(rect_x, rect_y, self.cell_size, self.cell_size, QColor("red"))

                elif self.grid[y][x] == 1:
                    painter.fillRect(rect_x, rect_y, self.cell_size, self.cell_size, QColor("black"))

                else:
                    painter.fillRect(rect_x, rect_y, self.cell_size, self.cell_size, QColor(220, 240, 255))

                painter.drawRect(rect_x, rect_y, self.cell_size, self.cell_size)

        # 🔥 DRAW PATH
        # === DRAW FULL PATH (light yellow dots) ===
        painter.setBrush(QColor(255, 255, 0, 120))  # light transparent yellow

        for node in getattr(self, "full_path", []):
            try:
                 y, x = node[0], node[1]
                 painter.drawEllipse(
                    int(x) * self.cell_size + 8,
                    int(y) * self.cell_size + 8,
                    6, 6
                )
            except:
               continue


# === DRAW VISITED PATH (bright yellow) ===
        painter.setBrush(QColor("yellow"))

        for node in self.path:
            try:
                y, x = node[0], node[1]
                painter.drawEllipse(
                    int(x) * self.cell_size + 6,
                    int(y) * self.cell_size + 6,
                    10, 10
            )
            except:
               continue


# === DRAW AGENT (moving ball 🔴) ===
        if len(self.path) > 0:
          y, x = self.path[-1][0], self.path[-1][1]

          painter.setBrush(QColor("red"))
          painter.drawEllipse(
             int(x) * self.cell_size + 5,
             int(y) * self.cell_size + 5,
             12, 12
    )
          
    # ✅ CLICK ONLY (FIXED)
    def mousePressEvent(self, event):
        x = event.pos().x() // self.cell_size
        y = event.pos().y() // self.cell_size

        if 0 <= x < self.cols and 0 <= y < self.rows:
            if self.mode == "obstacle":
                self.grid[y][x] = 1

            elif self.mode == "erase":
                self.grid[y][x] = 0

            elif self.mode == "start":
                self.start = (y, x)

            elif self.mode == "goal":
                self.goal = (y, x)

            self.update()


# ===============================
# 🎯 MAIN WINDOW
# ===============================
class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Autonomous Navigation System")

        self.canvas = Canvas()

        self.status = QLabel("Ready")
        self.steps_label = QLabel("Steps: 0")
        self.path_label = QLabel("Path: 0")
        self.obs_label = QLabel("Obstacles: 0")

        self.start_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")
        self.reset_btn = QPushButton("Reset")
        self.save_btn = QPushButton("Save Map")
        self.load_btn = QPushButton("Load Map")

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.status)
        layout.addWidget(self.steps_label)
        layout.addWidget(self.path_label)
        layout.addWidget(self.obs_label)

        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.reset_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.load_btn)

        self.setLayout(layout)

        # 🔥 TIMER (ANIMATION)
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)

        self.current_step = 0

        # 🔗 BUTTON EVENTS
        self.start_btn.clicked.connect(self.start_sim)
        self.stop_btn.clicked.connect(self.stop_sim)
        self.reset_btn.clicked.connect(self.reset)
        self.save_btn.clicked.connect(self.save_map)
        self.load_btn.clicked.connect(self.load_map)

    # ===============================
    # ▶ START SIMULATION
    # ===============================
    def start_sim(self):
      result = astar(self.canvas.grid.tolist(), self.canvas.start, self.canvas.goal)

      if not result:
        self.status.setText("No Path Found ❌")
        return

      self.full_path = result          # 🔥 STORE FULL PATH
      self.canvas.full_path = result   # 🔥 SEND TO CANVAS
      self.canvas.path = []            # visited path

      self.current_step = 0
      self.timer.start(80)

      self.status.setText("Running...")

    # ===============================
    # ⏸ STOP
    # ===============================
    def stop_sim(self):
        self.timer.stop()
        self.status.setText("Stopped")

    # ===============================
    # 🔄 RESET
    # ===============================
    def reset(self):
        self.canvas.grid = np.zeros_like(self.canvas.grid)
        self.canvas.path = []
        self.canvas.start = (0, 0)
        self.canvas.goal = (19, 19)

        self.canvas.update()

        self.status.setText("Reset Done")
        self.steps_label.setText("Steps: 0")
        self.path_label.setText("Path: 0")
        self.obs_label.setText("Obstacles: 0")

    # ===============================
    # 🎬 ANIMATION (ARROW EFFECT)
    # ===============================
    def animate(self):
        if self.current_step < len(self.full_path):
            self.canvas.path.append(self.full_path[self.current_step])
            self.current_step += 1

            self.canvas.update()

            self.steps_label.setText(f"Steps: {self.current_step}")
            self.path_label.setText(f"Path: {len(self.full_path)}")

            obstacles = int(np.sum(self.canvas.grid))
            self.obs_label.setText(f"Obstacles: {obstacles}")

        else:
            self.timer.stop()
            self.status.setText("Goal Reached ✅")
            self.show_graph()

    # ===============================
    # 📊 GRAPH INSIDE UI
    # ===============================
    def show_graph(self):
        fig = Figure(figsize=(4, 3))
        ax = fig.add_subplot(111)

        steps = list(range(len(self.canvas.path)))

        ax.plot(steps, marker='o')
        ax.set_title("Steps Over Time")

        if hasattr(self, 'graph'):
            self.layout().removeWidget(self.graph)
            self.graph.deleteLater()

        self.graph = FigureCanvas(fig)
        self.layout().addWidget(self.graph)

    # ===============================
    # 💾 SAVE MAP
    # ===============================
    def save_map(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Map", "", "JSON (*.json)")

        if path:
            data = {
                "grid": self.canvas.grid.tolist(),
                "start": self.canvas.start,
                "goal": self.canvas.goal
            }

            with open(path, "w") as f:
                json.dump(data, f)

    # ===============================
    # 📂 LOAD MAP
    # ===============================
    def load_map(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Map", "", "JSON (*.json)")

        if path:
            with open(path, "r") as f:
                data = json.load(f)

            self.canvas.grid = np.array(data["grid"])
            self.canvas.start = tuple(data["start"])
            self.canvas.goal = tuple(data["goal"])

            self.canvas.update()


# ===============================
# 🚀 RUN APP
# ===============================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())