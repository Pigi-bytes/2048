import sys
import random
import os
import json

from time import sleep
from PyQt6 import uic, QtWidgets
from PyQt5.QtCore import Qt

from constante import *



class Cell:
    def __init__(self, ID, label, frame):
        self.id = ID
        self.value =  0

        self.label = label
        self.frame = frame

    def update(self):

        fg = COLOR_FG[2] if self.value >= 8 else COLOR_FG[1]
        self.label.setStyleSheet(f"color: {fg}")

        bg = COLOR_LEFT
        if self.value in COLOR_BG.keys():
            bg = COLOR_BG[self.value]

        if self.value == 0:
            self.label.setText("")
        else:
            self.label.setText(str(self.value))

        self.frame.setStyleSheet(f"background-color: {bg}; border-radius: 5px;")

        
class board:

    def __init__(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY

        self.score = 0
        with open('data\score.json', 'r') as f:
            self.best_score = json.load(f)["best_score"]
        
    def generate_matrix(self, liste_label, liste_frame):
        self.matrix = []
        for i in range(16):
            self.matrix.append(Cell(i, liste_label[i], liste_frame[i]))

    def print_matrix(self,):
        for cell in self.matrix:
            cell.update()

    def generate_new_case(self,):
        liste_empty_cell = [cell.id for cell in self.matrix if cell.value == 0]
        if len(liste_empty_cell) == 0:
            with open('data\score.json', 'w') as f:

                json.dump({"best_score": self.best_score}, f)
            raise ("Game over")

        r_cell_id = random.choice(liste_empty_cell)
        r_cell_value = random.random()
        if r_cell_value <= 0.1:
            r_cell_value = 4
        else:
            r_cell_value = 2

        self.matrix[r_cell_id].value = r_cell_value

    def compress_vertical(self, direction):
        for row in range(self.sizeY):
            line_gen = range(row, len(self.matrix), self.sizeY)
            if direction == "down":
                line_gen = reversed(line_gen)

            self.compress_fusion(line_gen)

    def compress_horizontal(self, direction):
        for column in range(0, len(self.matrix), self.sizeY):
            line_gen = range(column, column+self.sizeY, 1)
            if direction == "left":
                line_gen = reversed(line_gen)
            self.compress_fusion(line_gen)

    def compress_fusion(self, liste_generator):
        line = [self.matrix[index] for index in liste_generator]

        line = self.two_pointer_algo(line)
        self.fusion(line)
        line = self.two_pointer_algo(line)

    def two_pointer_algo(self, liste):
        left = right = 0
        while right < len(liste):
            if liste[right].value == 0:
                right += 1
            else:

                liste[left].value, liste[right].value = liste[right].value, liste[left].value
                right += 1
                left += 1

        return liste

    def fusion(self, liste):
        for index in range(len(liste)-1):
            cell_0, cell_1 = liste[index], liste[index+1]

            if cell_0.value == cell_1.value:
                cell_0.value *= 2
                cell_1.value = 0
                self.add_score(cell_0.value)
    
    def add_score(self, value):
        self.score += value
        if self.score > self.best_score:
            self.best_score = self.score


class Ui_board(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_board, self).__init__()
        uic.loadUi("GUI/test.ui", self)

        self.score = self.findChild(QtWidgets.QLabel, "label_score_nb")
        self.bscore = self.findChild(QtWidgets.QLabel, "label_bscore_nb")
        self.liste_frame = [self.findChild(QtWidgets.QFrame, f"frame{i}") for i in range(16)]
        self.liste_label = [self.findChild(QtWidgets.QLabel, f"label_{i}") for i in range(16)]

        self.init_board()

    def init_board(self):
        self.game = board(4, 4)
        self.set_score()
        self.game.generate_matrix(self.liste_label, self.liste_frame)
        self.game.generate_new_case()
        self.game.generate_new_case()

        self.game.print_matrix()

    def set_score(self):
        self.score.setText(str(self.game.score))
        self.bscore.setText(str(self.game.best_score))

    def keyPressEvent(self, event):
        key = event.key()
        
        if key in (Qt.Key_Up, Qt.Key_Down, Qt.Key_Right, Qt.Key_Left):
            if key == Qt.Key_Up:
                self.game.compress_vertical('up')
            elif key == Qt.Key_Down:
                self.game.compress_vertical('down')
            elif key == Qt.Key_Right:
                self.game.compress_horizontal("left")
            elif key == Qt.Key_Left:
                self.game.compress_horizontal("right")

            self.game.generate_new_case()
            self.game.print_matrix()
            self.set_score()





if __name__ == "__main__":
    # Create an instance of QApplication
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_board()
    window.show()
    sys.exit(app.exec())
