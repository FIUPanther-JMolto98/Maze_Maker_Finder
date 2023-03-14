from threading import current_thread
import pygame
import pygame.freetype
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()
import math
from queue import PriorityQueue

pygame.init()

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* Path finding Algorithm')
font = pygame.freetype.SysFont('calibri', 6)

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
    menu_font = pygame.font.SysFont('calibri', 60)
    menu_text = menu_font.render('Maze Maker', True, WHITE)
    start_text = menu_font.render('Start Game', True, WHITE)
    quit_text = menu_font.render('Quit Game', True, WHITE)

    # Position the menu items
    menu_text_rect = menu_text.get_rect(center=(WIDTH//2, WIDTH//4))
    start_text_rect = start_text.get_rect(center=(WIDTH//2, WIDTH//2))
    quit_text_rect = quit_text.get_rect(center=(WIDTH//2, WIDTH*3//4))

    # Create a new window for the menu
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
                    # Start the game
                    return
                elif quit_text_rect.collidepoint(mouse_pos):
                    # Quit the game
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

    def reset(self):
        self.color = WHITE

    def is_start(self):
        return self.color == RED

    def is_end(self):
        return self.color == BLUE

    def make_closed(self):
        self.color = LIGHT_GREY

    def make_open(self):
        self.color = DARK_GREY

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
        # down
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():  # up
            self.neighbors.append(grid[self.row-1][self.col])

        # right
        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():  # left
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self, other):
        return False


def h(p1, p2):  # heuristic function for manhattan distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2)+abs(y1-y2)


def reconstruct_path(came_from, current, draw):
    while(current in came_from):
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float('inf') for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
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
                    h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):  # total width here
    grid = []
    gap = width//rows  # width of each spot
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width//rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap),
                         (width, i*gap))  # drawing ROW lines
        for i in range(rows):
            pygame.draw.line(win, GREY, (i*gap, 0),
                             (i*gap, width))  # drawing COL lines


def draw(win, grid, rows, width):  # xommand to draw everything on display
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
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


def load_maze(filename, grid):
      
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
            # [0]==Left click [2]==right click
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                if event.key == pygame.K_s:
                    save_maze(grid)
                if event.key == pygame.K_l:
                    filename = filedialog.askopenfilename(initialdir="./", title="Select file",
                                          filetypes=(("text files", "*.txt"), ("all files", "*.*")))
                    
                    if filename:
                        try:
                            start, end = load_maze(filename, grid)
                        except ValueError as e:
                            tk.messagebox.showerror("Error", str(e))


main(WIN, WIDTH)