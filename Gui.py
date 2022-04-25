from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import sys, math
from PyQt5.Qt import *
from Board import *
from Search import Search
from Node import Node
from PyQt5.QtCore import QProcess
from functools import partial
from os import listdir


class HexBoard(QWidget):

    def __init__(self, text_edit: QPlainTextEdit):
        super().__init__()
        background = QtGui.QColor(245, 245, 220)
        self.engine_wins = [0, 0]
        self.engine_names = None
        self.time = 1000
        self.turn = 0
        self.engine_match = False
        self.num_match_games = 1000
        self.played_reverse = False
        self.match_counter = 0
        self.opening_counter = 0
        self.is_thinking = False
        self.text_edit = text_edit
        self.board = Board()
        self.offset_x = 100
        self.offset_y = 100
        self.radius = 50
        self.pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        self.pen.setWidth(4)
        self.brush = QtGui.QBrush(background)
        self.polygons = []
        h = 2 * self.radius
        w = h * (math.sqrt(3) / 2)
        for i in range(11):
            for j in range(11):
                cx = w * j + i * w / 2
                cy = i * (3 / 4) * h
                polygon = self.get_polygon(6, self.radius, cx, cy)
                self.polygons.append(polygon)

        self.engine_one = QProcess()
        self.engine_two = QProcess()

    def get_polygon(self, n, radius, startx, starty):
        polygon = QtGui.QPolygonF()
        w = 360 / n
        for i in range(n):
            t = w * i + 30
            x = self.radius * math.cos(math.radians(t)) + startx
            y = self.radius * math.sin(math.radians(t)) + starty
            polygon.append(QtCore.QPointF(x + self.offset_x, y + self.offset_y))
        return polygon

    def send_command(self, command, engine: QProcess):
        ext = command + "\n"
        engine.write(ext.encode('utf-8'))

    def make_move(self, index):
        self.board.make_move(index)

    def clear_board(self):
        self.board.clear_board()
        self.send_command("clear_board", self.engine_one)
        if self.engine_match:
            self.send_command("clear_board", self.engine_two)

        self.is_thinking = False
        self.update()

    def engine_one_ready(self):
        return self.engines_started[0]

    def engine_two_ready(self):
        return self.engines_started[1]

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        for i in range(11):
            for j in range(11):
                ind = 11 * i + j
                poly = self.polygons[ind]
                if self.board.squares[ind] == -1:
                    painter.setBrush(QtGui.QColor(120, 0, 0))
                elif self.board.squares[ind] == 1:
                    painter.setBrush(QtGui.QColor(0, 0, 120))
                else:
                    painter.setBrush(self.brush)

                painter.drawPolygon(poly)

    def update_match_stats(self):
        if self.board.get_winner() != 0:
            opp = (self.turn + 1) % 2
            self.engine_wins[opp] += 1
            self.match_counter += 1
            if self.played_reverse:
                self.opening_counter += 1
                self.opening_counter = self.opening_counter % 121
                self.played_reverse = False
            else:
                self.played_reverse = True
            if self.match_counter < self.num_match_games:
                self.clear_board()
                self.turn = 1 if self.played_reverse else 0
                self.send_command("move:{}".format(self.opening_counter), self.engine_one)
                self.send_command("move:{}".format(self.opening_counter), self.engine_two)
                self.board.make_move(self.opening_counter)
                self.update()
                self.text_edit.setPlainText("{} {}|{}{}".format(self.engine_names[0],self.engine_wins[0],self.engine_names[1], self.engine_wins[1]))

    def search_with_engine(self):
        # searches with whatever engine's turn it is
        self.update_match_stats()
        if self.turn == 0:
            self.send_command("search:{}".format(self.time), self.engine_one)
            self.is_thinking = True
        else:
            self.send_command("search:{}".format(self.time), self.engine_two)
            self.is_thinking = True
        self.turn = 1 if self.turn == 0 else 0

    def ready_read_one(self):
        message = str(self.engine_one.readAllStandardOutput(), 'utf-8')
        first, second = message.split(":")
        if first == "Move":
            move = int(second)
            self.board.make_move(move)
            self.is_thinking = False
            if self.engine_match:
                self.send_command("move:{}".format(move), self.engine_two)
                self.search_with_engine()
        self.update()

    def ready_read_two(self):
        message = str(self.engine_two.readAllStandardOutput(), 'utf-8')
        print(message)
        first, second = message.split(":")
        if first == "Move":
            move = int(second)
            self.board.make_move(move)
            self.is_thinking = False
            if self.engine_match:
                self.send_command("move:{}".format(move), self.engine_one)
                self.search_with_engine()
        self.update()

    def show_message_box(self, msg):
        box = QMessageBox()
        box.setText(msg)
        box.setStandardButtons(QMessageBox.Ok)

    def mousePressEvent(self, event):
        if self.is_thinking:
            return

        point = QtCore.QPoint(event.x(), event.y())

        for index, shape in enumerate(self.polygons):
            if self.board.squares[index] != 0:
                continue
            if shape.containsPoint(point, QtCore.Qt.OddEvenFill):
                self.board.make_move(index)
                self.send_command("move:{}".format(index), self.engine_one)
                self.send_command("search:{}".format(self.time), self.engine_one)
                self.is_thinking = True
                break

        self.update()


