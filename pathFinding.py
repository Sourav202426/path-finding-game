#Path Finding Game using A* Algorithm
import pygame
import heapq
import math

# Window width
width = 400 
rows = 10
# Color definitions for nodes and barriers 
# White - Initial state of all nodes and  unvisited state .
# Orange - start node .
# Purple - end (or goal) node.
# Black - Represents barriers.
# Green - Used to mark open nodes that are actively being considered in the algorithm.
# Red - Marks closed nodes and it  will not be revisited.
# Blue -  final path from the start node to the end node once the shortest path is found.
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
purple = (128, 0, 128)
orange = (255,165,0)
# Define the Node class for each cell in the grid
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = white
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    def get_pos(self):
        return self.row, self.col
    def is_closed(self):
        return self.color == red
    def is_open(self):
        return self.color == green
    def is_barrier(self):
        return self.color == black
    def is_start(self):
        return self.color == orange
    def is_end(self):
        return self.color ==  purple
    def reset(self):
        self.color = white
    def make_start(self):
        self.color = orange
    def make_closed(self):
        self.color = red
    def make_open(self):
        self.color = green
    def make_barrier(self):
        self.color = black
    def make_end(self):
        self.color =  purple
    def make_path(self):
        self.color = blue

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    # Add neighboring nodes (down, up, right, left) if they are within bounds and not barriers
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): 
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): 
            self.neighbors.append(grid[self.row][self.col - 1])
# Initialize the grid
def make_grid(rows, width):
    grid = []
    gap = width// rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid
# Heuristic function 
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
    
# A* Algorithm implementation
def a_star_algorithm(draw, grid, start, end):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}
    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()   
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)
        if current == end:
            reconstruct_path(came_from, end, draw, start)
            end.make_end()  
            start.make_start() 
            return True 
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()             
        draw()
        if current != start:
            current.make_closed()      
    return False

# Function to reconstruct path after finding the solution
def reconstruct_path(came_from, current, draw, start):
    while current in came_from:
        current = came_from[current]
        if current != start:  # Skip recoloring the start node
            current.make_path()
            draw()  # Update the display to show the path
            pygame.time.delay(50)  # Delay in milliseconds (50ms delay between each step of the path)


# Draw the grid lines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, black, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, black, (j * gap, 0), (j * gap, width))

# Main draw function
def draw(win, grid, rows, width):
    win.fill(white)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

# Get the mouse position on the grid
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

# Main function
def main(win, width):
    grid = make_grid(rows, width)
    start = None
    end = None
    run = True
    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:  # Left mouse click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()
            elif pygame.mouse.get_pressed()[2]:  # Right mouse click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    a_star_algorithm(lambda: draw(win, grid, rows, width), grid, start, end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, width)
    pygame.quit()

# Run the program
WIN = pygame.display.set_mode((width, width))
pygame.display.set_caption("A* Pathfinding Algorithm")
main(WIN, width)
