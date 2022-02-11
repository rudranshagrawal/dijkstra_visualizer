"""
Trivial Implementation of Dijkstra's Algorithm
Author: Rudransh Agrawal
"""
import pygame
import sys
from collections import deque

# Define some colors
BLACK = (0, 0, 0)
WHITE = (60, 60, 60)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# This sets the margin between each cell
MARGIN = 0

# Set the COLUMNS and ROWS of the screen
COLUMNS, ROWS = 64, 48
# This sets the WIDTH and HEIGHT of each grid location
WINDOW_SIZE = [GAME_WIDTH, GAME_HEIGHT] = [640, 480]
WIDTH, HEIGHT = GAME_WIDTH // COLUMNS, GAME_HEIGHT // ROWS

# Set the HEIGHT and WIDTH of the screen
screen = pygame.display.set_mode(WINDOW_SIZE)


class Node:
    def __init__(self, i, j):
        self.row, self.column = i, j
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False
        self.isStart = False
        self.isEnd = False

    def add_neighbors(self, grid):
        if self.row < ROWS - 1:
            self.neighbors.append(grid[self.row + 1][self.column])
        if self.row > 0:
            self.neighbors.append(grid[self.row - 1][self.column])
        if self.column < COLUMNS - 1:
            self.neighbors.append(grid[self.row][self.column + 1])
        if self.column > 0:
            self.neighbors.append(grid[self.row][self.column - 1])


# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
# To pop elements in O(1) Time
queue = deque()
visited = []
path = []
grid = []

# Add a Node Object to eachpoint in grid
for row in range(ROWS):
    arr = []
    for column in range(COLUMNS):
        arr.append(Node(row, column))
    grid.append(arr)

# Make Adjacency List
for row in range(ROWS):
    for column in range(COLUMNS):
        grid[row][column].add_neighbors(grid)


# Initialize pygame
pygame.init()

# Set title of screen
pygame.display.set_caption("Dijkstra's Visualization")

# Flag to Indicate Start of Implementation
startFlag = False

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


def setWall(pos, isWall):
    column = pos[0] // HEIGHT
    row = pos[1] // WIDTH
    grid[row][column].wall = isWall


start = grid[0][0]
start.isStart = 1
end = grid[29][55]
end.isEnd = 1
queue.append(start)
start.visited = True
completionFlag = False


# -------- Main Program Loop -----------


while True:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            # done = True  # Flag that we are done so we exit this loop
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            setWall(pygame.mouse.get_pos(), 1)
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0] or event.buttons[2]:
                setWall(pygame.mouse.get_pos(), 1)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                startFlag = True

    # Implement Dijkstra

    if startFlag:
        if len(queue) > 0:
            current = queue.popleft()
            if current == end:
                temp = current
                while temp.prev:
                    path.append(temp.prev)
                    temp = temp.prev
                if not completionFlag:
                    completionFlag = True
            if not completionFlag:
                for i in current.neighbors:
                    if not i.visited and not i.wall:
                        i.visited = True
                        i.prev = current
                        queue.append(i)

    # Set the screen background
    screen.fill(WHITE)

    # Draw the grid
    for row in range(ROWS):
        for column in range(COLUMNS):
            color = (0, 0, 0)
            if grid[row][column].wall == 1:
                color = BLUE
            if grid[row][column].visited == 1:
                color = GREEN
            if grid[row][column].isStart == 1:
                color = RED
            if grid[row][column].isEnd == 1:
                color = RED
            pygame.draw.rect(screen, color, [WIDTH * column, HEIGHT * row, WIDTH - 1, HEIGHT - 1])
            if grid[row][column] in path:
                pygame.draw.rect(screen, RED, [WIDTH * column, HEIGHT * row, WIDTH - 1, HEIGHT - 1])
                # pygame.draw.circle(screen, WHITE, (column * WIDTH + WIDTH // 2, row * HEIGHT + HEIGHT // 2), WIDTH // 3)

    # grid[0][0] = 0
    # Limit to 60 frames per second
    # clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
# pygame.quit()
