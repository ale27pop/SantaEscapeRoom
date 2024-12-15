import pygame

# Initialize Pygame
pygame.init()

# Grid configuration
GRID_ROWS = 10  # Smaller grid size
GRID_COLS = 10
CELL_SIZE = 50  # Smaller cell size

GRID_WIDTH = GRID_COLS * CELL_SIZE
GRID_HEIGHT = GRID_ROWS * CELL_SIZE

STATUS_HEIGHT = 100  # Height of the status section
LEGEND_WIDTH = 250   # Width for the legend

SCREEN_WIDTH = GRID_WIDTH + LEGEND_WIDTH  # Total screen width (legend + grid)
SCREEN_HEIGHT = GRID_HEIGHT + STATUS_HEIGHT  # Total screen height

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Santa's Escape Room")

# Font configuration
font = pygame.font.Font(None, 30)