class MyWindow(QMainWindow):

    def __init__(self, width, height):
        super().__init__()
        self.text = QPlainTextEdit()
        self.text.setMaximumHeight(150)
        self.text.setReadOnly(True)
        self.width = width
        self.board = HexBoard(self.text)
        self.engine_match_window = SettWindow(self.board)
        self.height = height
        self.setGeometry(0, 0, width, height)
        layout = QVBoxLayout()
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)

        layout.addWidget(line)
        layout.addWidget(self.board)
        layout.addWidget(line2)

        layout.addWidget(self.text)

        wd = QWidget(self)
        self.setCentralWidget(wd)
        wd.setLayout(layout)

        clear = QAction("Clear", self)
        engine_select = QAction("Select", self)
        engine_select.triggered.connect(self.engine_options)

        clear.setStatusTip('Exit application')
        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('Board')
        engineMenu = menubar.addMenu("Engine")
        match = QAction("Match", self)
        match.triggered.connect(self.start_match)
        engineMenu.addAction(match)
        engineMenu.addAction(engine_select)
        fileMenu.addAction(clear)
        clear.triggered.connect(self.board.clear_board)

    def engine_options(self):
        self.engine_match_window.show()

    def start_match(self):
        self.board.engine_match = True
        self.board.send_command("move:{}".format(self.board.opening_counter), self.board.engine_one)
        self.board.send_command("move:{}".format(self.board.opening_counter), self.board.engine_two)
        self.board.make_move(self.board.opening_counter)
        self.board.update()
        self.board.search_with_engine()


class SettWindow(QMainWindow):

    def __init__(self, board: HexBoard):
        super().__init__()
        self.board = board
        self.dialog = QFileDialog()
        self.setGeometry(0, 0, 600, 600)

        self.files = [f for f in listdir("Engines")]
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMaximum(600000)
        self.slider.setMinimum(1000)
        self.slider_label = QLabel("1000")
        self.slider.valueChanged.connect(self.slider_moved)
        self.engine2_box = QComboBox()
        self.engine_box = QComboBox()
        self.engine_box.addItems(self.files)
        self.engine2_box.addItems(self.files)

        self.start_button = QPushButton("Close")

        layout = QGridLayout()
        layout.addWidget(self.engine_box, 0, 1, 1, 1)
        layout.addWidget(self.engine2_box, 1, 1, 1, 1)
        layout.addWidget(QLabel("Engine1"), 0, 0, 1, 1)
        layout.addWidget(QLabel("Engine2"), 1, 0, 1, 1)
        layout.addWidget(self.slider_label, 3, 1, 1, 1)
        layout.addWidget(self.slider, 3, 2, 1, 1)
        layout.addWidget(self.start_button, 4, 1, 1, 3)
        wd = QWidget()
        self.setCentralWidget(wd)
        wd.setLayout(layout)
        self.start_button.clicked.connect(self.close_window)

    def slider_moved(self, x):
        self.board.time = x
        self.slider_label.setText(str(x))

    def close_window(self):
        path1 = self.engine_box.currentText()
        path2 = self.engine2_box.currentText()
        self.board.engine_one.start("Engines/{}".format(path1))
        self.board.engine_one.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.board.engine_one.waitForStarted()

        self.board.engine_two.start("Engines/{}".format(path2))
        self.board.engine_two.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.board.engine_two.waitForStarted()

        self.board.engine_one.readyRead.connect(self.board.ready_read_one)
        self.board.engine_two.readyRead.connect(self.board.ready_read_two)
        self.board.engine_names = [path1,path2]
        self.close()


def show_window():
    app = QApplication(sys.argv)

    # file = QFile(":/dark.qss")
    # file.open(QFile.ReadOnly | QFile.Text)
    # stream = QTextStream(file)
    # app.setStyleSheet(stream.readAll())

    window = MyWindow(2100, 1600)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # some other test
    # app = QApplication(sys.argv)
    # w = MainWindow()
    # w.show()
    # app.exec_()

    show_window()
