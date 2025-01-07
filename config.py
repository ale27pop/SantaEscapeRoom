import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_ROWS, GRID_COLS, CELL_SIZE, COLORS

# Initialize Pygame
pygame.init()

# Grid Configuration (using constants)
GRID_WIDTH = GRID_COLS * CELL_SIZE  # Total grid width
GRID_HEIGHT = GRID_ROWS * CELL_SIZE  # Total grid height

STATUS_HEIGHT = 100  # Height for the status section at the bottom
LEGEND_WIDTH = SCREEN_WIDTH - GRID_WIDTH  # Dynamically calculate legend width

# Screen Configuration (using constants)
SCREEN_WIDTH = max(SCREEN_WIDTH, GRID_WIDTH + LEGEND_WIDTH)  # Ensure screen width accommodates the grid and legend
SCREEN_HEIGHT = GRID_HEIGHT + STATUS_HEIGHT  # Total screen height

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Santa's Escape Room")

# Font Configuration
FONT_SIZE = 30  # Size of the font
font = pygame.font.Font(None, FONT_SIZE)  # Default Pygame font with specified size
