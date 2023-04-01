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

pygame.init()

WIDTH = 800
# HEIGHT = 800 + 60
WIN = pygame.display.set_mode((WIDTH, WIDTH))
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

def menu():
    menu_font = pygame.font.SysFont('Impact', 60)
    menu_text = menu_font.render('Maze Maker Solver', True, WHITE)
    start_text = menu_font.render('Start Game', True, WHITE)
    quit_text = menu_font.render('Quit Game', True, WHITE)


    menu_text_rect = menu_text.get_rect(center=(WIDTH//2, WIDTH//4))
    start_text_rect = start_text.get_rect(center=(WIDTH//2, WIDTH//2))
    quit_text_rect = quit_text.get_rect(center=(WIDTH//2, WIDTH*3//4))


    menu_window = pygame.display.set_mode((WIDTH, WIDTH))

    while True:
        menu_window.fill(BLACK)
        menu_window.blit(menu_text, menu_text_rect)
        menu_window.blit(start_text, start_text_rect)
        menu_window.blit(quit_text, quit_text_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_text_rect.collidepoint(mouse_pos):
                    return
                elif quit_text_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()

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

    draw_grid(win, rows, width, width)  # Pass width as the height parameter
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

# def draw_buttons(win,width):
#     button_font = pygame.font.SysFont('arial', 20)
#     clear_button_rect = pygame.Rect(20, width + 20, 100, 40)
#     pygame.draw.rect(win, GREY, clear_button_rect, border_radius=5)
#     clear_text = button_font.render('Clear Grid', True, BLACK)
#     clear_text_rect = clear_text.get_rect(center=clear_button_rect.center)
#     win.blit(clear_text, clear_text_rect)

def handle_button_click(pos,width):
    x, y = pos
    if y > width + 20 and y < width + 60:
        if x > 20 and x < 120:
            return 'clear'
    return None

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None
    run = True
    started = False

    while run:
        
        draw(win, grid, ROWS, width)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
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
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                if spot == end:
                    end = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                button_clicked = handle_button_click(pos,width)
                if button_clicked == 'clear':
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
main(WIN, WIDTH)