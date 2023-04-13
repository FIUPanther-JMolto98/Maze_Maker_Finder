from threading import current_thread
import pygame
import pygame.freetype
import tkinter as tk
from tkinter import filedialog
from functools import partial
root = tk.Tk()
root.withdraw()
import math
import random
from collections import deque
from queue import PriorityQueue
import heapq

pygame.init()

HEIGHT = 1000
WIDTH = 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze Maker Solver')
font = pygame.freetype.SysFont('Calibri', 6)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
LIGHT_GREY = (204, 204, 204)
GREY = (128, 128, 128)
DARK_GREY = (104, 104, 104)
TURQUOISE = (64, 224, 208)

def instructions():
    menu_window = pygame.display.set_mode((WIDTH, WIDTH))
    instructions_heading = pygame.font.SysFont('Impact', 30)
    instructions_font = pygame.font.SysFont('Calibri', 30)
    instructions_text1 = instructions_heading.render('INSTRUCTIONS:', True, (245,188,66))
    instructions_text2 = instructions_font.render('Step 1: Choose Start Point.', True, (230, 115, 115))
    instructions_text3 = instructions_font.render('Step 2: Choose End Point.', True, (115, 171, 230))
    instructions_text4 = instructions_font.render('Step 3: Construct Maze.', True, WHITE)
    instructions_text5 = instructions_heading.render('KEYBOARD CONTROLS:', True, (245,188,66))
    instructions_text6 = instructions_font.render('Press 1: To Apply DFS', True,(230, 115, 115))
    instructions_text7 = instructions_font.render('Press 2: To Apply BFS', True,(115, 171, 230))
    instructions_text8 = instructions_font.render('Press 3: To Apply GRD L1 Norm', True,(153, 230, 115))
    instructions_text9 = instructions_font.render('Press 4: To Apply GRD L2 Norm', True,(153, 230, 115))
    instructions_text10 = instructions_font.render('Press 5: To Apply A* L1 Norm', True,(230, 201, 115))
    instructions_text11 = instructions_font.render('Press 6: To Apply A* L2 Norm', True,(230, 201, 115))
    instructions_text12 = instructions_font.render('Press 7: To Apply BI_DFS', True,(192, 115, 230))
    instructions_text13 = instructions_font.render('Press S: Save Current Maze to TXT File', True, WHITE)
    instructions_text14 = instructions_font.render('Press L: Load Maze from TXT File', True, WHITE)
    instructions_text15 = instructions_font.render('Press R: Generate Random Maze', True, WHITE)
    instructions_text16 = instructions_font.render('Press E: Wipe Screen Clean', True,WHITE)
    instructions_text17 = instructions_font.render('Press C: Clear Solution Visuals (Once Found)', True, WHITE)

 
    instructions_surface = pygame.Surface((WIDTH, WIDTH))
    instructions_surface = pygame.image.load("background_inverted.png")
    instructions_surface = pygame.transform.scale(instructions_surface, (WIDTH, WIDTH))
    instructions_rect = instructions_surface.get_rect()

    instructions_surface.blit(instructions_text1, (50, 50))
    instructions_surface.blit(instructions_text2, (50, 100))
    instructions_surface.blit(instructions_text3, (50, 125))
    instructions_surface.blit(instructions_text4, (50, 150))
    instructions_surface.blit(instructions_text5, (50, 250))
    instructions_surface.blit(instructions_text6, (50, 300))
    instructions_surface.blit(instructions_text7, (50, 325))
    instructions_surface.blit(instructions_text8, (50, 350))
    instructions_surface.blit(instructions_text9, (50, 375))
    instructions_surface.blit(instructions_text10, (50, 400))
    instructions_surface.blit(instructions_text11, (50, 425))    
    instructions_surface.blit(instructions_text12, (50, 450))    
    instructions_surface.blit(instructions_text13, (50, 500))    
    instructions_surface.blit(instructions_text14, (50, 525))    
    instructions_surface.blit(instructions_text15, (50, 550))    
    instructions_surface.blit(instructions_text16, (50, 575))    
    instructions_surface.blit(instructions_text17, (50, 600))    

    back_button_font = pygame.font.SysFont('Impact', 30)
    back_button = pygame.Surface((800, 150))
    back_button.fill(WHITE)
    back_button_text = back_button_font.render('BACK', True, WHITE)
    back_button_rect = back_button_text.get_rect(center=(WIDTH//2, WIDTH - 50))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    return

        
        menu_window.blit(back_button, (WIDTH//2 - back_button.get_width()//2, WIDTH -100 - back_button.get_height()))
        menu_window.blit(back_button_text, back_button_rect.move(WIDTH//2 - back_button_text.get_width()//2, WIDTH -100 - back_button.get_height()))

        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
            back_button_text = back_button_font.render('BACK', True, RED)
        else:
            back_button_text = back_button_font.render('BACK', True, WHITE)
        
        menu_window.blit(instructions_surface, (0, 0))
        menu_window.blit(back_button_text, back_button_rect)
        pygame.display.update()
        
        
        
def menu():
    menu_font = pygame.font.SysFont('Impact', 60)
    menu_button = pygame.Surface((800, 150))
    menu_button.fill(WHITE)
    menu_text = menu_font.render('MAZE MAKER SOLVER', True, BLACK)
    menu_text_rect = menu_text.get_rect(center=menu_button.get_rect().center)
    
    
    
    
    button_font = pygame.font.SysFont('Impact', 50)
    start_button = pygame.Surface((450, 80))
    start_button.fill((81,245,66))
    start_text = button_font.render('START GAME', True, WHITE)
    start_text_rect = start_text.get_rect(center=start_button.get_rect().center)
 
    
    
    
    quit_button = pygame.Surface((450, 80))
    quit_button.fill((245,66,66))
    quit_text = button_font.render('QUIT GAME', True, WHITE)
    quit_text_rect = quit_text.get_rect(center=quit_button.get_rect().center)
    menu_text_rect = menu_text.get_rect(center=(WIDTH//2, WIDTH//4))
    
    instructions_button = pygame.Surface((450, 60))
    instructions_button.fill((245,188,66))
    instructions_text = button_font.render('INSTRUCTIONS', True, WHITE)
    instructions_text_rect = instructions_text.get_rect(center=instructions_button.get_rect().center)

    
    menu_window = pygame.display.set_mode((WIDTH, WIDTH))
    
    while True:
        background_image = pygame.image.load("background.png")
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        background_rect = background_image.get_rect()
        menu_window.blit(background_image, background_rect)
        menu_window.blit(menu_button, (WIDTH//2 - menu_button.get_width()//2, WIDTH//3  - menu_button.get_height()))
        menu_window.blit(menu_text, menu_text_rect)

        menu_window.blit(start_button, (WIDTH//2 - start_button.get_width()//2, WIDTH//1.75 - start_button.get_height()))
        menu_window.blit(quit_button, (WIDTH//2 - quit_button.get_width()//2, WIDTH*3//3.75 - quit_button.get_height()))
        menu_window.blit(start_text, start_text_rect.move(WIDTH//2 - start_button.get_width()//2, WIDTH//1.75 - start_button.get_height()))
        menu_window.blit(quit_text, quit_text_rect.move(WIDTH//2 - quit_button.get_width()//2, WIDTH*3//3.75 - quit_button.get_height()))
        menu_window.blit(instructions_button, (WIDTH//2 - instructions_button.get_width()//2, WIDTH//13 - instructions_button.get_height()))
        menu_window.blit(instructions_text, instructions_text_rect.move(WIDTH//2 - instructions_button.get_width()//2, WIDTH //13 - instructions_button.get_height()))
        
        start_button_rect = start_text.get_rect(center=(WIDTH//2, WIDTH//1.75 - 50))
        quit_button_rect = quit_text.get_rect(center=(WIDTH//2, WIDTH*3//3.75 - 50))
        instructions_button_rect = instructions_text.get_rect(center=(WIDTH//2, WIDTH//13)) ###########################################

        if start_button_rect.collidepoint(pygame.mouse.get_pos()):
            start_text = button_font.render('START GAME', True, (60,148,40))
        else:
            start_text = button_font.render('START GAME', True, WHITE)

        if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
            quit_text = button_font.render('QUIT GAME', True, (148,40,40))
        else:
            quit_text = button_font.render('QUIT GAME', True, WHITE)
                  
            
        if instructions_button_rect.collidepoint(pygame.mouse.get_pos()):
            instructions_text = button_font.render('INSTRUCTIONS', True, (148,107,40))
        else:
            instructions_text = button_font.render('INSTRUCTIONS', True, WHITE)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if start_text_rect.move(WIDTH//2 - start_button.get_width()//2, WIDTH//1.75 - start_button.get_height()).collidepoint(event.pos):
                    return
                elif quit_text_rect.move(WIDTH//2 - quit_button.get_width()//2, WIDTH*3//3.75 - quit_button.get_height()).collidepoint(event.pos):
                    quit()
                elif instructions_text_rect.move(WIDTH//2 - instructions_button.get_width()//2, WIDTH //12 - instructions_button.get_height()).collidepoint(event.pos): ##################################################
                    instructions()
                                          
menu()

def display_error(win, width, message):
    font = pygame.font.SysFont('comicsans', 50)
    text = font.render(message, True, (255, 0, 0))
    win.blit(text, (width // 2 - text.get_width() // 2, width // 2 - text.get_height() // 2))
    pygame.display.update()

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.x = row*width
        self.y = col*width
        self.width = width
        self.row = row
        self.col = col
        self.color = WHITE
        self.neighbors = []
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == LIGHT_GREY

    def is_open(self):
        return self.color == DARK_GREY

    def is_barrier(self):
        return self.color == BLACK
    
    def is_solution(self):
        return self.color == GREEN

    def reset(self):
        self.color = WHITE

    def is_start(self):
        return self.color == RED

    def is_end(self):
        return self.color == BLUE

    def make_closed(self):
        self.color = LIGHT_GREY

    def make_open(self):
        self.color = GREY
        
    def make_closed_DFS(self):
        self.color = "#E67373"

    def make_open_DFS(self):
        self.color = "#E8A9A9"

    def make_closed_BI_DFS_F(self):
        self.color = "#E67373"

    def make_open_BI_DFS_F(self):
        self.color = "#E8A9A9"

    def make_closed_BI_DFS_B(self):
        self.color = "#A9C6E8"

    def make_open_BI_DFS_B(self):
        self.color = "#73ABE6"

    def make_open_BFS(self):
        self.color = "#A9C6E8"

    def make_closed_BFS(self):
        self.color = "#73ABE6"

    def make_open_GRD(self):
        self.color = "#BAE8A9"

    def make_closed_GRD(self):
        self.color = "#99E673"
    
    def make_open_ASTR(self):
        self.color = "#E8DFA9"

    def make_closed_ASTR(self):
        self.color = "#e6c973"
    
    def make_open_DIJK(self):
        self.color = "#E8A9CB"

    def make_closed_DIJK(self):
        self.color = "#E673BE" 

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = RED

    def make_end(self):
        self.color = BLUE

    def make_path(self):
        self.color = GREEN

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col])


        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self, other):
        return False


def L1(p1, p2):  #heuristic function for manhattan distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2)+abs(y1-y2)

def L2(p1, p2):  #heuristic function for euclidean distance
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

def is_solution_path(came_from, current):
    while current in came_from:
        current = came_from[current]
        if current.is_start():
            return True
        current.make_path()
    return False

def reconstruct_path(came_from, current, draw):
    while(current in came_from):
        current = came_from[current]
        current.is_solution_path = True
        current.make_path()
        draw()
def reconstruct_path_bi(forward_came_from, backward_came_from, forward_intersection, backward_intersection, draw):
    current = forward_intersection
    while current in forward_came_from:
        current = forward_came_from[current]
        current.is_solution_path = True
        current.make_path()
        draw()

    current = backward_intersection
    while current in backward_came_from:
        current = backward_came_from[current]
        current.is_solution_path = True
        current.make_path()
        draw()

    forward_intersection.is_solution_path = True
    forward_intersection.make_path()
    backward_intersection.is_solution_path = True
    backward_intersection.make_path()
    draw()

def DFS(draw, grid, start, end):
    clear_solution_path(grid, start, end)
    stack = [start]
    visited = {start}
    came_from = {}
    while stack:
        current = stack.pop()
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                visited.add(neighbor)
                stack.append(neighbor)
                neighbor.make_open_DFS()
        
        draw()
        if current != start:
            current.make_closed_DFS()

    return False

def BI_DFS(draw, grid, start, end):
    clear_solution_path(grid, start, end)

    forward_stack = [start]
    forward_visited = {start}
    forward_came_from = {}

    backward_stack = [end]
    backward_visited = {end}
    backward_came_from = {}

    while forward_stack and backward_stack:
        forward_current = forward_stack.pop()
        backward_current = backward_stack.pop()

        for direction in [forward_current, backward_current]:
            if direction == forward_current:
                stack, visited, came_from, other_visited, other_came_from = forward_stack, forward_visited, forward_came_from, backward_visited, backward_came_from
            else:
                stack, visited, came_from, other_visited, other_came_from = backward_stack, backward_visited, backward_came_from, forward_visited, forward_came_from

            for neighbor in direction.neighbors:
                if neighbor not in visited:
                    if neighbor in other_visited:

                        reconstruct_path_bi(forward_came_from, backward_came_from, direction, neighbor, draw)
                        start.make_start()
                        end.make_end()
                        return True

                    came_from[neighbor] = direction
                    visited.add(neighbor)
                    stack.append(neighbor)
                    if direction == forward_current:
                        neighbor.make_open_BI_DFS_F()
                    elif direction == backward_current:
                        neighbor.make_open_BI_DFS_B()

        draw()

        if forward_current != start:
            forward_current.make_closed_BI_DFS_F()

        if backward_current != end:
            backward_current.make_closed_BI_DFS_B()

    return False

def BFS(draw, grid, start, end):
    clear_solution_path(grid, start, end)
    queue = deque([start])
    visited = {start}
    came_from = {}
    
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = queue.popleft()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                came_from[neighbor] = current
                neighbor.make_open_BFS()
        
        draw()
        
        if current != start:
            current.make_closed_BFS()
        
    return False

def GRD_L1(draw, grid, start, end):
    clear_solution_path(grid, start, end)
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = L1(start.get_pos(), end.get_pos())

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_f_score = L1(neighbor.get_pos(), end.get_pos())
            if temp_f_score < f_score[neighbor]:
                came_from[neighbor] = current
                f_score[neighbor] = temp_f_score
                if neighbor not in open_set.queue:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    neighbor.make_open_GRD()

        draw()
        if current != start:
            current.make_closed_GRD()

    return False

def GRD_L2(draw, grid, start, end):
    clear_solution_path(grid, start, end)
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = L2(start.get_pos(), end.get_pos())

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_f_score = L2(neighbor.get_pos(), end.get_pos())
            if temp_f_score < f_score[neighbor]:
                came_from[neighbor] = current
                f_score[neighbor] = temp_f_score
                if neighbor not in open_set.queue:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    neighbor.make_open_GRD()

        draw()
        if current != start:
            current.make_closed_GRD()

    return False

def AST_L1(draw, grid, start, end):
    clear_solution_path(grid, start, end)
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float('inf') for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = L1(start.get_pos(), end.get_pos())
    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    L1(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open_ASTR()

        draw()
        if current != start:
            current.make_closed_ASTR()

    return False

def AST_L2(draw, grid, start, end):
    clear_solution_path(grid, start, end)
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float('inf') for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = L2(start.get_pos(), end.get_pos())
    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    L2(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open_ASTR()

        draw()
        if current != start:
            current.make_closed_ASTR()

    return False

def make_grid(rows, width):
    grid = []
    gap = width//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            spot.is_solution_path = False
            grid[i].append(spot)
    return grid

def generate_random_maze(rows, width):
    grid = make_grid(rows, width)
    for row in grid:
        for spot in row:
            if random.random() < 0.3:
                spot.make_barrier()

    start = random.choice(random.choice(grid))
    start.make_start()

    end = random.choice(random.choice(grid))
    while end == start:
        end = random.choice(random.choice(grid))
    end.make_end()
    
    return start, end, grid

def draw_grid(win, rows, width, height):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for i in range(rows):
            pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, height))

def draw(win, grid, rows, width):
    grid_area = pygame.Rect(0, 0, width, width)
    pygame.draw.rect(win, WHITE, grid_area)
    
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width//rows
    y, x = pos
    row = y//gap
    col = x//gap

    return row, col

def save_maze(grid):
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    if filename:
        with open(filename, 'w') as f:
            for row in grid:
                for spot in row:
                    if spot.is_barrier():
                        f.write('1')
                    elif spot.is_start():
                        f.write('S')
                    elif spot.is_end():
                        f.write('E')
                    else:
                        f.write('0')
                f.write('\n')


def load_maze(grid):
    filename = filedialog.askopenfilename(initialdir="./", title="Select file",
                                                          filetypes=(("text files", "*.txt"), ("all files", "*.*")))                   
    if filename:
        try:
            start, end = load_maze_from_file(filename, grid)
            return start, end, grid
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))

def load_maze_from_file(filename, grid):
    with open(filename, 'r') as f:
        text = f.read()
        text = text.strip().split('\n')
        start = None
        end = None
        for y, row in enumerate(text):
            for x, char in enumerate(row):
                if char == '1':
                    grid[y][x].make_barrier()
                elif char == 'S':
                    grid[y][x].make_start()
                    start = grid[y][x]
                elif char == 'E':
                    grid[y][x].make_end()
                    end = grid[y][x]
    return start, end

def clear_grid(grid, start, end):
    for row in grid:
        for spot in row:
            if not spot.is_barrier() and not spot.is_start() and not spot.is_end():
                spot.reset()
                spot.color = WHITE
    start.make_start()
    end.make_end()
    return start,end,grid

def erase_grid(grid,start,end):
    start = None
    end = None
    grid = make_grid(ROWS, width)
    return grid,start,end

def clear_solution_path(grid, start, end):
    for row in grid:
        for spot in row:
            if spot.is_solution():
                spot.reset()
                spot.color = LIGHT_GREY
    start.make_start()
    end.make_end()
    return start,end,grid

def main(win, width, height):
    pygame.display.set_mode((WIDTH, HEIGHT))
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None
    run = True
    started = False

    def draw_buttons(surface, height):
        mouse_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - width)
        button_height = 40
        button_width = 120
        button_rows = 4
        button_cols = 3
        border_color = (255,255,255)
        button_color = (0,0,0)
        font_color = (255, 255, 255)
        border_width = 2

        total_button_width = button_cols * button_width
        total_space = width - total_button_width
        padding = total_space // (button_cols + 1)

        font = pygame.font.SysFont('Impact', 24)

        buttons = []
        
        extra_padding = 20

        for i in range(button_rows):
            for j in range(button_cols):
                x = padding + j * (button_width + padding)
                y = padding - 100 + i * (button_height + 10)
                button_label = f"Button {i * button_cols + j + 1}"
                button_action = f"button_{i * button_cols + j + 1}"
                
                buttons.append({'label': button_label, 'pos': (x, y), 'action': button_action, 'color': button_color, 'hover':False})

        buttons[0]['label'] = 'SAVE'
        buttons[0]['action'] = 'save'

        buttons[1]['label'] = 'DFS'
        buttons[1]['action'] = 'dfs'

        buttons[2]['label'] = 'BFS'
        buttons[2]['action'] = 'bfs'

        buttons[3]['label'] = 'LOAD'
        buttons[3]['action'] = 'load'

        buttons[4]['label'] = 'GRD_L1'
        buttons[4]['action'] = 'grd_l1'

        buttons[5]['label'] = 'GRD_L2'
        buttons[5]['action'] = 'grd_l2'

        buttons[6]['label'] = 'RANDOM'
        buttons[6]['action'] = 'random'

        buttons[7]['label'] = 'AST_L1'
        buttons[7]['action'] = 'ast_l1'

        buttons[8]['label'] = 'AST_L2'
        buttons[8]['action'] = 'ast_l2'

        buttons[9]['label'] = 'WIPE'
        buttons[9]['action'] = 'wipe'

        buttons[10]['label'] = 'BI_DFS'
        buttons[10]['action'] = 'bi_dfs'

        buttons[11]['label'] = 'CLEAR_SOL'
        buttons[11]['action'] = 'clear_sol'

        default_colors = {
            'SAVE': {'border': (255, 255, 255), 'button': (0, 0, 0), 'font': (255, 255, 255)},
            'LOAD': {'border': (255, 255, 255), 'button': (0, 0, 0), 'font': (255, 255, 255)},
            'RANDOM': {'border': (255, 255, 255), 'button': (0, 0, 0), 'font': (255, 255, 255)},
            'WIPE': {'border': (255, 0, 0), 'button': (0, 0, 0), 'font': (255, 0, 0)},
            'DFS': {'border': (230, 115, 115), 'button': (0, 0, 0), 'font': (230, 115, 115)},
            'BFS': {'border': (115, 171, 230), 'button': (0, 0, 0), 'font': (115, 171, 230)},
            'GRD_L1': {'border': (153, 230, 115), 'button': (0, 0, 0), 'font': (153, 230, 115)},
            'GRD_L2': {'border': (153, 230, 115), 'button': (0, 0, 0), 'font': (153, 230, 115)},
            'AST_L1': {'border': (230, 201, 115), 'button': (0, 0, 0), 'font': (230, 201, 115)},
            'AST_L2': {'border': (230, 201, 115), 'button': (0, 0, 0), 'font': (230, 201, 115)},
            'BI_DFS': {'border': (192, 115, 230), 'button': (0, 0, 0), 'font': (192, 115, 230)},
            'CLEAR_SOL': {'border': (0, 0, 0), 'button': (0, 0, 0), 'font': (255, 255, 0)}
        }
        
        hover_colors = {
            'SAVE': {'border': (255, 255, 255), 'button': (255, 255, 255), 'font': (0, 0, 0)},
            'LOAD': {'border': (255, 255, 255), 'button': (255, 255, 255), 'font': (0, 0, 0)},
            'RANDOM': {'border': (255, 255, 255), 'button': (255, 255, 255), 'font': (0, 0, 0)},
            'WIPE': {'border': (255, 0, 0), 'button': (255, 0, 0), 'font': (255, 255, 255)},
            'DFS': {'border': (230, 115, 115), 'button': (230, 115, 115), 'font': (255, 255, 255)},
            'BFS': {'border': (115, 171, 230), 'button': (115, 171, 230), 'font': (255, 255, 255)},
            'GRD_L1': {'border': (153, 230, 115), 'button': (153, 230, 115), 'font': (255, 255, 255)},
            'GRD_L2': {'border': (153, 230, 115), 'button': (153, 230, 115), 'font': (255, 255, 255)},
            'AST_L1': {'border': (230, 201, 115), 'button': (230, 201, 115), 'font': (255, 255, 255)},
            'AST_L2': {'border': (230, 201, 115), 'button': (230, 201, 115), 'font': (255, 255, 255)},
            'BI_DFS': {'border': (192, 115, 230), 'button': (192, 115, 230), 'font': (255, 255, 255)},
            'CLEAR_SOL': {'border': (255, 255, 0), 'button': (255, 255, 0), 'font': (0, 0, 0)}
        }


        for button in buttons:
            button_rect = pygame.Rect(button['pos'], (button_width, button_height))
            button['hover'] = button_rect.collidepoint(mouse_pos)
            
            if button['hover']:
                border_color = hover_colors[button['label']]['border']
                button_color = hover_colors[button['label']]['button']
                font_color = hover_colors[button['label']]['font']
            else:
                border_color = default_colors[button['label']]['border']
                button_color = default_colors[button['label']]['button']
                font_color = default_colors[button['label']]['font']

            text = font.render(button['label'], True, font_color)
            pygame.draw.rect(surface, border_color, button_rect, border_width)
            fill_rect = pygame.Rect(button['pos'][0] + border_width, button['pos'][1] + border_width,
                                button_width - 2 * border_width, button_height - 2 * border_width)
            pygame.draw.rect(surface, button_color, fill_rect)
            text_rect = text.get_rect(center=(button['pos'][0] + button_width // 2, button['pos'][1] + button_height // 2))
            surface.blit(text, text_rect)

    def handle_button_click(pos, width, height):
        button_height = 40
        button_width = 120
        padding = 10
        button_rows = 4
        button_cols = 3
        total_button_width = button_cols * button_width
        total_space = width - total_button_width
        padding = total_space // (button_cols + 1)

        buttons = []
        
        extra_padding = 20

        for i in range(button_rows):
            for j in range(button_cols):
                x = padding + j * (button_width + padding)
                y = padding - 100 + i * (button_height + 10)
                button_label = f"Button {i * button_cols + j + 1}"
                button_action = f"button_{i * button_cols + j + 1}"
                buttons.append({'label': button_label, 'pos': (x, y), 'action': button_action})

        buttons[0]['label'] = 'SAVE'
        buttons[0]['action'] = 'save'

        buttons[1]['label'] = 'DFS'
        buttons[1]['action'] = 'dfs'

        buttons[2]['label'] = 'BFS'
        buttons[2]['action'] = 'bfs'

        buttons[3]['label'] = 'LOAD'
        buttons[3]['action'] = 'load'

        buttons[4]['label'] = 'GRD_L1'
        buttons[4]['action'] = 'grd_l1'

        buttons[5]['label'] = 'GRD_L2'
        buttons[5]['action'] = 'grd_l2'

        buttons[6]['label'] = 'RANDOM'
        buttons[6]['action'] = 'random'

        buttons[7]['label'] = 'AST_L1'
        buttons[7]['action'] = 'ast_l1'

        buttons[8]['label'] = 'AST_L2'
        buttons[8]['action'] = 'ast_l2'

        buttons[9]['label'] = 'WIPE'
        buttons[9]['action'] = 'wipe'

        buttons[10]['label'] = 'BI_DFS'
        buttons[10]['action'] = 'bi_dfs'

        buttons[11]['label'] = 'CLEAR_SOL'
        buttons[11]['action'] = 'clear_sol'

        if pos[1] < width:
            return None

        for button in buttons:
            if button['pos'][0] <= pos[0] <= button['pos'][0] + button_width and \
            button['pos'][1] <= pos[1] - width <= button['pos'][1] + button_height:
                return button['action']
        return None

    while run:
        draw(win, grid, ROWS, width)
        buttons_surface = pygame.Surface((width, height-width))
        buttons_surface = pygame.image.load("background_inverted.png")
        draw_buttons(buttons_surface,height)
        win.blit(buttons_surface,(0,width))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()

                if pos[1] < width:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]

                    if not start and spot != end:
                        start = spot
                        start.make_start()

                    elif not end and spot != start:
                        end = spot
                        end.make_end()

                    elif spot != end and spot != start:
                        spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()

                if pos[1] < width:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    if spot == end:
                        end = None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                button_clicked = handle_button_click(pos,width,WIDTH)
                if button_clicked is not None:
                    if button_clicked == 'save':
                            save_maze(grid)
                    if button_clicked == 'load':
                            start, end, grid = load_maze(grid)
                    if button_clicked == 'random':
                            start, end, grid = generate_random_maze(ROWS, width)
                    if button_clicked == 'wipe':
                        start = None
                        end = None
                        grid = make_grid(ROWS, width)
                    if button_clicked == 'dfs' and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        DFS(lambda: draw(win, grid, ROWS, width),
                                grid, start, end)
                    if button_clicked == 'bfs' and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        BFS(lambda: draw(win, grid, ROWS, width),
                                grid, start, end)
                    if button_clicked == 'grd_l1' and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        GRD_L1(lambda: draw(win, grid, ROWS, width),
                                grid, start, end)
                    if button_clicked == 'grd_l2' and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        GRD_L2(lambda: draw(win, grid, ROWS, width),
                                grid, start, end)
                    if button_clicked == 'ast_l1' and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        AST_L1(lambda: draw(win, grid, ROWS, width),
                                grid, start, end)
                    if button_clicked == 'ast_l2' and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        AST_L2(lambda: draw(win, grid, ROWS, width),
                                grid, start, end)
                    if button_clicked == 'bi_dfs' and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        BI_DFS(lambda: draw(win, grid, ROWS, width),
                                grid, start, end)
                    if button_clicked == 'clear_sol' and start and end:
                        clear_grid(grid,start,end)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    start, end, grid = generate_random_maze(ROWS, width)
                
                if event.key == pygame.K_1 and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    DFS(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)
                
                if event.key == pygame.K_2 and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    BFS(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)
                
                if event.key == pygame.K_3 and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    GRD_L1(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)
                
                if event.key == pygame.K_4 and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    GRD_L2(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)
                
                if event.key == pygame.K_5 and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    AST_L1(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)
                
                if event.key == pygame.K_6 and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    AST_L2(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)                  
                
                if event.key == pygame.K_7 and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    BI_DFS(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)

                if event.key == pygame.K_c:
                    if start and end != None:
                        clear_grid(grid, start, end)
                
                if event.key == pygame.K_e:    
                    if start and end != None:
                        start = None
                        end = None
                        grid = make_grid(ROWS, width)
                
                if event.key == pygame.K_s:
                    save_maze(grid)
                
                if event.key == pygame.K_l:
                    start, end, grid = load_maze(grid)
        pygame.display.update()
main(WIN, WIDTH, HEIGHT)