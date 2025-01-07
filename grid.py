import pygame
from constants import COLORS, ELEMENT_COLORS, CLUE_COLORS, GRID_ROWS, GRID_COLS, CELL_SIZE, LEGEND_LABELS

def load_assets():
    """Load and scale assets for the grid elements."""
    santa_image = pygame.image.load("assets/santa.jpg")
    present_image = pygame.image.load("assets/present.jpg")
    obstacle_image = pygame.image.load("assets/flour.jpg")
    exit_image = pygame.image.load("assets/exit.jpg")
    grinch_image = pygame.image.load("assets/grinch.jpg")

    # Scale images to fit the grid cells
    assets = {
        "santa": pygame.transform.scale(santa_image, (CELL_SIZE, CELL_SIZE)),
        "present": pygame.transform.scale(present_image, (CELL_SIZE, CELL_SIZE)),
        "obstacle": pygame.transform.scale(obstacle_image, (CELL_SIZE, CELL_SIZE)),
        "exit": pygame.transform.scale(exit_image, (CELL_SIZE, CELL_SIZE)),
        "grinch": pygame.transform.scale(grinch_image, (CELL_SIZE, CELL_SIZE)),
    }
    return assets

def draw_grid(screen, assets, santa_position, grinch_position, presents, obstacles, exit_point):
    """
    Draws the game grid based on the provided positions for Santa, Grinch, presents, obstacles, and the exit.
    Santa can occupy the same position as an object temporarily (overwriting).
    """
    screen.fill(COLORS["background"])

    # Draw the grid
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, COLORS["grid"], rect, 1)

    # Add proximity indicators for objects
    add_proximity_clues(screen, presents, CLUE_COLORS["cookie_smell"], "top_left")  # Clues for presents
    add_proximity_clues(screen, obstacles, CLUE_COLORS["flour_smell"], "bottom_right")  # Clues for obstacles
    add_proximity_clues(screen, [exit_point], CLUE_COLORS["cold_breeze"], "top_right")  # Clues for exit
    add_proximity_clues(screen, [tuple(grinch_position)], CLUE_COLORS["grinch_sound"], "bottom_left")  # Clues for Grinch

    # Draw game elements, except Santa (drawn last to allow overwriting)
    for present in presents:
        if present != tuple(santa_position):
            screen.blit(assets["present"], (present[1] * CELL_SIZE, present[0] * CELL_SIZE))
    for obstacle in obstacles:
        if obstacle != tuple(santa_position):
            screen.blit(assets["obstacle"], (obstacle[1] * CELL_SIZE, obstacle[0] * CELL_SIZE))
    if exit_point != tuple(santa_position):
        screen.blit(assets["exit"], (exit_point[1] * CELL_SIZE, exit_point[0] * CELL_SIZE))
    if grinch_position != santa_position:
        screen.blit(assets["grinch"], (grinch_position[1] * CELL_SIZE, grinch_position[0] * CELL_SIZE))

    # Draw Santa last (overwriting other objects temporarily)
    screen.blit(assets["santa"], (santa_position[1] * CELL_SIZE, santa_position[0] * CELL_SIZE))

def add_proximity_clues(screen, objects, clue_color, position):
    """
    Adds visual clues dynamically based on proximity to specific elements.
    The clues are placed in specific parts of the adjacent cells:
        - "top_left": cookie smell (present clue)
        - "bottom_right": flour smell (trap)
        - "top_right": cold breeze (exit)
        - "bottom_left": grinch sound (grinch)
    """
    offsets = [
        (0, -1),  # Left
        (0, 1),   # Right
        (-1, 0),  # Up
        (1, 0),   # Down
    ]

    for obj in objects:
        for dx, dy in offsets:
            nx, ny = obj[0] + dx, obj[1] + dy
            if 0 <= nx < GRID_ROWS and 0 <= ny < GRID_COLS:
                rect_x = ny * CELL_SIZE
                rect_y = nx * CELL_SIZE
                if position == "top_left":
                    pygame.draw.circle(screen, clue_color, (rect_x + 10, rect_y + 10), 5)
                elif position == "bottom_right":
                    pygame.draw.circle(screen, clue_color, (rect_x + CELL_SIZE - 10, rect_y + CELL_SIZE - 10), 5)
                elif position == "top_right":
                    pygame.draw.circle(screen, clue_color, (rect_x + CELL_SIZE - 10, rect_y + 10), 5)
                elif position == "bottom_left":
                    pygame.draw.circle(screen, clue_color, (rect_x + 10, rect_y + CELL_SIZE - 10), 5)

def update_grid(grid, position, value):
    """
    Updates the grid matrix with the specified value at the given position.
    """
    x, y = position
    if 0 <= x < GRID_ROWS and 0 <= y < GRID_COLS:
        grid[x][y] |= value

def clear_clues(grid, position):
    """
    Clears clues around the given position in the grid matrix.
    """
    x, y = position
    offsets = [
        (0, -1),  # Left
        (0, 1),   # Right
        (-1, 0),  # Up
        (1, 0),   # Down
    ]

    for dx, dy in offsets:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_ROWS and 0 <= ny < GRID_COLS:
            grid[nx][ny] &= ~0xFF  # Clear specific proximity indicators

def draw_legend(screen, font, legend_x, legend_y):
    """
    Draws the legend on the specified position of the screen.
    """
    line_spacing = 40  # Space between legend items

    # Background for the legend
    pygame.draw.rect(screen, (255, 255, 255), (legend_x - 10, legend_y - 10, 220, len(LEGEND_LABELS) * line_spacing + 20))

    # Legend title
    title = font.render("Legend", True, (0, 0, 0))
    screen.blit(title, (legend_x, legend_y))
    legend_y += line_spacing

    # Legend items
    for label, color in LEGEND_LABELS.items():
        pygame.draw.rect(screen, color, (legend_x, legend_y + 10, 20, 20))
        text = font.render(label, True, (0, 0, 0))  # Black text
        screen.blit(text, (legend_x + 30, legend_y))
        legend_y += line_spacing
