from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import sys, math
import Board
from Search import Search
from Node import Node


class MyWindow(QMainWindow):

    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

    def init(self):
        self.setGeometry(0, 0, self.width, self.height)
        self.show()


class HexBoard(QWidget):

    def __init__(self):
        super().__init__()
        self.search = Search()
        self.offset_x = 100
        self.offset_y = 100
        self.radius = 70
        self.pen = QtGui.QPen(QtGui.QColor(231, 231, 231))
        self.pen.setWidth(3)
        self.brush = QtGui.QBrush(QtGui.QColor(209, 188, 138))
        self.polygons = []
        h = 2 * self.radius
        w = h * (math.sqrt(3) / 2)
        self.setGeometry(0, 0, round(w * 11 + 11 * w / 2) + self.offset_x, int(11 * (3 / 4) * h) + self.offset_y)
        self.setAutoFillBackground(True)

        for i in range(11):
            for j in range(11):
                cx = w * j + i * w / 2
                cy = i * (3 / 4) * h
                polygon = self.get_polygon(6, self.radius, cx, cy)
                self.polygons.append(polygon)

    def get_polygon(self, n, radius, startx, starty):
        polygon = QtGui.QPolygonF()
        w = 360 / n
        for i in range(n):
            t = w * i + 30
            x = self.radius * math.cos(math.radians(t)) + startx
            y = self.radius * math.sin(math.radians(t)) + starty
            polygon.append(QtCore.QPointF(x + self.offset_x, y + self.offset_y))
        return polygon

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        for i in range(11):
            for j in range(11):
                ind = 11 * i + j
                poly = self.polygons[ind]
                if self.search.board.squares[ind] == -1:
                    painter.setBrush(QtGui.QColor(0, 0, 0))
                elif self.search.board.squares[ind] == 1:
                    painter.setBrush(QtGui.QColor(255, 255, 255))
                else:
                    painter.setBrush(self.brush)

                painter.drawPolygon(poly)

    def mousePressEvent(self, event):
        point = QtCore.QPoint(event.x(), event.y())

        for index, shape in enumerate(self.polygons):
            if self.search.board.squares[index] != 0:
                continue
            if shape.containsPoint(point, QtCore.Qt.OddEvenFill):
                self.search.board.make_move(index)
                break

        # engine move for testing
        self.search.max_time = 900
        Node.use_rave = True
        self.search.search()
        best_move = self.search.root.best_child().move
        self.search.board.make_move(best_move)
        self.search.clear()
        self.update()


def window():
    app = QApplication(sys.argv)
    widget = HexBoard()
    widget.setMinimumWidth(800)
    widget.setMinimumHeight(800)
    widget.show()
    sys.exit(app.exec())

def window_test():
    app =QApplication(sys.argv)
    window = MyWindow(200,200)
    window.init()
    sys.exit(app.exec_())



if __name__ == "__main__":
    window_test()
