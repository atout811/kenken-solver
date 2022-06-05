import pygame
from collections import OrderedDict

def draw_grid(screen, screen_width, screen_height, grid_size):
    """
    Function that draws grid_size x grid_size grid on the screen
    """
    block_size = int(screen_width/grid_size) #Set the size of the grid block
    num_squares = screen_width/block_size
    count = 0
    for x in range(0, screen_width, block_size):
        for y in range(0, screen_height, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            font = pygame.font.SysFont("comicsansms", 20)
            pygame.draw.rect(screen, (50,50,50), rect, 1)

def draw_cages(screen, screen_width, screen_height, grid_size, grids):
    """
    Function that draws the kenken puzzle cages on the screen
    Important Args:
        grids (list of tuples): that contains positions of the kenken puzzle cages, the number to display and operator
        grids example for 3x3 puzzle:
        [(((1, 1), (2, 1), (3, 1)), '*', 6), (((1, 2), (2, 2), (3, 2)), '+', 6), (((1, 3), (2, 3), (3, 3)), '+', 6)]
    """
    block_size = int(screen_width/grid_size) #Set the size of the grid block
    point_map = OrderedDict()
    rectangle_map = OrderedDict()
    lines_map = OrderedDict()
    x = 0
    y = 0
    count = 0
    for r in range(1, grid_size+1):
        for c in range(1, grid_size+1):
            count+=1
            point_map[(r,c)] = (x,y) # map (row, column) values to rectangle center
            p1,p2,p3,p4 = (x,y),(x+block_size,y),(x+block_size, y+block_size),(x, y+block_size)
            rectangle_map[(r,c)] = [p1,p2,p3,p4]
            lines_map[(r,c)] = [(p1,p2), (p2,p3), (p3,p4), (p4,p1)] 
            x = x + block_size
        x = 0
        y = y + block_size

    # looping through the grid required to be drawn
    to_draw = []
    for item in grids:
        to_draw = []
        marked = []
        points, op, num = item
        for point in points:
            for line in lines_map[point]:
                if line not in to_draw:
                    to_draw.append(line)

        for item in to_draw:
            x = ((item[1], item[0]))
            if x in to_draw:
                marked.append(item)

        for item in to_draw:
            if item not in marked:
                pygame.draw.line(screen, (0,0,0), item[0], item[1], 10)

        # assigning operator and number to cage        
        pygame.font.init()
        font = pygame.font.SysFont("comicsansms", 20)
        text = font.render(str(num)+op, True, (0,0,0))
        text_rect = text.get_rect()
        t1, t2 = point_map[points[0]] 
        text_rect.center = (t1+25, t2+20) # 1st grid in cage
        screen.blit(text, text_rect)
    return point_map
        
def populate_grid(screen, screen_width, screen_height, grid_size, solution, point_map):
    """
    Function that fills the grid with the required solution
    Expected input format for "solution" - it should be a list of pairs of ((row_number, column_number), value):
        [((row,column),value)]
    """
    block_size = int(screen_width/grid_size) #Set the size of the grid block
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 50)
    for pair in solution:
        value = pair[1]
        grid = pair[0]
        text = font.render(str(value), True, (220,20,60))
        text_rect = text.get_rect()
        t1, t2 = point_map[grid] 
        text_rect.center = (t1+block_size/2, t2+block_size/2) # 1st grid in cage 
        screen.blit(text, text_rect)

