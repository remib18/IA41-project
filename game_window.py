import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsRectItem,
    QGraphicsPolygonItem,
    QGraphicsEllipseItem,
    QGraphicsPathItem,
    QGraphicsTextItem,
)
from PyQt6.QtGui import QBrush, QPolygonF, QPen, QPainterPath
from PyQt6.QtCore import Qt, QPointF

from game_runtime import GameRuntime


class GameWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.runtime = GameRuntime()
        self.runtime.load_new_board()
        self.runtime.new_target()
        self.cell_size = 40
        self.canvas_padding = 20
        canvas_base_size = (
            self.cell_size * self.runtime.board.board_size + self.canvas_padding * 2
        )
        canvas_size = (
            canvas_base_size,
            canvas_base_size + 40,
        )

        # Window setup
        self.setWindowTitle("Ricochet Robots")
        self.setFixedSize(canvas_size[0], canvas_size[1])

        # Create a scene and view
        self.scene = QGraphicsScene()
        view = QGraphicsView(self.scene, self)
        view.setGeometry(0, 0, canvas_size[0], canvas_size[1])
        self.scene.setBackgroundBrush(Qt.GlobalColor.white)

        self.chip_items = []
        self.draw_board()
        self.draw_goal()

    @staticmethod
    def get_color(color_code):
        # TODO: Add more colors when randomization is allowed
        colors = [
            Qt.GlobalColor.red,
            Qt.GlobalColor.green,
            Qt.GlobalColor.cyan,
            Qt.GlobalColor.darkYellow,
        ]
        return colors[color_code]

    @staticmethod
    def get_color_name(color_code):
        # TODO: Add more colors when randomization is allowed
        colors = [
            "red",
            "green",
            "blue",
            "yellow",
        ]
        return colors[color_code]

    @staticmethod
    def get_shape(shape_code):
        # TODO: Add more shapes when randomization is allowed
        shapes = [
            "circle",
            "square",
            "triangle",
            "star",
        ]
        return shapes[shape_code]

    def draw_board(self):
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(4)  # Set thickness to 4 pixels

        walls_grid = self.runtime.board.walls
        mirrors_grid = self.runtime.board.mirrors
        chips_grid = self.runtime.board.chips

        for i in range(self.runtime.board.board_size):
            for j in range(self.runtime.board.board_size):
                x1 = j * self.cell_size
                y1 = i * self.cell_size

                # Draw cell background
                rect = QGraphicsRectItem(x1, y1, self.cell_size, self.cell_size)
                rect.setBrush(QBrush(Qt.GlobalColor.white))
                rect.setPen(QPen(Qt.GlobalColor.gray))
                self.scene.addItem(rect)

                # Draw walls
                if walls_grid[i][j][0]:  # North wall
                    self.scene.addLine(x1, y1, x1 + self.cell_size, y1, pen)
                if walls_grid[i][j][1]:  # East wall
                    self.scene.addLine(
                        x1 + self.cell_size,
                        y1,
                        x1 + self.cell_size,
                        y1 + self.cell_size,
                        pen,
                    )
                if walls_grid[i][j][2]:  # South wall
                    self.scene.addLine(
                        x1,
                        y1 + self.cell_size,
                        x1 + self.cell_size,
                        y1 + self.cell_size,
                        pen,
                    )
                if walls_grid[i][j][3]:  # West wall
                    self.scene.addLine(x1, y1, x1, y1 + self.cell_size, pen)

                # Draw chips
                chip = chips_grid[i][j]
                if chip[0] is not None and chip[1] is not None:
                    self.draw_shape(x1, y1, chip[0], chip[1], (i, j))

                # Draw mirrors
                mirror = mirrors_grid[i][j]
                if mirror[0] is not None and mirror[1] is not None:
                    color = GameWindow.get_color(mirror[0])
                    angle = mirror[1]
                    mirror_pen = QPen(color)
                    mirror_pen.setWidth(3)  # Set thickness to 3 pixels for mirrors

                    margin = self.cell_size * 0.1  # 10% of the cell size

                    if angle == 45:
                        self.scene.addLine(
                            x1 + margin,
                            y1 + margin,
                            x1 + self.cell_size - margin,
                            y1 + self.cell_size - margin,
                            mirror_pen,
                        )
                    elif angle == 135:
                        self.scene.addLine(
                            x1 + self.cell_size - margin,
                            y1 + margin,
                            x1 + margin,
                            y1 + self.cell_size - margin,
                            mirror_pen,
                        )

        # Draw pawns
        for idx, (row, col) in enumerate(self.runtime.pawns):
            x_center = col * self.cell_size + self.cell_size / 2
            y_center = row * self.cell_size + self.cell_size / 2
            self.draw_pawn(x_center, y_center, idx)

            # Check if the pawn is over a chip and make the chip transparent
            for (chip_row, chip_col), chip_item in self.chip_items:
                if chip_row == row and chip_col == col:
                    chip_item.setOpacity(0.8)  # Set chip to 80% transparent

    def draw_pawn(self, x_center, y_center, color_code):
        color = GameWindow.get_color(color_code)
        # Create the chess pawn shape using QPainterPath
        pawn_path = QPainterPath()
        base_radius = self.cell_size / 4
        head_radius = base_radius / 1.5

        # Draw base (rectangle base for pawn)
        pawn_path.addEllipse(
            x_center - base_radius,
            y_center - base_radius,
            2 * base_radius,
            base_radius,
        )
        # Draw head (circle)
        pawn_path.addEllipse(
            x_center - head_radius,
            y_center - base_radius - head_radius,
            2 * head_radius,
            2 * head_radius,
        )

        pawn_item = QGraphicsPathItem(pawn_path)
        pawn_item.setBrush(QBrush(color))
        self.scene.addItem(pawn_item)

    def draw_shape(self, x, y, color_code, shape_code, coords=None):
        item = None
        color = GameWindow.get_color(color_code)
        shape = GameWindow.get_shape(shape_code)
        if shape == "circle":
            radius_offset = 5
            item = QGraphicsEllipseItem(
                x + radius_offset,
                y + radius_offset,
                self.cell_size - 2 * radius_offset,
                self.cell_size - 2 * radius_offset,
            )
        elif shape == "square":
            item = QGraphicsRectItem(
                x + 5, y + 5, self.cell_size - 10, self.cell_size - 10
            )
        elif shape == "triangle":
            item = QGraphicsPolygonItem()
            points = [
                QPointF(x + self.cell_size / 2, y + 5),
                QPointF(x + 5, y + self.cell_size - 5),
                QPointF(x + self.cell_size - 5, y + self.cell_size - 5),
            ]
            item.setPolygon(QPolygonF(points))
        elif shape == "star":
            item = QGraphicsPolygonItem()
            # Define points for a proper five-pointed star
            points = [
                QPointF(x + self.cell_size / 2, y + 5),  # Top point
                QPointF(
                    x + self.cell_size * 0.6, y + self.cell_size * 0.4
                ),  # Right upper inner
                QPointF(
                    x + self.cell_size - 5, y + self.cell_size * 0.4
                ),  # Right outer
                QPointF(
                    x + self.cell_size * 0.7, y + self.cell_size * 0.65
                ),  # Right lower inner
                QPointF(
                    x + self.cell_size * 0.8, y + self.cell_size - 5
                ),  # Bottom right
                QPointF(
                    x + self.cell_size / 2, y + self.cell_size * 0.8
                ),  # Bottom center
                QPointF(
                    x + self.cell_size * 0.2, y + self.cell_size - 5
                ),  # Bottom left
                QPointF(
                    x + self.cell_size * 0.3, y + self.cell_size * 0.65
                ),  # Left lower inner
                QPointF(x + 5, y + self.cell_size * 0.4),  # Left outer
                QPointF(
                    x + self.cell_size * 0.4, y + self.cell_size * 0.4
                ),  # Left upper inner
            ]
            item.setPolygon(QPolygonF(points))

        if item is not None:
            item.setBrush(QBrush(color))
            self.scene.addItem(item)
            if coords:
                self.chip_items.append((coords, item))
        return item

    def draw_goal(self):
        target_color_code = self.runtime.current_target[0]
        target_shape_code = self.runtime.current_target[1]

        # Create a goal text label
        goal_text_item = QGraphicsTextItem()
        goal_text_item.setPlainText("Goal: Move ")
        goal_text_item.setDefaultTextColor(Qt.GlobalColor.black)
        goal_text_item.setPos(10, -40)  # Position above the board
        self.scene.addItem(goal_text_item)

        # Create a graphical representation for the pawn
        self.draw_pawn(98, -25, target_color_code)

        # Create a text label for "to"
        to_text_item = QGraphicsTextItem()
        to_text_item.setPlainText(" to ")
        to_text_item.setDefaultTextColor(Qt.GlobalColor.black)
        to_text_item.setPos(110, -40)  # Position after the pawn
        self.scene.addItem(to_text_item)

        # Create a graphical representation for the target shape
        x1, y1 = 130, -45
        target_item = self.draw_shape(x1, y1, target_color_code, target_shape_code)
        if target_item:
            target_item.setZValue(10)
        else:
            print("Error: Target shape not found")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())
