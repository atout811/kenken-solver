import pygame
import sys
from game_functions import *
from PyQt5 import QtWidgets, uic
from kenken import Kenken, generate, benchmark

# UI window to get user inputs
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('get_input.ui', self)
        self.setWindowTitle("Kenken Puzzle Generator & Solver")
        self.pushButton.clicked.connect(self.save)
        self.show()

    def save(self):
        self.algorithm = self.comboBox.currentText()
        self.grid_size = int(self.plainTextEdit.toPlainText())
        self.get_input = False
        self.close()

    def get_data(self):
        return self.algorithm, self.grid_size, self.get_input
  
# Kenken Puzzle Generator and Solver
def main(grid_size, algorithm):
    restart = False
    pygame.init()
    screen_width = 600
    screen_height = 600
    bg_color = (255, 255, 255)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height))
    size, grid = generate(grid_size)
    assignment, _ = benchmark(Kenken(size, grid), algorithm)

    solution = []
    for keys, values in assignment.items():
        for i, key in enumerate(keys):
            solution.append((key, values[i]))

    # print(solution)
    while True:
        screen.fill(bg_color)
        pygame.display.set_caption("Kenken Puzzle Solver")
        img = pygame.image.load('icon.png')
        pygame.display.set_icon(img)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    restart = True
                    
        if restart == True:
            game()
                
        # Drawing the grid and cages
        draw_grid(screen, screen_width, screen_height, grid_size)
        point_map = draw_cages(screen, screen_width, screen_height, grid_size, grid)

        populate_grid(screen, screen_width, screen_height, grid_size, solution, point_map)
        pygame.display.update()

def game():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
    algorithm, grid_size, get_input = window.get_data()
    #print(get_input, grid_size, algorithm)
    if get_input==False:
        main(grid_size, algorithm)

game()
