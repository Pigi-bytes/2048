from pynput import keyboard
import random
import os
from time import sleep

class Cell:
    def __init__(self, ID):
        self.id = ID
        self.value = 0

class board:
    def __init__(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY

        self.matrix = [Cell(i) for i in range(sizeX*sizeY)]

    def print_matrix(self,):
        for cell in self.matrix:
            if cell.id % self.sizeY == 0:
                print("")
            print(cell.value, end=" | ")
        print("\n" + "_"*14)
             
    def generate_new_case(self,):
        liste_empty_cell = [cell.id for cell in self.matrix if cell.value == 0]
        if len(liste_empty_cell) == 0: raise ("Game over")

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


game = board(4,  4)
game.generate_new_case()
game.print_matrix()
while True:
    
    with keyboard.Events() as events:
        event = events.get()
        os.system("cls")

        if event.key == keyboard.KeyCode.from_char('z'):
            game.compress_vertical('up')

        if event.key == keyboard.KeyCode.from_char('s'):
            game.compress_vertical('down')

        if event.key == keyboard.KeyCode.from_char('d'):
            game.compress_horizontal("left")

        if event.key == keyboard.KeyCode.from_char('q'):
            game.compress_horizontal("right")


    sleep(0.2)
    game.generate_new_case()
    game.print_matrix()

